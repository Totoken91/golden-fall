# Matières de la chambre — V0.16

Le porteur de projet valide le parquet et sa réduction, puis demande le même travail sur le maximum d’objets où cela a du sens. Le sol reste strictement identique. Les anciennes versions restent intactes.

## Surfaces retenues

| Famille | Source réelle | Intégration |
|---|---|---|
| Bureau, appui et petits bois | Poly Haven wood_table_worn | 128px, grain et usure de table, normales discrètes |
| Étagères, chaise, lit, chevet, commode, porte et encadrements | Poly Haven wood_table_001 | Grain fin, albedo brun équilibré, deux valeurs de finition selon le bois d’origine |
| Rideaux et abat-jour | Poly Haven rough_linen | Trame réelle, couleur bleue source neutralisée ; palette olive/beige et émission de lampe conservées |
| Matelas, oreillers, couverture | Poly Haven cotton_jersey | Trame réelle avec couleurs, patchwork et coutures d’origine |
| Sac, rabat et tissu de haut-parleur | ambientCG Fabric061 | Toile réelle, palette et boucles/coutures d’origine conservées |
| Corbeille | ambientCG Metal046B | Métal sombre mat, tuile de travail estimée à 0,5m |
| Plafond | ambientCG Plaster007 du cache | Enduit discret, contribution de luminance 22%, palette existante conservée |

L’essai dark_wood a été écarté après inspection : ses bandes prenaient trop de place sur les meubles. Ses fichiers acquis restent dans le cache avec cette réserve. Le matériau de meuble final est exposé dans son albedo pour retrouver la gamme du bois précédent, sans toucher aux lumières ni cuire d’éclairage dans les textures. Les profils et teintes sont enregistrés.

Papier peint, tapis, posters, photos, livres/atlas imprimés, PC et ses évents, céramique, cuir des sangles et petites pièces métalliques gardent leurs matières propres. Leur remplacement générique ferait perdre une identité ou serait peu lisible à cette échelle.

## UV et géométrie

Les groupes de meubles assemblent des pièces dont les anciens tilings diffèrent. La passe crée une copie de leurs arrays en mémoire : seuls UV et tangentes changent. La projection de chaque face existante est exprimée en mètres, avec le grain sur son axe le plus long. wood_table_worn a le grain suivant U ; wood_table_001 suivant V. La tuile physique source vient de l’API. Positions et indices restent exactement identiques ; les normales plates subissent seulement la quantification de stockage ArrayMesh, avec écart vectoriel contrôlé inférieur à 0,0002. Les collisions existantes, transformations et fichiers GLB/Blender sont conservés.

Pour les tissus uniques, les maps réelles sont répétées selon une estimation de leur étendue UV physique puis réduites à un atlas 128px. Leur luminance module la texture d’identité existante ; normal et roughness sont traitées comme données, sans teinte. Les normales réduites sont renormalisées et les roughness textiles restent mates. Le manifeste de dérivation décrit chaque source, hypothèse d’échelle, hash et transformation. La licence CC0 concerne le composant téléchargé ; aucune nouvelle licence n’est imposée aux textures personnelles du projet.

## Reproduire et contrôler

Après acquisition des sources officielles avec le pipeline décrit dans le document 24 :

```powershell
python scripts/textures/prepare_room_materials.py
godot --headless --path game --editor --import --quit
godot --path game --script <chemin_absolu>/scripts/qa/room_material_compare.gd
python scripts/textures/pipeline.py verify --offline
python scripts/textures/prepare_room_materials.py --verify
```

Le script QA restaure les véritables matériaux et meshes de V0.15 pour l’avant, avec le parquet validé, puis remet les nouvelles matières pour l’après. Il verrouille les entrées, la physique, les matrices, le FOV et le temps météo ; il sauvegarde 18 captures, neuf vues. Les positions de sommets et indices sont comparés exactement, les normales selon la tolérance ci-dessus. Les mipmaps doivent exister réellement, pas seulement être demandées dans le matériau.

Les captures finales sont obtenues depuis le PCK jouable. `captures/matieres_v016/index.html` permet le curseur, l’affichage entier avant/après et les vues côte à côte. Les autres captures/vidéos du dossier sont historiques. Résumé : `verification/material_pass_summary.json`. Le budget reste 7 250 triangles de modèle et 720 de pluie, soit 7 970. Cette passe ne développe aucune nouvelle zone ou mécanique.
