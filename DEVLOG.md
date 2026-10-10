# DEVLOG

## 2026-10-09 — V0.8, conservation de la scène et passe ciblée

### Architecture

1. La scène et la pose de comparaison V0.7 sont conservées, avec la même capsule, caméra et résolution de rendu.
2. Le générateur Blender remodèle les tissus, le manteau et les arbres, puis vérifie les intersections manteau/chaise et couverture/matelas avant export.
3. Des textures originales différencient bois, laine, tissage, plastique et métal ; quelques petits objets personnels complètent les surfaces existantes.
4. `RoomWeather` pilote les trois plans de pluie, les gouttes de vitre et le vent, ainsi qu'une brume extérieure liée à la profondeur ; la lumière intérieure est recomposée sans changer la palette.
5. `RoomFilm` déplace une caméra dans la scène réelle pour l'export MovieMaker ; la comparaison fixe garde un temps météo déterminé et la vidéo est encodée en H.264/AAC.

### Itérations visuelles

La vue au même angle a confirmé une meilleure séparation du chevet, de la fenêtre et des coins sombres. Le manteau a été reconstruit en passant au-dessus de la traverse, avec quatre pièces de tissu et des dégagements devant/derrière le dossier. La première vidéo a révélé de petites traversées du matelas sous les bords du duvet ; une coupe dédiée du bord et un contrôle BVH ont corrigé ce problème. La dernière vidéo est recapturée depuis le paquet jouable, avec la pluie active.

La chambre, le cadrage, le style PSX et la palette golden brown sont préservés conformément à la demande humaine. Les photos, la cassette et le casque sont des propositions de décoration sans nouvelle biographie du protagoniste. Aucun service de génération payant ni asset de jeu tiers utilisé. La suite et les autres lieux restent hors de cette passe.

## 2026-10-09 — V0.7, chambre PSX après rejet visuel

### Architecture de cette étape

1. Une scène de revue séparée remplace la scène d'entrée, sans modifier les JSON ni les classes de progression/sauvegarde de V0.6.
2. Un générateur Blender produit une chambre originale fermée, UV et matériaux basse résolution, source `.blend` et export GLB embarquant ses textures.
3. `RoomWalker` associe une capsule physique, une caméra à hauteur humaine, un regard à la souris et un rayon d'interaction de 2,25 m.
4. Un SubViewport 640×360 affiche la 3D en nearest et avec un léger dithering ; `AutumnUI` conserve ses textes et panneaux à résolution native.
5. `room_review` relie quatre interactions à une session éphémère de PC/carnet/agenda ; les décors historiques et leur boucle restent disponibles dans les sources et tests.

### Revue réelle

Le premier rendu a révélé des arbres trop massifs, une ombre d'abat-jour circulaire sur le plafond, des intersections couverture/matelas et un cadrage trop large. Les itérations suivantes ont remplacé les cimes proches par des cartes de feuilles originales, séparé les ombres de l'abat-jour, relevé la couverture et corrigé les UV du clavier. Trois vues en situation et une capture de l'ordinateur sont livrées. La comparaison au concept reste ouverte ; aucune validation artistique n'est déduite des tests.

### Vérification

24 contrôles de chambre, 39 contrôles de logique conservée, 22 d'interface conservée et 16 tests Python réussis. GLB : 48 meshes, 19 900 triangles, source éditable présente. Mesure fixe locale : 120 échantillons après chauffe, 6,94 ms en moyenne, p95 9,65 ms sur RTX 3050 Laptop ; pas de garantie matériel cible. Détails et lacunes dans `VERIFICATION.md`.

Modèle au statut `generated`, autorité de validation humaine conservée. Aucun coût externe, aucune copie de pixels du concept. Rue/diner, PNJ et semaine non étendus.

Le script de distribution utilise désormais le binaire console pour les commandes d'import/export et le binaire graphique pour jouer : le binaire graphique seul ne renvoyait pas sa version dans le pipeline PowerShell.

## 2026-10-09 — V0.6, première journée

### Architecture retenue

