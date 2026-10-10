# 20 — Installer Blender + Codex + Godot pour le pipeline 3D

**Important** : ces outils sont à installer **sur la machine qui doit exécuter Blender/Godot**. Un Codex cloud sans accès aux programmes locaux ne peut pas piloter à distance Blender du PC simplement parce que son MCP est déclaré.

## Option 1 — Pipeline local sans MCP (recommandé pour commencer)

1. Installer Blender et Godot 4.x depuis leurs sites officiels ; vérifier `blender --version` et `godot --version` dans le terminal si présents dans le PATH.
2. Exécuter `blender --background --python scripts/assets/generate_streetlamp.py -- --out-dir assets` depuis la racine du dépôt.
3. Inspecter `assets/source_blender/prop_streetlamp_sodium.blend` et `assets/exported/prop_streetlamp_sodium.glb` ; intégrer le GLB dans la scène de rue Godot.
4. Lancer `python scripts/assets/inspect_glb.py ...` puis valider visuellement le rendu en jeu.
5. Utiliser les générateurs batch pour la plupart des objets répétitifs ; garder Blender GUI pour les retouches artistiques.

## Option 2 — MCP for Blender (facultatif)

Source communautaire : https://github.com/ahujasid/mcp-for-blender — **non officiel**, permet notamment à un assistant de faire exécuter du Python dans Blender. N'activer que dans un environnement de travail de confiance.

**Si `uv` est installé**, assistant de configuration :

```bash
uvx mcp-for-blender setup
```

Alternative manuelle (Codex CLI) :

```bash
codex mcp add blender -- uvx mcp-for-blender
uvx mcp-for-blender install-addon
codex mcp list
```

Ouvrir Blender → activer l'extension `MCP for Blender` dans les add-ons si nécessaire → panneau latéral `N` → démarrer la connexion si elle n'est pas déjà active. Redémarrer Codex après installation quand requis.

Le package s'appelait autrefois `blender-mcp` ; pour une nouvelle installation, utiliser `mcp-for-blender`. Les commandes pouvant évoluer, vérifier le README du dépôt au moment d'installer.

### Sécurité MCP / plugins externes

- Le serveur autorise l'exécution de code dans Blender. **Réviser les scripts** avant de les exécuter, particulièrement ceux qui téléchargent des ressources ou accèdent au disque.
- Les packs tiers (Modèles IA, Sketchfab, etc.) peuvent avoir des conditions/licences différentes ; ne pas importer au hasard.
- Ne pas stocker de clé API dans `AGENTS.md`, `asset_manifest.json`, le dépôt ou les logs ; variables d'environnement/secrets locaux seulement.
- Ne pas payer ni générer via des crédits externes sans accord explicite.

## Dépannage rapide

| Symptôme | Vérification |
|---|---|
| `blender: command not found` | Installer Blender ou pointer vers son exécutable (`blender.exe` sous Windows). |
| `uvx` absent | Installer `uv` avec la méthode officielle ; puis relancer le terminal. |
| Codex ne voit pas Blender | `codex mcp list` ; extension active ; relancer Codex ; même machine ? |
| GLB vide ou faux pivot | Sélection exportée, objets exclus, échelle et origine Blender. |
| Couleurs différentes dans Godot | Réglages d'exposition/tonemapping, textures, shader ; Godot est la référence visuelle finale. |
| Personnage animé déformé | Pose de repos, mapping os, retargeting et weights. |

## Critère « installation réussie »

Un unique asset généré en `.blend` et `.glb`, visible dans une scène Godot, peut être **regénéré deux fois** avec la même identité et validé par les scripts. Pour le rigging, ajouter un test séparé : mannequin animé Idle/Walk dans Godot.
