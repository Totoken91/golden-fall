#!/usr/bin/env python3
"""Validate planned/generated/approved asset metadata and paths."""
from __future__ import annotations
import json
from pathlib import Path
import sys

REQUIRED = ("id", "category", "status", "source", "export", "license", "generation_method")
STATUSES = {"planned", "generated", "approved"}
CATEGORIES = {"environment", "prop", "character", "foliage", "animation"}


def validate(path: Path) -> list[str]:
    errors = []
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return [f"manifeste inaccessible/invalide: {exc}"]
    if payload.get("schema_version") != 1 or not isinstance(payload.get("assets"), list):
        return ["schema_version=1 et assets[] attendus"]
    ids = set()
    root = path.parent
    for item in payload["assets"]:
        if not isinstance(item, dict):
            errors.append("entrée asset non objet")
            continue
        aid = item.get("id", "<sans-id>")
        for key in REQUIRED:
            if not isinstance(item.get(key), str) or not item[key].strip():
                errors.append(f"{aid}: champ manquant ou vide {key}")
        if aid in ids:
            errors.append(f"{aid}: ID dupliqué")
        ids.add(aid)
        if item.get("status") not in STATUSES:
            errors.append(f"{aid}: statut invalide")
        if item.get("category") not in CATEGORIES:
            errors.append(f"{aid}: catégorie invalide")
        if item.get("status") == "approved":
            qa = item.get("qa", {})
            if not isinstance(qa, dict) or qa.get("technical") is not True or qa.get("visual_in_godot") is not True:
                errors.append(f"{aid}: approved exige une QA technique et visuelle explicite")
            capture = qa.get("capture") if isinstance(qa, dict) else None
            if not isinstance(capture, str) or not capture:
                errors.append(f"{aid}: capture Godot requise pour approved")
            else:
                evidence = (root / capture).resolve()
                if not evidence.is_relative_to(root.resolve()) or not evidence.is_file():
                    errors.append(f"{aid}: capture Godot absente ou hors assets/")
        for key in ("source", "export"):
            val = item.get(key)
            if not isinstance(val, str) or not val:
                continue
            candidate = (root / val).resolve()
            if not candidate.is_relative_to(root.resolve()):
                errors.append(f"{aid}: chemin hors assets/ ({key})")
            elif item.get("status") in ("generated", "approved") and not candidate.is_file():
                errors.append(f"{aid}: fichier {key} absent ({val})")
    return errors


def main(argv):
    path = Path(argv[1]) if len(argv) > 1 else Path("assets/asset_manifest.json")
    errors = validate(path)
    if errors:
        for e in errors:
            print("ERROR:", e)
        return 1
    print(f"OK : manifeste valide ({path})")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
