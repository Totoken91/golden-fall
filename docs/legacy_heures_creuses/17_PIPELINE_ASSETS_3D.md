# 17 — Pipeline de production 3D : Blender → Godot

**Statut : proposition technique ajoutée au pack V0.5 (9 octobre 2026).** La direction artistique, le genre et les choix narratifs validés dans `00_DECISIONS.md` restent inchangés. Ce pipeline ne constitue pas une obligation d'installer des outils payants, ni une demande d'étendre le périmètre de P0.

**Actualisation V0.14 :** le pipeline Blender/Python → GLB → Godot est utilisé pour la chambre livrée. La direction courante est PSX / première personne (`21_REORIENTATION_VISUELLE_PSX.md`) et les acquis sont dans `22_GUIDE_CREATION_ZONES.md`. Les budgets et références PS2 des sections V0.5 ci-dessous sont historiques : pour reproduire la chambre, employer les réglages V0.14, sans les extrapoler en budget global du jeu.

## But de production

Transformer les références Golden Autumn Gothic en **assets 3D éditables, répétables, vérifiables**, sans dépendre à chaque livraison d'une génération opaque. Le prototype doit pouvoir être lancé avec un greybox, mais chaque placeholder important doit rester aligné avec les proportions, couleurs et cadrages du projet.

**Règle d'or :** générer des *familles d'assets* à partir de gabarits partagés (panneaux, façades, bardages, fenêtres, arbres, lampadaires) plutôt que 100 modèles autonomes incohérents.

### Outils par rôle

| Rôle | Outil principal | Usage Codex | Limite |
|---|---|---|---|
| Décor / mobilier / architecture | Blender + `bpy` en mode batch | Écriture, exécution, itération de scripts versionnés | Le rendu doit être inspecté ; code valide ≠ asset esthétique |
| Retouches et aperçu | MCP for Blender, optionnel | Inspecter scène, manipuler objets, faire évoluer les générateurs | Nécessite Blender sur machine accessible + extension activée |
| Conception personnage | Base humanoïde low-poly travaillée dans Blender | Variantes de corps, vêtements, coiffures, couleurs | Topologie et silhouette à approuver humainement |
| Rig de base | Mixamo *ou* Rigify (choix à tester) | Import/export et scripts de vérification | Auto-rig non garanti ; Mixamo comporte une étape manuelle |
| Animations de base | Bibliothèque réutilisable | Idle, walk, turn, sit, talk, look-back | Nécessite retarget / correction des pieds et des contacts |
| Génération IA 3D facultative | Meshy/Tripo avec crédits et API | Référence/blocage organique ponctuel | Coût, licence, topologie et cohérence à contrôler |
| Livraison moteur | glTF 2.0 `.glb` → Godot | Import, collision, scène héritée, animation | Rendu des matériaux et retargeting à tester dans Godot |

Le pipeline par défaut doit **fonctionner sans MCP et sans API externe** : Blender local + scripts Python + export GLB + import Godot.

## Workflow conseillé, par asset

1. **Brief** : fonction, zone, échelle (mètres), références, budget géométrique et texture, matériaux et interactions.
2. **Génération** : créer `assets/source_blender/<categorie>/<asset>.blend` à partir d'un script `scripts/assets/` ou d'un travail manuel versionné.
3. **Contrôle technique** : origine/pivot stable, pas de scale accidentelle, axes, normals, noms, UV si textures, collision séparée du visuel.
4. **Contrôle visuel** : vues face, profil, 3/4 et vérification en lumière froide diffuse + lumière ambre. Voir `docs/19_QUALITE_ASSETS.md`.
5. **Export** : `.glb` dans `assets/exported/`, source `.blend` conservée. Un export raté ne remplace pas le précédent validé.
6. **Intégration** : scène Godot héritée, collisions et matériaux complémentaires si nécessaires ; ne pas modifier le GLB brut dans l'éditeur.
7. **Validation dans le jeu** : échelle relative au joueur, caméra réelle, silhouette à l'écran, lisibilité du soir et performance.

### Commandes locales

```bash
# Création automatisée par Blender (si installé dans le PATH)
blender --background --python scripts/assets/generate_streetlamp.py -- --out-dir assets

# Vérifier la structure d'un GLB sans Blender
python scripts/assets/inspect_glb.py assets/exported/prop_streetlamp_sodium.glb

# Vérifier le manifeste des assets planifiés / livrés
python scripts/assets/validate_manifest.py assets/asset_manifest.json

# Vérifier les données du jeu (script déjà présent en V0.4)
python scripts/validate_content.py
```

Ces commandes sont des recettes **à exécuter** ; leur présence ne prouve pas que Blender ou Godot sont installés sur la machine. Voir `docs/20_INSTALLATION_OUTILS.md`.

### Structure de fichiers (une source unique de vérité)

```text
assets/
  README.md
  asset_manifest.json             # ID stable, source, export, statut, droits, tests
  source_blender/                 # .blend éditables
  exported/                       # .glb moteur, une ressource par fichier
  previews/                       # contact sheets, GIF/vidéos de validation
  animation_library/              # fichiers de clips + documentation de rig
scripts/assets/
  generate_streetlamp.py          # pilote de génération procédurale
  inspect_glb.py                  # garde-fou conteneur GLB
  validate_manifest.py           # garde-fou inventaire
```

## Bibliothèque modulaire pour Morrow Creek

Construire progressivement dans cet ordre :

