#!/usr/bin/env python3
"""Fast glTF binary integrity and coarse mesh counts. Not a geometric/art test."""
from __future__ import annotations

import json
from pathlib import Path
import struct
import sys


class GlbError(ValueError):
    pass


def inspect(path: Path) -> dict:
    raw = path.read_bytes()
    if len(raw) < 20:
        raise GlbError("En-tête GLB tronqué")
    magic, version, declared_size = struct.unpack_from("<4sII", raw, 0)
    if magic != b"glTF" or version != 2 or declared_size != len(raw):
        raise GlbError("Signature, version ou taille GLB invalide")
    at = 12
    data = None
    binary = None
    while at < len(raw):
        if at + 8 > len(raw):
            raise GlbError("En-tête de chunk tronqué")
        length, ctype = struct.unpack_from("<II", raw, at)
        at += 8
        if length % 4 or at + length > len(raw):
            raise GlbError("Chunk mal aligné ou débordant")
        chunk = raw[at:at+length]
        at += length
        if ctype == 0x4E4F534A:  # JSON
            if data is not None:
                raise GlbError("Plusieurs chunks JSON")
            try:
                data = json.loads(chunk.decode("utf-8").rstrip(" \t\r\n\x00"))
            except (ValueError, UnicodeDecodeError) as exc:
                raise GlbError("JSON GLB invalide") from exc
        elif ctype == 0x004E4942:  # BIN
            binary = chunk
    if not isinstance(data, dict) or data.get("asset", {}).get("version") != "2.0":
        raise GlbError("glTF JSON absent ou version incompatible")
    meshes = data.get("meshes", [])
    if not meshes:
        raise GlbError("Aucun mesh dans cet asset")
    accessors = data.get("accessors", [])
    tris = 0
    for mesh in meshes:
        for prim in mesh.get("primitives", []):
            count_index = prim.get("indices")
            if count_index is not None and not (0 <= count_index < len(accessors)):
                raise GlbError("Index d'accessor invalide")
            if count_index is not None and prim.get("mode", 4) == 4:
                tris += int(accessors[count_index].get("count", 0)) // 3
    return {
        "file": str(path),
        "bytes": len(raw),
        "meshes": len(meshes),
        "nodes": len(data.get("nodes", [])),
        "skins": len(data.get("skins", [])),
        "animations": len(data.get("animations", [])),
        "triangles_estimated_indexed": tris,
        "has_binary_chunk": binary is not None,
    }


def main(argv):
    if len(argv) != 2:
        print("Usage: python scripts/assets/inspect_glb.py path/to/model.glb", file=sys.stderr)
        return 2
    try:
        print(json.dumps(inspect(Path(argv[1])), ensure_ascii=False, indent=2))
        return 0
    except (OSError, GlbError) as exc:
        print(f"ÉCHEC : {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
