# Vérification actuelle — V0.19

**66 contrôles du hub PC dans quatre processus successifs et 82 contrôles de chambre : zéro échec.** PCK final : voir verification/pc_hub_summary.json.

Consultation gratuite, intention sans coût, étude physique, recherche explicitement payante et unique, note explicite/dédupliquée, reprises gratuites et payantes, journal de fin sur PC et sortie sûre, absence de barre/panneaux de gestion externes, F5 limité au PC avec retour visible, état final, refus de chargement invalide et repos vérifiés. Deux commandes nouvelles sont exercées par de vrais événements souris : icône Agenda et bouton Sauvegarder maintenant. Les tests utilisent leur propre fichier, jamais le slot du joueur.

Régression de la revue indépendante : collisions, raycasts, WASD, pluie, budget, mipmaps/maps et interactions souris/clavier du CRT. Modèles, textures, shaders dont dithering, règles du noyau et liaison des matières conservés par hash. Captures actuelles : captures/interfaces_pc_v019/index.html. Les comptes V0.18 et Python précédents ci-dessous sont historiques et ne constituent pas les résultats courants.

---

# Vérification actuelle — V0.18

**51 contrôles de campagne, trois processus successifs, zéro échec. 82 contrôles de régression de chambre, zéro échec.**

Le même PCK final est utilisé pour le parcours après les cours, la sauvegarde dans le CRT, une première relance qui retrouve la session et l'indice sans coût supplémentaire, puis une seconde relance après sommeil. Parcours alternatif repos/sommeil, chargement invalide, double action, note explicite et unique, retour exact de caméra et journal terminal vérifiés. Slot de test isolé, aucune sauvegarde joueur remplacée.

Régression chambre : collisions, raycasts, WASD/souris, budget 7 970 triangles, vrais mipmaps et maps 128px, densité bois 224 texels/m, pluie extérieure animée et gestes du CRT. Sources Blender/GLB, textures et liaison de sol préservées par hash. Shader de dithering identique à la variante douce de l'essai.

Résumé et hash PCK : verification/campaign_summary.json. Captures du parcours : captures/campagne_v018/index.html. Logs : verification/v018_*.log. Les 31 tests Python V0.16 ci-dessous sont historiques, non relancés. Les contrôles actuels ne valident pas une rue/diner, une rencontre sociale ou les sept jours, qui restent à développer.

---

# Vérification actuelle — V0.17

82 contrôles runtime depuis le PCK, zéro échec. Neuf paires de captures : matrices, météo et triangles identiques ; chaque avant reproduit pixel pour pixel son après V0.16. Dix groupes de bois vérifiés à 224 texels/m, maps 128px. Parquet et fichiers sources préservés par hash. Aucune requête réseau. Résumé : verification/cohesion_summary.json. Les résultats Python 31 tests ci-dessous sont historiques V0.16, non relancés dans cette passe.

---

# Vérification courante — V0.16

**81 contrôles du PCK final, zéro échec ; 31 tests Python réussis.** Les contrôles couvrent les 20 surfaces ciblées, leurs maps 128px et vrais mipmaps, le nombre réel de triangles après application, le parquet conservé, le déplacement, les collisions, le PC physique, ses entrées et son retour de caméra, la pluie et l’audio. Log : `verification/runtime_materials/room_checks.log`.

**Neuf comparaisons / dix-huit captures depuis le PCK final.** Matrices, positions, FOV, météo et triangles strictement identiques avant/après. L’avant de la chambre reproduit pixel pour pixel la capture V0.15 au parquet validé. Les sommets et indices des copies de mesh sont exactement préservés ; 63 contrôles d’attributs, normales reconditionnées avec écart maximal 0,0000981 (<0,0002). Pas de déplacement, nouvelle subdivision ou changement de collision. L’émission de l’abat-jour conserve aussi son opérateur d’origine. Preuves : `captures/matieres_v016/comparison.json` et `verification/material_pass_summary.json`.

129 fichiers de modèles, sources, anciennes textures, audio et shaders comparés par SHA256 : identiques à V0.15. Total inchangé : 7 250 triangles modèle + 720 pluie = **7 970**. Manifeste officiel : 14 variantes vérifiées hors ligne, aucun fichier invalide. Compositions de tissus/plafond contrôlées dans `assets/textures/room_derived_manifest.json` ; les sources téléchargées CC0 sont distinguées des textures d’identité du projet. L’essai de bois trop strié est conservé au cache mais n’est pas appliqué. Les nouvelles matières ont été inspectées dans le moteur, sans prétendre à une validation artistique de l’utilisateur.

Les sections ci-dessous décrivent les passes historiques ; leurs mesures de performance ne sont pas des mesures V0.16.

---

# Vérification — V0.14

**75 contrôles moteur, zéro échec**, dans l'exécutable portable lancé depuis un autre dossier. Déplacement, collisions, interactions, écran physique, souris/clavier dans l'OS, recherche/carnet, retour exact de caméra, pluie extérieure animée, absence de pluie par-dessus l'intérieur, audio et captures. stderr vide et sortie 0. **17 tests Python réussis**, dont la régression d'encodage UTF-8 ; manifeste valide.

## Appuis et géométrie