1. `ContentDB` charge les mêmes JSON que les validateurs éditoriaux, avec contrôle de synchronisation des copies moteur.
2. `LifeState` centralise l’état, les coûts d’action, les conditions et les souvenirs ; les vues n’appliquent pas de récompense de leur propre initiative.
3. `WebArchive` normalise et classe les recherches locales, puis distingue consultation de page et prise de note explicite.
4. `SaveManager` sérialise l’état v2 par remplacement d’un fichier temporaire et recharge aussi l’exemple v1 avec valeurs par défaut.
5. Les scripts `world` produisent des décors provisoires et l’avatar, tandis que `AutumnUI` présente agenda, dialogues, ordinateur et carnet ; `main` relie les interactions.

### Réalisé

- Première journée : chambre → rue → diner/Hannah → souvenir → PC/recherche → indice → fin au lendemain ; variantes selon les choix.
- Statistique unifiée en `stamina`, vocabulaire des créneaux et routes alternatives déclaré, documentation des données harmonisée.
- Choix cassette différenciés, seuil de confiance exploité, suite pour silhouette évitée et délai d’un jour encodés dans les données futures.
- Validateur renforcé et refus d’un statut asset `approved` sans QA explicite et capture présente.
- Portraits SVG et ambiances WAV originaux provisoires ; trois espaces 3D en primitives ; contrôles clavier, navigation par boutons, sauvegarde/reprise.
- Sources et distribution Windows portable, notices Godot incluses. Aucun appel à un service payant.

### Validation

- 16 tests Python : contrats initiaux et régressions inconnues de la V0.5 (statistique, créneau, accès alternatif, relation, QA).
- 39 vérifications de logique Godot : deux parcours, calendrier, coûts uniques, recherche normalisée, indices explicites, sauvegarde et migration, conditions de mémoire et confiance.
- 22 vérifications d’interface : boutons effectivement reliés, déplacement via événements clavier, arrêt sous panneau, dialogue lié, recherche, note et fin de journée.
- Captures produites par le viewport Godot et examinées ; correction d’un débordement du portrait et d’un éclairage trop fort. Un contrôle automatique garde le portrait hors du texte.

### Limites et trois problèmes de design à éprouver

1. Deux créneaux permettent de construire la chaîne, mais leur intérêt comme dilemme n’est pas encore démontré par un playtest humain.
2. Hannah n’a qu’une courte introduction : l’attachement ne peut pas être déduit du succès des tests.
3. La scène en primitives prouve la lisibilité, mais son aspect de maquette et son cadrage guidé doivent évoluer vers une rue plus intime ; le style final n’est pas validé.

La silhouette n’est pas mise en scène dans cette journée, les sept jours ne sont pas implémentés, le rigging Blender reste non testé. Prochaine priorité : faire essayer la journée, corriger son rythme, puis étendre aux sept jours et à une anomalie préparée par le quotidien. Voir `JOUER.md` pour le lancement et les commandes.

## 2026-10-09 — Pack initial
- Contient vision, références, systèmes, fichiers de données exemples, tests de contrats et consignes de Codex.
- Aucun prototype Godot implémenté à cette date.
- Prochaine étape : boucle Godot jouable sur 7 jours, selon `docs/06_VERTICAL_SLICE.md`.

## 2026-10-09 — Pack V0.5 (pipeline 3D ajouté)

- Ajout docs `17_PIPELINE_ASSETS_3D.md` à `20_INSTALLATION_OUTILS.md` (Blender scripts/MCP, Godot GLB, rigs Mixamo/Rigify, Meshy optionnel, QA).
- Ajout `scripts/assets/generate_streetlamp.py`, `inspect_glb.py`, `validate_manifest.py`, tests sans Blender, `assets/asset_manifest.json` et dossiers sources/export.
- **Aucun asset `.blend` ou `.glb` généré ni validé dans Godot dans ce pack** ; la génération dépend de l'environnement Codex/Blender/Godot réel.
- Mise à jour des consignes de démarrage et roadmap pour que la production 3D soit progressive et ne bloque pas les 7 jours jouables.
- Prochaine étape du pipeline : exécuter A01 avec Blender sur la machine de dev, ouvrir le GLB dans Godot, capturer le résultat et corriger le générateur.
# V0.9 — Construction des accessoires