**P0 — décors fonctionnels**
- `prop_streetlamp_sodium` : lampadaire, cône lumineux contrôlé dans Godot, pas dans texture émissive seule.
- `prop_crt_monitor`, `prop_desk`, `prop_mug`, `prop_cd_stack`, `prop_diner_booth` : objets essentiels pour l'ambiance.
- `env_wall_wood_a`, `env_window_rain_a`, `env_sidewalk_segment`, `env_diner_window` : kit réutilisable.
- `foliage_maple_a`, `foliage_pine_a`, `foliage_leaf_decal_a` : géométrie minimale, variantes par couleurs/rotation.

**P1 — industrialisation**
- Gabarit de maisons à panneaux interchangeables : toitures, fenêtres, bardages, porches, degrés d'usure.
- Diner intérieur/extérieur enrichi, boutique de disques, éclairage local.
- Système de placement déterministe (seed, variante, rotation et densité) pour feuilles et petits props.

**P2/P3 — très sélectif**
- Scierie Black Alder Mill, bâtiments industriels, forêt profonde, intérieurs narratifs uniques.
- Personnages secondaires et leurs costumes, décors d'événements.

## Discipline de style : ne pas confondre image de référence et mesh 3D

Les mockups d'inspiration fournis dans les échanges sont **plus détaillés qu'un vrai rendu PS2**. Viser le même cadrage, la lumière, le ton et les matériaux, **pas** leurs innombrables détails ou une photogrammétrie. Low-poly intentionnel, silhouettes lisibles, textures modestes, bords irréguliers sélectifs et une composition solide.

### Budgets initiaux *indicatifs, non validés par benchmarking*

| Catégorie | Triangle budget pilote | Texture de départ | Priorité |
|---|---:|---|---|
| Très petit prop (livre, tasse, boîte CD) | 30–400 | 128–256 px | Réutilisation |
| Prop structurant (lampe, chaise, CRT) | 200–1 500 | 256–512 px | Silhouette |
| Bâtiment modulaire simple | 1 000–6 000 | atlas 512–1024 px | Réemploi |
| Personnage jouable / PNJ proche | 2 000–8 000 | 512–1024 px | Animation et proportions |
| Arbre low-poly / hybride planes | 150–2 000 | atlas 256–1024 px | Densité / distance |

Ce ne sont **ni des exigences historiques PS2, ni des plafonds définitifs**. Ajuster seulement après profiling dans la cible Godot et constat visuel (collisions, transparence, ombres et draw calls comptent autant que les triangles).

### Matériaux et lumière

- Gérer deux jeux d'éclairage Godot : fin d'après-midi dorée, soirée/pluie. Pas d'éclairage baked définitif avant implantation du décor.
- Materiaux mats à rugosité élevée, micro-usure sélective ; pas de surfaces plastiques excessivement brillantes.
- Ne pas remplacer la géométrie faible par un LUT orange écrasant : palette de `docs/08_DIRECTION_ART.md`.
- Pluie et feuilles doivent être économes : decals/particules locales, pas simulation physique coûteuse.

## Intégration Godot 4.x

- Format transport principal : **glTF 2.0 binaire `.glb`** ; source `.blend` non destructrice.
- Pour collision, navigation, interaction et éclairage : **scène Godot distincte** qui référence l'import (`.tscn` hérité ou composition) ; ne pas dépendre de modifications à l'intérieur du `.glb`.
- Conserver l'échelle réelle : une unité Blender = 1 mètre dans le pipeline choisi ; vérifier hauteur de porte et personnage en jeu.
- Tester un personnage animé dans le moteur avant d'importer une bibliothèque entière (voir `18_RIGGING_ANIMATION.md`).
- Utiliser un *profiling check* de la zone en jeu et consigner le résultat, pas une estimation chiffrée inventée.

## Pipeline évolutif et signaux d'échec

| Échec visible | Correction | Ne pas faire |
|---|---|---|
| Bâtiments tous différents et hors style | Revenir à un atlas de matériaux et kit modulaire | Générer plus de bâtiments indépendants |
| Mesh déformé / UV absent | Retoucher source Blender et regénérer | Cacher derrière une LUT |
| PNJ visuellement générique | Approver un personnage pilote avant variantes | Faire un casting entier en une passe |
| Animations pied glissant / bras passant dans corps | Retarget, contact au sol, vérification en Godot | Qualifier l'animation « finie » |
| Codex bloqué par Blender absent | Greyblox en primitives Godot, documenter le manque | Exiger un asset externe pour jouer à P0 |
| API IA payante demandée | Chiffrer, autorisation explicite, trace de licence | Utiliser clé / crédits sans autorisation |

## Définition de « prêt à produire »

Un **lampadaire** et une **banquette de diner** peuvent être regénérés, corrigés et réimportés sans tout refaire ; un **humanoïde pilote** se déplace et s'assoit sans problèmes majeurs de silhouette ; un panorama de rue atteint le Golden Autumn Gothic avec peu d'assets ; les tests et previews distinguent ce qui est validé de ce qui reste expérimental.

**Sources de travail (vérifiées octobre 2026)** :
- Blender CLI : https://docs.blender.org/manual/fr/4.5/advanced/command_line/arguments.html
- Godot import 3D : https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_3d_scenes/index.html
- Godot formats glTF : https://docs.godotengine.org/en/4.6/tutorials/assets_pipeline/importing_3d_scenes/available_formats.html
- MCP for Blender (communautaire) : https://github.com/ahujasid/mcp-for-blender