**142 contacts contrôlés**, écart absolu inférieur à 1 mm : mobilier au sol, étagères, piles, casque sur livre, périphériques sur plateau, souris sur tapis, cadre et lampe sur chevet, radio et corbeille. Les livres de tailles différentes peuvent légèrement dépasser leur support tout en gardant leur centre porté. **13 paires d'assemblages sans intersection de triangles**, dont rideaux/boiseries, rideaux/bureau, rideaux/lampe, lit/chevet, oreillers/matelas, oreillers/couverture, oreillers/tête de lit, lit/murs, cadre/lampe et câble du casque/livres. Ces tests ne traitent pas les joints mécaniques et coutures intentionnels comme des défauts. Détail : verification/contact_checks.json.

Sac : zéro intersection corps/rabat, corps/sangle, rabat/sangle. Touches de clavier : zéro intersection mutuelle. Couverture/matelas : zéro intersection. Chaise sans veste. **7 250 triangles modèle + 720 pluie = 7 970**, cap 8 000 ; mêmes comptes dans Blender, inspection GLB et moteur. Modèle 66 meshes, GLB du jeu identique à l'export.

L'extérieur, ses transformations et ses données de géométrie sont préservés ; seuls des noms automatiques de meshes Cone changent avec l'ajout d'objets intérieurs. Les 52 PNG V0.13 sont identiques ; les 53 textures V0.14 se reconstruisent à l'identique. PC physique, contrôleur du joueur, données, logique, UI du système et son fourni préservés. L'interface de la chambre est réparée. verification/delivery_checks.json et texture_rebuild.json.

## Pluie et images

360 gouttes réparties dans trois volumes. Les 360 vitesses sont indépendantes ; les volumes sont entièrement derrière la fenêtre. L'audit des positions à deux secondes constate des cases vides et des regroupements lorsqu'on projette les positions sur une grille d'analyse 10 × 10 ; cette grille sert uniquement au diagnostic et ne génère pas la pluie. Le moteur vérifie le mouvement et la reproductibilité à temps figé. verification/rain_distribution.json.

01_porte.png et 21_exterieur.png conservent positions, cibles, FOV et temps météo de V0.13. Les différences numériques de base caméra restent sous 10⁻⁶. Six vues rapprochées avant/après ont été recapturées depuis les exécutables V0.13 intact et V0.14, avec entrées verrouillées. Leurs positions, FOV et temps sont identiques et les bases restent dans une tolérance de 10⁻⁶, vérifiées dans verification/contact_camera_checks.json. La première référence avait subi un déplacement de souris à l'ouverture ; elle a été remplacée avant livraison. La physique est suspendue seulement pour ces vues, qui permettent d'inspecter les appuis autrement qu'en plan large. Les captures 25 à 31 montrent aussi le casque, le CRT, le chevet, le rideau, l'aménagement, les pieds et l'interface corrigée.

Vingt vues studio Blender nouvelles, quatre par famille : casque, PC, cadre, literie et fenêtre/rideaux. Contact sheet : captures/34_assets_studio_v014.png. Les images Godot constituent la vérification dans la scène réelle. Les vidéos précédentes sont archivées pour éviter de les confondre avec cette passe.

Deux vidéos nouvelles du moteur : contacts **24,10 s / 723 images**, pluie **16,10 s / 483 images**, 1280 × 720 à 30 images/s, H.264/AAC. Décodage intégral réussi, audio non silencieux sans saturation. Le trajet d'inspection évite un passage trop près de la face du CRT. Ce sont des parcours de caméra automatisés ; ils ne mesurent pas le framerate interactif. Le pack a été reconstruit après cet ajustement du trajet, sans changement du jeu ni du modèle contrôlés.

## Mesure et limites

Mesure séparée avec pluie et audio actifs, sans autre capture/construction en cours : **11.66 ms en moyenne, 15.73 ms au 95e percentile**, 42.19 MiB de mémoire statique Godot, 459 draw calls, RTX 3050 Laptop GPU. 30 images de chauffe et 120 mesures dans la seule vue de porte ; ce n'est pas un benchmark matériel général. captures/performance_live.json. La mesure de la QA figée reste distincte dans performance.json et ne représente pas le coût de l'animation de pluie.

La correction vise les défauts signalés et ceux observés durant l'inspection ; les contrôles automatiques ne constituent pas une approbation artistique. Sources et rapports sont livrés pour poursuivre les retours. Aucune nouvelle zone ni mécanique de progression ajoutée.

Les scripts de recapture et de mesure séparée sont livrés dans scripts/qa/. Ils utilisent les ressources du PCK lorsqu'ils sont lancés avec l'exécutable portable et --script <chemin absolu du script>. Définir LHC_REFERENCE_DIR et LHC_REFERENCE_PREFIX pour les comparaisons, LHC_QA_DIR pour la mesure. Les versions précédentes sont conservées intactes.


## V0.15 — Parquet 128px

31 tests Python réussis. PCK final : 78 contrôles moteur, zéro échec, y compris les sept niveaux de mipmaps effectivement importés. Avant/après : neuf captures réelles, trois caméras dont position, matrice, FOV, météo et géométrie sont identiques entre 256/128/64px. Modèles, UV, générateurs Blender, textures de chambre antérieures, shaders et audio ont des hashes identiques à V0.14 ; seul le matériau floor est remplacé à exécution. Résultats actuels : verification/parquet_summary.json, verification/runtime_parquet/room_checks.log et captures/parquet_psx/cameras.json. Les autres sections décrivent les contrôles antérieurs V0.14.