La chambre et la caméra conservées constituent le contexte de cette passe. Les quatre familles de modèles sont construites dans un module Blender séparé, avec surfaces de vêtement cousues et volumes adaptés à chaque matière. Les textures locales en basse résolution restent embarquées dans les sources et exports. Les exports isolés et le décor assemblé utilisent la même géométrie, affichée dans Godot avec les lumières existantes. Les données de jeu et la pluie restent indépendantes de cette passe d'assets.

La veste V0.8 est rejetée par l'utilisateur : l'absence d'intersection ne suffisait pas à valider sa silhouette en plaque. La V0.9 ouvre les pans, dégage le col, plie les manches et ajoute poches, doublure et coutures. Le clavier, la tasse et le sac sont reconstruits, sans ajout de lore ou de mécanique. Fabrication locale dans Blender/Python, aucun coût externe.

# V0.10 — Sac et budget de géométrie

La chambre, son cadrage et ses lumières restent le contexte de travail. Le sac est reconstruit avec un rabat qui suit les facettes réelles du corps et une sangle plate qui reste hors de son volume et du sol. Les détails de couture et de boucle du rabat passent dans sa texture. Les sections radiales, les grilles de tissu et les biseaux invisibles sont réduits à la construction des assets. Un contrôle bloquant compte les triangles avant export et des contrôles distincts vérifient le sac, les touches, l’absence de vêtement et la couverture contre le matelas.

L'utilisateur a signalé le sac clippé : l'inspection V0.9 avait manqué le rabat et les attaches, tandis que les seuls contrôles d'intersection automatiques concernaient veste/chaise et couverture/matelas. Le budget de projet 16 000 triangles comprend tous les meshes du GLB, y compris les arbres hors champ ; il ne constitue pas une certification matérielle PS1. Les détails sous-pixel privilégient textures et rubans simples, sans agrandir les textures.



## V0.11 — Posters générés (9 octobre 2026)

La demande actuelle autorise deux générations par image_gen intégré pour remplacer les posters. Les originaux figés et les prompts sont conservés dans assets/art/posters, puis réduits en deux textures 192 × 256. Les images sont remplacées dans les matériaux des deux sources Blender, sans modifier géométrie, UV, transformations ou placements. Le GLB, les quatre exports d'accessoires, les données et le cadrage ont été comparés à V0.10 ; le total reste 13 820 triangles et la chaise reste nue. L'exécutable empaqueté est reconstruit, 36 contrôles moteur et 16 tests passent, et de nouvelles captures ainsi qu'une vidéo réelle montrent l'intégration.

À la demande suivante de l'utilisateur, tous les acquis utiles des passes de chambre sont consignés dans docs/22_GUIDE_CREATION_ZONES.md : retours artistiques, géométrie, intersections, textures, génération d'images, lumière, météo, captures, outils et livraison. AGENTS.md, CODEX_START_PROMPT.md et le document de continuité y renvoient. La reconstruction des 43 textures a aussi été exécutée et vérifiée identique octet pour octet, sans nouvelle génération réseau.


## V0.12 — Architecture de la passe PSX (9 octobre 2026)

La deuxième image fournie devient la référence pour les silhouettes plus anguleuses, sans annuler les textures et corrections retenues. Le générateur bpy reconstruit des accessoires avec moins de faces et remplace les détails sous-pixel des livres par un atlas. La literie devient moins gonflée, moins subdivisée et ombrée par faces ; les branches lointaines deviennent des plans croisés. Le budget bloquant est abaissé à 8 000 triangles pour la chambre et tout son extérieur, avec nouveaux contrôles et mêmes contrats Godot. Les sources, exports, captures au cadrage constant et vidéo seront reconstruits avant livraison.

## V0.12 — Résultat et interaction PC

La reconstruction réduit la chambre et tout l'extérieur de 13 820 à 6 680 triangles (−51,66 %), avec formes facettées et deux textures ajoutées pour livres et coutures. Le rabat du sac demande 18 mm de marge sur les nouvelles facettes ; ses trois contrôles d'intersection passent à zéro. La demande complémentaire autorise un vrai écran interactif : Cedar 03 est un viewport 640 × 480 sur le plan existant, avec transition caméra, saisie, recherche d'archives, carnet, fenêtres et retour exact. La pluie devient plus dense avec extérieur assombri ; le MP3 fourni est raccordé en WAV mono de 35,656 secondes. La simulation des événements a nécessité de relâcher aussi les boutons de molette et d'attendre la mise en page avant le clic ; 62 contrôles moteur passent, deux films réels avec son sont recalculés, et les apprentissages sont intégrés au guide de zones.

