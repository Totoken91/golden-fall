# Cohésion des matières — V0.17

Retour utilisateur : V0.16 préférée, mais bois trop contrastés/sombres et pixels du chevet trop grands par rapport au bureau. Une résolution commune ne garantit pas une densité commune : 128px sur 1,5m donnent 85,3 texels/m ; sur 0,55m, 232,7 texels/m. Le rapport était 2,727.

Dix groupes de bois passent à 224 texels/m sur les deux axes UV métriques, avec les quatre maps synchronisées. Résolution maintenue à 128px, période rendue 0,5714286m. Les deux essences restent distinctes. Contraste albedo 0,72 autour de la moyenne de chaque canal, exposition 1,06 ; teinte des finitions sombres relevée à (0,42, 0,42, 0,40). Normal, roughness et AO sont réutilisées à l'identique ; seule leur échelle UV suit l'albedo.

Parquet approuvé strictement conservé. Aucun changement de lumière, placement, sommets, indices, collisions ou tissus. 7 970 triangles. Sources officielles déjà en cache, zéro requête réseau et zéro nouveau téléchargement. Provenance, licences, hashes et transformations dans assets/textures/cohesion_manifest.json.

## Reproduire

Après toute nouvelle préparation des matières de chambre, exécuter dans cet ordre :

```powershell
python scripts/textures/prepare_room_materials.py
python scripts/textures/harmonize_room_wood.py
python scripts/textures/harmonize_room_wood.py --verify
```

La deuxième commande réapplique la cohésion après la préparation de base. Les réglages sont dans game/data/room_materials.json. Réimporter Godot et réexporter le PCK après toute modification. L'échelle déclarée dans le matériau publié reste celle de la source ; la passe runtime applique explicitement la densité métrique par surface.

## Comparaison et contrôle

captures/cohesion_v017/index.html : neuf curseurs, avant = V0.16 appréciée, après = V0.17. Les neuf avant reproduisent pixel pour pixel les neuf après V0.16. Caméras et météo identiques entre chaque paire. 82 contrôles runtime réussis, zéro échec. Contrôles de densité, hashes et géométrie dans verification/cohesion_summary.json et comparison.json. Les 31 tests Python de V0.16 sont historiques et n'ont pas été relancés pour cette passe. Inspection artistique moteur effectuée ; validation utilisateur V0.17 encore à recueillir.
