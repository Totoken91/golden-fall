# Assets — source, export, qualité

Les sous-dossiers ont volontairement été laissés sans modèles : Blender/Godot ne sont **pas** exécutés à la génération de ce pack. Le premier objet planifié est `prop_streetlamp_sodium`, avec un script Blender fonctionnel **à exécuter et valider dans Blender/Godot**.

Depuis la racine du projet, sur une machine équipée de Blender :

```bash
blender --background --python scripts/assets/generate_streetlamp.py -- --out-dir assets
python scripts/assets/inspect_glb.py assets/exported/prop_streetlamp_sodium.glb
```

Puis passer `status` de `planned` à `generated` dans `asset_manifest.json` (jamais automatiquement à `approved`) et exécuter `python scripts/assets/validate_manifest.py`. Après validation en jeu et captures : `approved`.

Les dossiers `source_blender/`, `exported/`, `previews/`, `animation_library/` ne contiennent pas d'asset final. Conserver les sources `.blend` versionnées. Les caches de Godot n'ont pas leur place dans ces dossiers.

Voir `docs/17_PIPELINE_ASSETS_3D.md` à `docs/20_INSTALLATION_OUTILS.md`.