## V0.13 — Architecture de la passe extérieure

La capture utilisateur montre des arbres trop isolés et une pluie en colonnes répétitives. La forêt sera recomposée en trois bandes de profondeur, avec sous-bois, silhouettes lointaines et masses de feuillage asymétriques. Les textures découpées portent la densité plutôt que des subdivisions, avec budget de chambre et extérieur toujours inférieur à 8 000 triangles. Les trois plans existants de pluie recevront des gouttes réparties par cellule et profondeur, avec rivulets irréguliers sur le verre et sol humide discret. La chambre, son cadrage, les accessoires, le PC physique et le fichier audio fourni seront conservés, puis contrôlés et filmés dans le moteur.

## V0.13 — Résultat

90 arbres remplacent les 44 précédents, avec trois profondeurs, 28 groupes de sous-bois, deux silhouettes lointaines et un ciel couvert. Sept textures de basse résolution ajoutées, 45 précédentes inchangées ; modèle complet 7 406 triangles, soit 726 ajoutés et toujours sous 8 000. Le shader de pluie varie ses gouttes par cellule, le verre porte des ruissellements moins réguliers et le sol des rides discrètes. La géométrie de 54 nodes intérieurs et les quatre exports d'accessoires sont identiques à V0.12, ainsi que PC et audio. 63 contrôles moteur passent, trois vidéos réelles sont refaites ; une capture de référence V0.12 intacte permet le véritable avant/après extérieur.

## V0.14 — Architecture des contacts et de la pluie

Les défauts signalés sont des erreurs de construction et de support des accessoires, pas un manque de subdivisions. Les objets du bureau et du chevet seront alignés sur des surfaces mesurées, avec casque couché et cadre à pied. Les évents du CRT seront dessinés dans le matériau de sa coque inclinée pour éviter toute séparation et économiser des triangles. La pluie utilisera des gouttes indépendantes réparties dans trois volumes extérieurs, avec vitesses, phases et positions variables, sous un plafond total de 8 000 triangles. L'encodage UTF-8 sera réparé et contrôlé, puis les contacts et le mouvement seront vérifiés dans Godot et consignés dans le guide.

## V0.14 — Résultat vérifié

142 appuis, 13 paires d'assemblages, contrôles du sac/touches/literie réussis. 7 250 + 720 = 7 970 triangles ; 53 textures reproductibles dont 52 inchangées. 75 contrôles moteur, 17 tests Python, manifeste valide, deux vidéos Godot 24,10 et 16,10 secondes avec son fourni. Mesure séparée météo et son actifs : 11.66 ms moyen / 15.73 ms p95 dans la vue de porte. Vingt vues studio et six comparaisons rapprochées livrées ; pas d'approbation artistique présumée, aucun coût API externe. Le guide ajoute contacts, ensembles complets, dégagements, limite des grilles de pluie, coût runtime, encodage et import après export effectif.


## 2026-10-09 — Synchronisation documentaire après V0.14

Demande : préciser ce qui reste pour le prototype et vérifier la mémoire du changement visuel. Correction des mentions courantes PS2/troisième personne dans décisions, présentation, art et roadmap ; historique conservé et signalé. Ajout du document 23 : état réel, séparation chambre de revue / première journée historique, ordre recommandé pour intégrer une journée puis une semaine. Aucun changement de jeu, de build ou d'asset ; aucune validation artistique présumée.


## 2026-10-09 — Pipeline permanent de textures officielles

Demande humaine : recherche automatique Poly Haven et ambientCG, téléchargement de vrais fichiers PBR, optimisation, cache/provenance, mémoire AGENTS et test réel ; aucune refonte du jeu.

L'outil Python fonctionne hors du runtime du jeu et utilise exclusivement les API officielles pour rechercher et résoudre les liens de fichiers. Les originaux, reçus et métadonnées restent dans assets/textures, avec variantes optimisées et manifeste JSON. La publication génère des StandardMaterial3D et un catalogue hors ligne pour un composant Godot qui applique une surface précise en fonction de sa période UV en mètres. Les conversions distinguent albedo sRGB, normale OpenGL renormalisée et maps scalaires linéaires, avec un profil réaliste discret plutôt qu'une pixelisation obligatoire. Le classement est une présélection explicite ; les captures moteur et les réserves restent nécessaires avant chaque intégration.

Réseau : premier essai sous sandbox bloqué par résolution DNS ; exécution réseau autorisée ensuite réussie. Poly Haven wood_planks : 7 141 479 octets, quatre maps ; ambientCG Plaster007 : archive de 8 071 422 octets, quatre maps extraites. Huit maps 256px : 442 279 octets. Deux relances hors ligne : aucune requête et aucun octet téléchargé. Les URL finales et hashes sont consignés dans les reçus ; aucun fichier de prévisualisation utilisé.

Validation : 31 tests Python, dont 14 spécifiques au pipeline, réussis ; 18 contrôles Godot réussis et quatre captures réellement inspectées. L'accès au GPU a nécessité l'exécution graphique autorisée après un crash de Godot dans le sandbox. Les tests utilisent un répertoire temporaire dans le workspace pour éviter les restrictions AppData. L'application du parquet utilise le vrai maillage, temporairement en mémoire ; les fichiers existants du jeu/build/assets ont été comparés aux hashes antérieurs sans changement. Enduit sur panneaux de contrôle seulement ; taille 2m déclarée comme hypothèse, répétitions et joints signalés dans les revues. Voir docs/24_PIPELINE_TEXTURES_OFFICIELLES.md et verification/texture_pipeline_summary.json.


## V0.15 — Parquet réduit, 9 octobre 2026

L’utilisateur apprécie le parquet réel et demande sa réduction PSX avec avant/après. Sources du cache transformées hors ligne en 128 et 64px sans nouveau téléchargement. Le choix 128px conserve mieux les joints, avec nearest et mipmaps ; couleurs, force normale, taille physique, UV, lumière et géométrie conservés. Le matériau est appliqué uniquement à la surface floor après prepare_meshes, via configuration et bibliothèque hors ligne ; les sources GLB/Blender sont inchangées. Neuf captures moteur aux caméras figées comparent 256/128/64px en vue large, proche et détail ; leurs matrices, FOV, météo et triangles sont comparés strictement. La V0.14 est conservée.

Contrôle final V0.15 : import explicite des mipmaps dans les fichiers .png.import (un filtre de matériau seul ne les génère pas). Présence effective de sept niveaux vérifiée sur les quatre maps 128px et dans le PCK. Pipeline de publication corrigé pour préparer ces options à chaque nouvelle texture. PCK : 78 contrôles réussis ; 31 tests Python réussis. Comparaisons recapturées après cet import.


## V0.15 — Correction de la référence avant/après

L’utilisateur précise que l’avant doit être le plancher antérieur à toute texture téléchargée. Quatre nouvelles captures moteur restaurent temporairement le matériau original floor du GLB (bedroom_floor.png), puis le comparent au parquet Poly Haven réduit à 128px, en vue de chambre et en détail. Positions et matrices de caméra, FOV, météo et 7 970 triangles strictement identiques. Planches côte à côte et comparateur interactif dans captures/parquet_origine_vs_128/. Le matériau du jeu et son PCK restent inchangés.


## V0.16 — Matières réelles réduites dans la chambre

Parquet 128px validé par l’utilisateur et préservé. Extension ciblée à vingt surfaces groupées, bois, textiles, corbeille et plafond, depuis les fichiers réels des deux API officielles. Inspection de sources et captures moteur ; premier acajou écarté pour ses bandes trop fortes. Trames de tissus composées avec les motifs/coutures/boucles existants. Sources et transformation dans les deux manifestes. Projection métrique et tangentes pour les bois, aucun sommet ni indice déplacé. Lumière, aménagement, collisions, modèles sources, images personnelles et PC physique conservés. Dix-huit captures depuis le PCK, matrices strictement identiques entre neuf couples avant/après ; l’avant chambre reproduit exactement la capture V0.15 validée. 31 tests Python réussis. Les résultats runtime sont dans verification/runtime_materials/.


## V0.17 — Densité des détails et contraste des bois

Ne pas confondre résolution de texture et taille des pixels dans le monde : 128px sur 1,5m contre 0,55m produisent un écart de densité de 2,727. Comparer côte à côte les objets voisins, puis harmoniser les texels/m sans uniformiser leurs essences. Dix groupes de bois à 224 texels/m, contraste adouci, finitions sombres relevées ; parquet approuvé et 7 970 triangles conservés. Aucune acquisition réseau. Neuf avant/après depuis le PCK, avant V0.16 reproduit exactement, 82 contrôles runtime sans échec. Guide et commandes : document 26.


## V0.18 — Dithering retenu et premier socle de campagne

Le contrôleur de campagne hérite de la chambre afin de conserver son rendu et ses collisions. Le même LifeState porte activités, mémoire et enquête. L'OS Cedar reste une vue physique de WebArchive, sans nouvel état d'indice local. La sauvegarde dédiée restaure une session et sa pose d'exploration sans réappliquer les coûts. La revue visuelle et la scène historique restent indépendantes, tandis que la rue/diner, Hannah et les sept jours constituent les prochains lots.

Dithering doux intégré après validation utilisateur du dithering. Activités domestiques, créneaux, note explicite, journal, sauvegarde et reprise raccordés ; borne du premier jour conservée honnêtement. Contrôles réels dans trois processus Godot plus régression de chambre ; résultats exacts et hash dans verification/campaign_summary.json. Géométrie et sources des matières préservées.


## V0.19 — Agenda, journal et sauvegarde sur Cedar 03

Le contrôleur de campagne conserve le noyau unique de progression. L'OS expose agenda, journal et sauvegarde comme fenêtres physiques, sans second stockage des indices. La consultation du PC ne démarre plus l'activité de recherche, désormais déclenchée explicitement dans CedarSearch. La sauvegarde persiste séparément l'ouverture du PC et la session, permettant deux types de reprise sans coût supplémentaire. La pause et l'autosave restent indépendantes tandis que les actions physiques gardent leurs supports dans la chambre.

Barre flottante supprimée de la campagne, J/Tab de gestion externes remplacés par indication du PC. Planning d'intentions, étude sur bureau et repos sur lit. Confirmation de sauvegarde dans le CRT et horloge/date cohérentes. Tests dans quatre processus et régression de chambre ; résultats exacts dans verification/pc_hub_summary.json. Dithering, modèles et matériaux conservés ; aucune extension des zones ou de la semaine dans cette passe.

## V0.22 — Golden Fall direction (2026-10-10)

Creator supplied the Golden Fall V0.9 micro-MVP pack (supersedes earlier packs) and approved: US English, no activity/slot economy, web build on Vercel.

Changed
- Integrated pack docs (`docs/golden_fall/`) and data (`game/data/*_en.json`); old French data, validators and tests removed (kept in previous version folders).
- New core: `GoldenState` (day_index 0–2 = Oct 15–17 2003, time never moves for walking/reading/PC), `SaveManager` (schema 0.9.0, `user://golden_fall_v1.json`, atomic, rejects foreign saves), `WebArchive` (whole-word/prefix search over the pack's pages), `Calendar`.
- Campaign in English: title menu, desk flavour text (no Study), bed asks before sleeping and advances exactly one day; Friday sleep shows a neutral end screen.
- Cedar 03 desktop in English with new apps: Calendar (October 2003 grid), Journal, Messages (mossline IMs per day, unread balloon), Save, Morrow Search, My Documents, Recycle Bin. Research is free; the leave-confirmation and research-cost logic are gone.
- Fixed: game stayed modal after leaving the PC (new flow); Start menu let clicks through to windows behind it (moved to front when opened).
- Web export preset (no threads) and `vercel.json`.

Tested
- `golden_check.gd` day1/day2/day3 in three processes: 55 checks, 0 failures. Bedroom regression `--room-check`: 82 checks, 0 failures. Python: pack contract test (nine Friday combinations), encoding, assets, texture pipeline.
- Web build launched in a browser (WebGL 2, single-threaded): title menu, new game, walking. First frame takes ~10 s in the browser (room material/UV preparation in GDScript).

Not done / known limits
- Street, diner, NPCs, dialogue UI, blips and the Friday event (Stages 1–5).
- Browser fonts fall back to Godot's default; first-load stall in the browser.
