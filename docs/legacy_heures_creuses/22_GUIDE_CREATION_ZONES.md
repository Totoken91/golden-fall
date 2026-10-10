# Guide de création des prochaines zones — acquis V0.7 à V0.13

Mis à jour le 9 octobre 2026, à la demande du porteur de projet : consigner les apprentissages pour créer les prochaines zones plus facilement. Base technique actuelle : **chambre V0.13**. Les chemins ci-dessous partent de la racine du pack. Ce guide documente ce qui a été construit et vérifié ; les propositions pour les autres zones restent des propositions.

## 1. Ce que les retours du porteur de projet nous ont appris

- La qualité se juge dans le jeu, depuis le vrai point de vue. Un modèle propre dans Blender, un nombre élevé de détails ou une jolie image de concept ne suffisent pas.
- La scène et son cadrage ont commencé à fonctionner en V0.7 ; l'utilisateur a demandé de les conserver. Pour une passe ciblée, préserver position, orientation, FOV et résolutions. Éviter de masquer un problème en changeant la caméra.
- Garder une esthétique **PSX et golden brown** : silhouettes simples, ambre/cuivre/bois, vert sombre, ivoire et brume naturelle. Ne pas transformer toute l'image en orange uniforme. Les matériaux doivent se distinguer par leur motif, leur fréquence de détail et leur réponse à la lumière.
- Un extérieur trop proche et géométrique détruit la profondeur. Un éclairage uniforme aplatit la pièce. Une literie faite de blocs rigides donne un résultat artificiel. Ces trois problèmes se traitent par composition, distance, lumière et silhouette avant d'ajouter des objets.
- Des accessoires qui traversent leur support ou leur propre volume restent visibles malgré le style rétro. La veste a été critiquée puis son retrait demandé ; **ne pas la réintroduire**. Le sac a nécessité un vrai contrôle géométrique, pas uniquement une vue avantageuse.
- L'utilisateur veut peu de polygones. La V0.9 était montée à 39 520 triangles ; la V0.10 est revenue à 13 820, baisse d'environ 65 %. Un détail sous-pixel appartient souvent à la texture. La V0.11 était encore trop arrondie et dense selon le nouveau retour ; V0.12 descend à **6 680 triangles (−52 %)**. Améliorer un asset signifie ici mieux choisir sa silhouette et ses textures, sans ajouter systématiquement des faces ou du lissage.
- Les premiers posters procéduraux manquaient d'identité. En V0.11, l'utilisateur a explicitement demandé imagegen : deux illustrations originales, réduites en textures, ont remplacé les anciens dessins. Leur validation artistique finale reste à l'utilisateur.

## 2. Référence technique à reprendre

| Élément | Base éprouvée |
|---|---|
| Moteur | Godot 4.6, GL Compatibility |
| Construction 3D | Blender 4.2.2, scripts Python/bpy |
| Sources | `assets/blender/hero_props.blend` : objets séparés ; `bedroom_psx.blend` : modèle assemblé |
| Export de référence | `assets/exported/bedroom_psx.glb`, copie identique dans `game/assets/room/bedroom.glb` |
| Unités et axes | Mètres ; Blender Z devient Godot Y, Blender Y devient Godot -Z |
| Chambre actuelle | 5,6 × 5,8 m, plafond 2,85 m |
| Rendu du monde | 640 × 360, nearest, sortie 1280 × 720 ; antialiasing désactivé |
| Caméra de jeu | Première personne, hauteur nominale 1,62 m, FOV vertical 62° |
| Budget de chambre | Plafond bloquant de travail 8 000 triangles, chambre **et extérieur complet** ; 7 406 actuellement |
| Météo | Pluie extérieure renforcée, gouttes sur verre, léger mouvement du feuillage ; trois plans, six triangles |
| PC physique | SubViewport 640 × 480 appliqué au plan existant ; caméra rapprochée, OS fictif Cedar 03 |
| Audio pluie | MP3 utilisateur archivé, WAV mono 22 050 Hz, boucle 35,656 s, fondu 2 s |
| Progression | Logique/interface/données séparées, conservées ; pas de refonte nécessaire pour améliorer une zone |

Le budget de 8 000 est un choix de réalisation pour cette chambre, pas un chiffre explicitement imposé par l’utilisateur ni une spécification validée pour toutes les futures zones, ni une garantie de fonctionnement sur une PS1. Définir un budget explicite par zone avant production et compter aussi les objets hors champ. Les trois plans de pluie ajoutent six triangles au modèle de décor.

## 3. Concevoir une zone avec un point de vue de référence

1. Définir l'usage de la zone : où entre le joueur, ce qu'il remarque d'abord et les interactions nécessaires. Les autres lieux et nouveaux éléments de lore demandent leur propre cadrage de périmètre.
2. Établir une vue de référence dans le moteur avec des volumes simples et des mesures crédibles. Consigner les paramètres avant une passe artistique.
3. Régler silhouette générale, circulation, premier plan, plan moyen, profondeur extérieure et points lumineux. Un accessoire très détaillé ne corrige pas une composition plate.
4. Construire les assets visibles à la taille qu'ils occupent réellement en pixels. Améliorer d'abord les silhouettes et les matériaux reconnaissables.
5. Ajouter quelques traces personnelles cohérentes, plutôt qu'une accumulation d'objets sans intention. Dans la chambre : photos, cassette annotée, carnet et posters.
6. Vérifier la zone à hauteur de jeu, aux points de vue proches et en mouvement. Les vues d'inspection complètent la caméra de référence.

Pour la chambre, `captures/camera_comparaison.json` donne la position et la matrice réelles, le FOV, les résolutions et le temps météo. Réutiliser le JSON comme preuve : une position d'entrée similaire ne garantit pas une caméra identique après collisions.

## 4. Modèles : silhouette avant subdivisions

Les modèles existants sont construits par bpy : sommets, faces, UV et matériaux, puis sauvegardés en .blend et exportés en .glb. Ils ne viennent pas d'un générateur texte-vers-3D.

- Réduire les sections radiales des petits tubes, les biseaux invisibles, les faces cachées et les subdivisions de tissu qui ne changent pas la silhouette. Le clavier conserve des touches distinctes avec dix triangles par touche.
- Peindre coutures, boucles, usure, étiquettes et très petits reliefs quand ils n'ont pas besoin d'une silhouette propre.
- Conserver un fichier d'objets séparés avant de regrouper les objets par usage et matériaux pour le runtime. Les accessoires portent `hero_family` pour les exports individuels.
- Les préfixes `C_` et `I_` sont des contrats du contrôleur actuel : collisions du décor et objets interactifs. `I_pc`, `I_desk`, `I_bed`, `I_door` servent aussi aux rayons d'interaction. Ne pas les renommer sans adapter le code. `Outside_`, `Foliage_`, `Glass_`, `Cloth_`, `Shade_` et les noms de matériaux ont aussi un rôle dans la préparation du rendu.
- Les exports individuels conservent actuellement les coordonnées de placement de la chambre. Pour une nouvelle bibliothèque modulaire, définir explicitement les pivots et origines avant réutilisation ; ne pas supposer qu'ils sont déjà centrés à l'origine.

| Accessoire V0.12 / V0.13 | Triangles | Plafond du générateur |
|---|---:|---:|
| Chaise nue | 116 | 160 |
| Clavier | 804 | 820 |
| Tasse | 134 | 150 |
| Sac | 232 | 260 |

Les 87 livres passent à huit triangles chacun, contre 32 avec les anciennes bandes en cubes. La couverture passe de 880 à 356 triangles et chaque oreiller de 176 à 56, avec coutures en texture et aucun cordon géométrique. Ne pas lisser systématiquement ces modèles : les facettes appartiennent à la direction PSX. Ces valeurs sont des repères réels, pas des quotas à remplir. Sources de contrôle : `scripts/assets/asset_geometry_checks.py`, `verification/geometry_budget.json`.

## 5. Contacts et intersections : le cas du sac

L'ancien sac avait un corps traversant le rabat et une sangle engagée dans ses côtés. La correction découpe le rabat sur les **triangles réels** du corps, avec une petite marge extérieure ; une surface approximativement semblable ne suffisait pas. La sangle est un ruban épais placé à l'extérieur, avec un tronçon plat au sol. Les boucles et coutures sont peintes.

En V0.12, réduire les sections du corps rend une facette d’épaule plus abrupte : une ancienne marge de 10 mm laisse trois intersections. Porter le rabat à 18 mm et refaire les contrôles résout ce cas. Une réduction de polygones peut donc réintroduire du clipping même si les pièces semblent garder leur position.

Les contrôles BVH distinguent corps/rabat, corps/sangle et rabat/sangle : zéro intersection pour les trois paires testées. Le point le plus bas du sac est à 7 mm du sol. Le clavier a aussi nécessité un contrôle entre touches individuelles : la barre d'espace était trop large. La couverture simplifiée est testée contre le matelas.

Pour un nouvel assemblage, nommer les pièces et choisir les paires qui ne doivent pas se traverser, puis contrôler les triangles et les distances au support. Inspecter au moins face et profil, ainsi que sous la lumière de jeu. Les contacts intentionnels et pièces jointives doivent être distingués des traversées. Un contrôle sur quelques paires n'est pas une preuve d'absence de toute intersection dans la scène.

## 6. Textures et imagegen

La chambre emploie 52 textures : 45 inchangées depuis V0.12 et sept nouvelles pour canopées, sous-bois, forêt lointaine et sol humide. Les ornements des livres et coutures des oreillers restent peints. Les textures procédurales sont principalement en 128 ou 256 pixels ; les deux lignes de forêt lointaine sont en 512 × 128. Les deux posters V0.11 utilisent des originaux **image_gen intégré**, conservés en 1086 × 1448, réduits en RGB **192 × 256**. Aucun polygone ajouté.

Pour un nouveau poster ou une illustration :

1. Décrire un asset plat, de face, remplissant son rectangle ; préciser ratio, palette, médium, composition et texte exact. Exclure mur, cadre et mockup si le jeu fournit déjà le support.
2. Faire un appel distinct par image originale. Préférer des masses lisibles et une hiérarchie typographique forte aux petits détails qui disparaissent en jeu.
3. Inspecter le résultat : orthographe, éléments non demandés, cohérence avec 2003 et avec l'univers. Une consigne dans le prompt ne prouve pas qu'elle a été respectée.
4. Copier l'original retenu **dans le projet**, conserver le prompt exact et la provenance. Ne pas dépendre du dossier personnel des images générées.
5. Réduire techniquement l'image aux dimensions du jeu ; conserver son ratio et ne pas couper les titres. Vérifier sous l'éclairage réel. Ici : Lanczos lors de la réduction, nearest au rendu.
6. Livrer l'original et la texture utilisée. Indiquer honnêtement « illustration générée puis réduite », sans la présenter comme du pixel art natif.

Fichiers de référence : `assets/art/posters/prompts.json`, `scripts/assets/prepare_poster_textures.py`, `apply_poster_art.py`. Pour une simple nouvelle image, remplacer les nœuds de texture dans les deux .blend puis réexporter ; inutile de reconstruire toute la géométrie. Cette passe compare aussi sommets, indices, normales, UV, transformations et affectations des matériaux du GLB pour démontrer qu'ils sont inchangés.

La génération n'est pas déterministe ; l'original livré est une source figée. La réduction et l'intégration sont reproductibles hors ligne. `make_room_textures.py` réapplique les originaux après ses textures procédurales, pour ne pas écraser les posters lors d'une reconstruction. Conserver l'historique de RNG si on veut éviter de modifier involontairement toutes les textures. La reconstruction des 43 textures a été exécutée et comparée en V0.11 : résultats identiques octet pour octet, consignés dans `verification/historique_v011/texture_rebuild.json`. La reconstruction V0.13 porte sur 52 textures, toutes identiques après régénération, dans `verification/texture_rebuild.json`.

L'autorisation explicite actuelle concerne ces posters. Elle ne vaut pas accord général pour consommer des crédits via un autre service. Utiliser l'outil intégré quand autorisé ; aucune génération nécessaire pendant le jeu.

## 7. Éclairage, tissus et extérieur

L'éclairage actuel combine une ambiance faible, une source chaude localisée à la lampe, une entrée de fenêtre plus froide et des rebonds discrets. Les valeurs exactes résident dans `game/scripts/room_review.gd`, fonction `build_view()`. Les comparer dans le moteur plutôt que recopier des valeurs isolées dans une nouvelle pièce aux dimensions différentes.

En V0.12, renforcer la pluie signifie densifier/allonger/accélérer les traînées et gouttes dans les shaders existants. Assombrir le ciel et la lumière de fenêtre conserve le contraste avec la lampe chaude ; aucun filtre bleu uniforme ni géométrie de particules ajoutée.

Le verre contient une salissure faible ; la pluie et les gouttes sont animées séparément. Les trois couches de pluie restent **dehors**, sans effet qui recouvre toute l'image. Les contrôles vérifient que la fenêtre change entre deux temps météo, tandis qu'une région intérieure reste identique.

Les arbres utilisent des branches/feuillages en plans découpés avec transparence et des silhouettes variées. Pas de cônes opaques empilés. En V0.13, 90 arbres occupent trois profondeurs, avec 28 groupes de sous-bois et deux masses de silhouettes lointaines. Le plus proche centre d'arbre est à environ 13.37 m de la fenêtre dans cette chambre ; la distance, les couches et la brume créent la profondeur. C'est une référence de mise en scène, pas une distance universelle.

La literie utilise des plis statiques et une silhouette irrégulière. Pas de simulation textile nécessaire pour cette zone. Le nombre de subdivisions doit servir les plis visibles ; éviter de densifier toute la surface pour corriger un coin.

## 8. Vérifier dans le vrai moteur

- Construire le pack Windows, puis lancer **l'exécutable livré depuis un autre dossier**, avec son .pck. Vérifier code de sortie, stdout et stderr avant de regarder les captures.
- Une image existante peut être héritée de la version précédente : vérifier sa date et la réussite de la nouvelle capture. Ne pas confondre concept généré, rendu studio Blender et capture Godot.
- Les vues proches sont des caméras d'inspection. La caméra de référence reste inchangée. Dans les vues d'inspection à l'intérieur d'un volume de meuble, suspendre la physique du personnage uniquement pendant la prise : sinon la capsule peut être repoussée et fausser le cadrage. Ne pas modifier les collisions du jeu pour prendre une capture.
- Geler la météo au même temps pour comparer des images. La réactiver pour vérifier la pluie et le feuillage en mouvement.
- Capturer une courte vidéo de la **scène 3D réelle** avec le parcours `game/scripts/room_film.gd` et Godot MovieMaker. Une image animée artificiellement ne vérifie pas la perspective, les occultations ou le clipping.
- Le mode actuel produit 633 images, 21,10 secondes, 1280 × 720 à 30 images/s ; encodage H.264/AAC et décodage intégral vérifié. La vitesse MovieMaker ne mesure pas les FPS en jeu.
- Mesurer les performances séparément : vue identifiée, chauffe, nombre d'images, matériel et conditions. La mémoire statique Godot n'est pas toute la RAM du processus ni la VRAM. Aucun chiffre court ne garantit une performance sur une autre machine.

Historique V0.12 : **62 contrôles moteur, zéro échec ; 16 tests Python ; manifeste valide**. Reconstruction des 45 textures identique ; nouveaux contrôles géométriques sur les modèles réduits. Vidéo de chambre 633 images/21,10 s et PC 723 images/24,10 s, toutes deux avec le son utilisateur. Les anciennes preuves spécifiques aux posters sont classées dans verification/historique_v011/. Le statut `generated` ne devient pas `approved` automatiquement après un test technique.

## 9. Pièges techniques rencontrés

- Blender : ajouter `--python-exit-code 1` ; sinon une exception Python peut laisser un code de sortie trompeur. Garder les logs et vérifier l'export réellement produit.
- Godot 4.6 : faire une importation headless puis `--script res://scripts/room_review.gd --check-only` avant l'export. Une erreur de parsing ne doit pas se retrouver dans un pack livré.
- Compteurs de viewport : `get_render_info` prend **deux arguments**, type puis information, par exemple `Viewport.RENDER_INFO_TYPE_VISIBLE, Viewport.RENDER_INFO_PRIMITIVES_IN_FRAME`. Un seul argument est invalide ici.
- Le nombre de primitives visibles du viewport diffère du budget du modèle entier. Compter les triangles avant export, dans le GLB et après import Godot.
- Les images du .blend doivent être embarquées, puis les chemins locaux réorientés vers les fichiers du nouveau pack. Un fichier qui ne marche que grâce à une ancienne version sur le disque n'est pas portable.
- Sous Windows, lancer les processus de capture en arrière-plan avec fenêtre masquée et des chemins absolus. Préserver les versions précédentes ; exclure caches `.godot`, sauvegardes `.blend1` et environnements d'outils du ZIP final.
- Vérifier l'archive : CRC, présence EXE/PCK/GLB/sources/captures, liste SHA-256 et empreinte du ZIP. Garder les outils d'installation et vidéos AVI intermédiaires dans `work/`, pas dans les livrables.

## 10. Ordre de travail conseillé pour la prochaine zone

**Périmètre et interactions → volumes et caméra → éclairage/profondeur → silhouettes et matériaux → détails personnels → contacts et budget → captures/mouvement → pack portable.**

Créer une version séparée de la base utile. Choisir un budget et les points de vue d'inspection. Réutiliser les fonctions de construction et les contrats de noms, en séparant le contenu propre à la zone des systèmes de jeu. Ajouter uniquement les contrôles qui répondent aux risques de cette zone, puis livrer les preuves utiles et les sources reproductibles.

La rue, le diner, les personnages et la progression de sept jours ne sont pas réalisés par ce guide. Les acquis de la chambre doivent accélérer leur production, pas faire passer leur périmètre ou leur direction artistique pour déjà validés.

## 11. Où retrouver les preuves et sources

| Besoin | Fichier ou dossier |
|---|---|
| Fabrication de la chambre | `scripts/assets/build_room.py`, `hero_props.py`, `bag_lowpoly.py` |
| Textures et posters | `make_room_textures.py`, `prepare_poster_textures.py`, `assets/art/posters/` |
| Export et budget | `export_room.py`, `asset_geometry_checks.py`, `verification/geometry_budget.json` |
| Chaîne Blender des posters, historique V0.11 | `apply_poster_art.py`, `verification/historique_v011/poster_source_checks.json` |
| Géométrie des posters inchangée en V0.11, historique | `verification/historique_v011/poster_geometry_checks.json` |
| Moteur, lumière, QA | `game/scripts/room_review.gd` |
| Déplacement / collisions | `game/scripts/world/first_person.gd` |
| Météo / vidéos | `game/scripts/world/room_weather.gd`, `game/scripts/room_film.gd`, `game/scripts/room_computer_film.gd` |
| PC / OS fictif | `game/scripts/world/room_computer.gd`, `game/scripts/ui/cedar_desktop.gd`, `game/shaders/physical_crt.gdshader` |
| Audio fourni / boucle | `assets/audio_source/`, `scripts/assets/prepare_rain_audio.py`, `verification/rain_audio.json` |
| Lancement et construction | `JOUER.md`, `scripts/build_windows.ps1` |
| Vue de référence | `captures/01_porte.png`, `captures/camera_comparaison.json` |
| Évidence de livraison | `VERIFICATION.md`, `verification/delivery_checks.json` |
| Origine des exigences | Demandes actuelles du porteur de projet, `AGENTS.md`, décisions et vision dans `docs/` |

Les demandes ultérieures de l'utilisateur priment sur ce guide. Mettre à jour ce document après chaque zone en distinguant résultats observés, défauts encore présents et nouvelles décisions explicitement acceptées.

## 12. Écrans physiques et interfaces interactives

Un écran interactif doit rester attaché à sa surface 3D, avec perspective et occultations. La chambre utilise le plan I_pc_screen existant ; un SubViewport 640 × 480 affiche Cedar 03 et devient sa texture par ShaderMaterial. Aucun mesh ajouté et aucune fenêtre d’OS réel. L’interface fictive originale reprend les signes de 2003, avec ses propres icônes, couleurs et appellations.

À l’entrée, sauvegarder transformation globale et FOV de caméra, immobiliser le corps, cacher le HUD et interpoler la caméra devant le CRT pendant 0,7 seconde. Dans cette chambre : position Godot (−0,85 ; 1,19 ; −1,40), FOV 40°. Au retour, restaurer exactement la transformation sauvegardée et le FOV normal 62°, puis réactiver exploration et HUD. Ces valeurs dépendent de la position du CRT, pas des futurs écrans.

La souris reste capturée : les déplacements relatifs font avancer un curseur local borné à 640 × 480. Cloner les événements, remplacer leurs positions par les coordonnées du curseur puis utiliser SubViewport.push_input(event, true). Signaler notify_mouse_entered/exited ; les champs reçoivent leur focus dans ce viewport. Ne pas laisser les touches de saisie déplacer le personnage ni Échap ouvrir la pause pendant la fermeture du PC. Les applications réutilisent le Web local et l’état mémoire existants ; ne pas dupliquer leur logique dans l’OS.

Le viewport ne s’actualise en continu que pendant l’utilisation ; il conserve sa dernière image quand le joueur s’éloigne. Les tests passent par les événements du moteur, pas par l’appel direct aux callbacks de boutons. Attendre la mise en page des containers avant de mesurer leurs rectangles ; relâcher les boutons de molette aussi, sinon les clics suivants peuvent rester capturés par le défilement. La QA masque les entrées natives parasites et désactive l’accumulation d’événements pour stabiliser son parcours automatique ; le jeu accepte les entrées normales.

Contrôler séparément : matériau connecté, transition de caméra, icône, focus du champ, saisie, Entrée, recherche, ouverture de page, note dans le vrai état, menu Démarrer, carnet, réduction/restauration, glisser de fenêtre, corps immobile et retour de caméra. Une vidéo de l’OS doit montrer aussi le cadre physique et le retour à la pièce.

## 13. Audio de pluie fourni et boucle

Archiver le fichier utilisateur sans modification et consigner son empreinte ; le nom du fichier ne prouve pas une licence. La conversion de V0.12 décode le MP3 en mono 22 050 Hz, garde la séquence à partir de deux secondes et fond sa fin vers les deux premières secondes. La frontière finale rejoint ainsi deux échantillons adjacents de l’enregistrement d’origine. Appliquer un gain constant après le raccord, pas une normalisation dynamique susceptible de créer une variation au retour.

La boucle actuelle dure 35,656 secondes, avec crête −3 dBFS et volume de lecteur −2 dB. Conserver le WAV sans compression avec perte pour préserver ce raccord. Le rapport compare le saut de frontière à celui des mêmes échantillons adjacents dans la source, à l’arrondi PCM près : imposer arbitrairement un saut nul à du bruit de pluie ne décrit pas sa continuité réelle.

Vérifier le code de sortie du convertisseur **et** le nombre d’échantillons : un filtre FFmpeg avec branches courtes peut terminer sans erreur mais produire un fichier vide. Faire le raccord sur les échantillons décodés permet ici une vérification explicite. Les films du moteur doivent inclure une piste audio non silencieuse et se décoder intégralement. Attendre la fin effective de MovieMaker avant l’encodage MP4 ; un AVI encore ouvert peut donner une vidéo incomplète malgré un décodage réussi.

## 14. Densifier un extérieur sans abandonner le PSX — V0.13

La capture utilisateur montrait des arbres isolés, de grands trous dans la forêt et des traînées de pluie régulières. Ajouter des subdivisions aux arbres n’aurait pas corrigé leur répartition. La nouvelle composition utilise 90 arbres contre 44, sur trois bandes : 24 entre 16 et 25 m, 32 entre 27 et 42 m et 34 entre 43 et 62 m. Répartir horizontalement les arbres par intervalles puis varier leurs positions dans chaque intervalle évite les trous accidentels d’un tirage uniforme. Les hauteurs, inclinaisons et canopées restent irrégulières.

Les branches et couronnes doivent conserver une cohérence de hauteur lorsque le niveau de détail change. Réduire le nombre d’étages de feuillage sans recalculer leurs positions laisserait des troncs nus dépasser au-dessus des couronnes. Les pins utilisent trois plans croisés, les feuillus des canopées asymétriques sur plans croisés et des branches en rubans. Les textures comportent des masses et des trous de ciel, pas uniquement une accumulation de petits traits de feuilles.

Le sous-bois relie les troncs au sol. Deux grands plans de silhouettes ferment le fond de forêt à très faible coût, derrière les arbres qui fournissent la vraie parallaxe. La brume varie avec profondeur et hauteur ; elle sépare les plans sans éclaircir uniformément le premier plan. Le ciel couvert est un bruit lent quantifié et le sol humide un effet discret avec anneaux stylisés, sans promettre de réflexion de toute la scène.

Budget observé : 4 984 triangles intérieurs inchangés et 2 422 pour extérieur/ciel, total 7 406, plus les six triangles des trois plans de pluie. La passe ajoute 726 triangles par rapport à V0.12 et reste sous le plafond de travail 8 000. Densifier augmente aussi le remplissage alpha et les occultations : les triangles ne suffisent pas à mesurer le coût. Contrôler les draw calls et le temps d’image dans le vrai moteur.

**Approche historique, remplacée après le retour V0.14 (voir §16).** La pluie V0.12 répétait les mêmes espacements et longueurs par colonne. Utiliser une graine par cellule/goutte pour position, longueur, luminosité et épaisseur ; donner une échelle et une vitesse différentes à chaque profondeur. Garder une tête plus nette et une traînée effilée. Les grosses gouttes proches restent rares, les gouttes éloignées fines. Sur le verre, décaler les gouttelettes dans leurs cellules et limiter les ruissellements à des chemins irréguliers. Une capture fixe ne prouve ni vitesse ni mouvement : vérifier en vidéo avec des pauses de caméra et un déplacement latéral.

Les sept nouvelles textures sont déterministes, avec leurs propres graines, pour préserver les 45 textures existantes. La géométrie, UV, normales, indices, matériaux et transformations de 54 nodes intérieurs sont identiques ; les quatre exports d’accessoires et le son sont identiques par empreinte. La comparaison proche utilise une nouvelle capture de V0.12 intacte, avec la même caméra et le même temps météo. Suspendre la capsule pendant cette seule inspection évite un décalage provoqué par sa collision avec le CRT. Comparer les bases caméra avec une tolérance numérique explicite (ici 10⁻⁶), et préserver exactement position/FOV.

Résultat V0.13 : 63 contrôles moteur sans échec, 16 tests Python, reconstruction de 52 textures identique, trois films réels avec le son utilisateur : extérieur 16,10 s, chambre 21,10 s, PC 24,10 s. Sources de cette passe : scripts/assets/build_forest.py, prepare_forest_textures.py, game/shaders/rain_outside.gdshader, window_water.gdshader, outdoor_depth.gdshader, overcast_sky.gdshader et game/scripts/exterior_film.gd. Rapports : verification/forest.json, interior_preservation.json, texture_rebuild.json, delivery_checks.json et videos.json. Validation artistique laissée au porteur du projet.


## 15. Supports, dégagements et aménagement — retour V0.14

**Conserver un modèle inchangé ne prouve pas qu'il est bien placé.** La V0.13 conservait des défauts déjà présents : casque debout, évents séparés de la coque, accessoires suspendus, rideau traversant une boiserie et meubles avancés sans raison. Les empreintes et le compte de triangles n'évaluent pas les contacts. Regarder les appuis de face, de profil et en trois-quarts dans le moteur, à hauteur du joueur et en inspection rapprochée.

Exprimer les supports à partir de leur vraie géométrie. Le bureau est à Z 0,8125 m, le chevet à Z 0,6275 m et la commode à Z 0,9075 m, en coordonnées Blender. La hauteur du centre d'un objet n'est pas sa hauteur d'appui ; mesurer son minimum mondial après rotation et déplacement. Le livre, ses pages et son étiquette doivent partager la même transformation. Pour une pile, faire porter chaque élément par le précédent, sans ajouter des intervalles arbitraires. Autoriser des débords naturels de livres de tailles différentes, mais garder le centre et une surface suffisante portés. Ne pas confondre contact, débord et pénétration.

Préparer des assemblages complets avec coordonnées locales et ancrages : meuble, objets posés, fils, lumière et collisions. Un déplacement d'ensemble doit transporter tous ces éléments. V0.14 déplace le lit de (+0,15 ; +0,805 ; 0) m et le chevet de (+0,15 ; +0,615 ; 0) m en Blender ; la lampe et sa lumière suivent le chevet. Les poteaux gardent 1,25 cm devant la plinthe arrière et le chevet 7,5 cm devant le mur, marge cohérente avec ses débords et la plinthe. Vérifier l'espace contre le mur et la circulation en vue haute ; garder la caméra de référence identique pour comparer l'aménagement.

Un cadre incliné a besoin d'un appui réel, pas seulement d'une inclinaison. Le casque repose par ses deux coussinets sur le livre supérieur ; son arceau est couché et son fil tombe hors du bord. Les poignées rejoignent les façades, les câbles rejoignent leur appareil. Le tapis, le sac, les pieds et la cassette sont contrôlés contre le sol. Dans une corbeille, placer un fond intérieur et des papiers pliés portés par ce fond, sans couvercle qui traverse les objets ni gros cubes de papier flottants.

Contrôler le rideau contre **tous** ses voisins : appui, cadre, bureau et lampe. Déplacer seulement le tissu devant l'appui créait encore un contact avec le bureau ou la lampe. La solution retenue raccourcit son ourlet au-dessus de l'appui, resserre celui de droite et ajoute des attaches autour de la tringle ainsi que des supports de tringle. Ne pas ajouter des polygones pour cacher un mauvais placement.

Les évents du CRT sont désormais dans la texture de sa vraie face inclinée. Les barrettes à X constant flottaient car la coque se rétrécit avec la profondeur. Le retrait de dix cubes économise 120 triangles et évite toute séparation sous changement d'angle. Utiliser la géométrie pour les silhouettes et appuis ; employer une texture pour les gravures et fentes sous le pixel. Garder normales et filtrage cohérents avec le matériau principal.

Résultat contrôlé : 142 contacts avec tolérance de 1 mm, 13 paires d'assemblages sans intersection. Les coutures et joints structurels sont des raccords intentionnels ; ne pas imposer zéro intersection à des assemblages qui doivent se joindre. Les tests du sac, des touches et de la literie restent séparés. Les nombres décrivent les paires effectivement testées, pas une promesse qu'un test automatique remplace l'inspection visuelle.

## 16. La graine par cellule ne supprime pas une grille de pluie

Le conseil de V0.13 de varier chaque cellule était insuffisant : une goutte par cellule conserve une structure régulière et des phases voisines. V0.14 le remplace par 360 gouttes indépendantes réparties en continu dans trois volumes extérieurs, 100 / 120 / 140 selon profondeur. Chaque goutte possède sa phase, sa vitesse entre 4,8 et 8,7 m/s, son inclinaison, sa longueur et son opacité ; sa position de réapparition varie à chaque cycle individuel. Il n'existe plus de ligne ni de colonne de génération. Les trous et les petits regroupements sont naturels dans une distribution libre.

Les trois MultiMesh conservent peu de groupes de rendu, mais chaque goutte ajoute deux triangles. Compter **toute la géométrie runtime** dans le plafond : 7 250 modèle + 720 pluie = 7 970, cap de travail 8 000. Le modèle seul est 156 triangles plus léger que V0.13 ; le total avec pluie augmente, ce qui doit être dit explicitement. Les silhouettes PSX restent facettées. Les 52 textures de V0.13 et la géométrie extérieure sont préservées ; la 53e texture sert aux évents du CRT.

Vérifier la pluie à temps figé pour comparer, puis en mouvement avec une caméra fixe et un déplacement latéral. Contrôler une zone de fenêtre qui doit changer et une zone intérieure qui doit rester identique. Les quads doivent tous rester derrière l'ouverture. Une grille 10 × 10 d'analyse des positions constate ici des cases vides et d'autres contenant plusieurs gouttes ; cette grille est un outil de contrôle, pas un motif de rendu.

La mesure de performance doit aussi laisser la météo active : figer le temps retire le coût de mise à jour des gouttes et du feuillage. Ne pas lancer film, encodage ou Blender en même temps qu'une mesure présentée comme celle du jeu seul. La mesure V0.14 séparée, pluie et son actifs, observe 11,66 ms en moyenne et 15,73 ms au 95e percentile sur RTX 3050 Laptop, dans une seule vue. Elle ne décrit pas tout le jeu ni d'autres matériels. Un film à 30 images/s forcées vérifie le mouvement, pas les FPS interactifs.

## 17. Encodage, import et preuves de livraison

Lire et écrire les sources explicitement en UTF-8. Sous Windows, lire un fichier UTF-8 avec l'encodage système puis le réécrire en UTF-8 peut transformer un simple point médian en plusieurs caractères visibles au centre de l'écran. V0.14 répare les chaînes et ajoute un test de régression des sources, ainsi qu'une capture du HUD avec réticule et accents corrects. Éviter les réparations globales qui abîmeraient des chaînes déjà correctes.

Attendre la fin complète de Blender, puis réimporter le GLB et construire le PCK. Une importation commencée trop tôt peut conserver l'ancien modèle dans le cache tout en utilisant les nouveaux scripts. Comparer les comptes Blender / GLB / moteur et les empreintes export / runtime. Les noms automatiques Cone.064 ou Cone.066 peuvent changer sans modification de géométrie ; comparer les données des attributs, indices, UV, normales, matériaux et transformations, pas seulement ces noms.

Garder les anciennes vidéos identifiées dans un dossier historique. Les comparaisons doivent venir de deux scènes réelles, avec mêmes positions, cibles et FOV ; appliquer une tolérance explicite aux minuscules différences de matrice caméra. Une trajectoire de vidéo doit éviter de frôler l'écran ou de traverser un meuble même si sa physique est suspendue. Les captures rapprochées 25–31 et les deux films V0.14 complètent la vue de porte, qui masquait auparavant les défauts.

Sources à reprendre pour les prochaines zones : build_room.py, contact_checks.py, asset_geometry_checks.py, room_weather.gd et asset_contact_film.gd. Rapports : contact_checks.json, geometry_budget.json, rain_distribution.json, delivery_checks.json, texture_rebuild.json et videos.json. Les choix d'aménagement de cette passe répondent au retour utilisateur ; les suggestions de méthode restent des conseils, pas de nouvelles décisions de jeu validées.

Pour les comparaisons rapprochées, verrouiller aussi les entrées de regard avec le mode modal, pas seulement la physique. Un événement de souris reçu à l'ouverture peut changer la première vue entre l'orientation demandée et la capture. Sauvegarder les matrices **effectivement capturées** dans les deux versions et les comparer ; les mêmes paramètres d'entrée ne suffisent pas. Les six comparaisons V0.14 ont été recapturées ainsi depuis les PCK réels.


## 18. Recherche de matières réelles — pipeline officiel permanent

Pour toute nouvelle texture de matériau, employer `scripts/textures/pipeline.py` et lire `24_PIPELINE_TEXTURES_OFFICIELLES.md`. Vérifier d'abord le manifeste/cache puis rechercher automatiquement sur Poly Haven et ambientCG. Utiliser les vrais fichiers albedo/normal/roughness/AO depuis les métadonnées de téléchargement, jamais une vignette ou une prévisualisation comme texture finale. Décrire la surface et son ancienneté, éviter la répétition du même matériau partout, conserver les textures d'identité comme les posters et photos.

La résolution et le filtrage sont choisis par surface ; silhouette PSX et palette golden brown restent les repères. Pas de couleur chaude appliquée aux données de normale ou roughness. Une période UV connue en mètres évite des lames géantes ou un grain trop fin ; le composant `texture_library.gd` applique ce contrat sur une surface précise, sans nouveau polygone. Le premier essai réel a confirmé une période UV du sol de 1,8m face à une tuile source de 1,5m, soit une échelle de matériau de 1,2.

Ne pas confondre un classement API avec une appréciation de qualité ou un matériau seamless approuvé. Inspecter des répétitions 2×2 et le résultat dans Godot, puis enregistrer la capture et les réserves dans le manifeste. Le parquet d'essai conserve des joints/motifs et l'enduit des bandes répétées : emplois ciblés et contrôle de chaque surface, aucune substitution générale. Les essais de cette tâche sont temporaires et ne remplacent pas les matériaux de la chambre.


## 19. Parquet réel et réduction PSX — V0.15

Le parquet Poly Haven 256px plaît au porteur de projet ; il demande une résolution plus PSX. Comparaison réelle 256/128/64px : retenir 128px nearest avec mipmaps pour conserver les joints et le veinage, 64px perd trop de définition. La résolution ne change pas la taille physique du motif : conserver la tuile 1,5m, les UV à période 1,8m et leur facteur 1,2. Garder couleur et force normale identiques pour isoler le changement. Appliquer le matériau au seul sol après la préparation des meshes, qui force autrement nearest sur les matériaux importés. Ne pas intégrer un remplacement au GLB si une liaison de matériau explicite et reproductible suffit. Avant/après : caméra, FOV, heure météo et géométrie identiques ; enregistrer les matrices.

Vérification importante : nearest-with-mipmaps dans le matériau ne suffit pas. Forcer `mipmaps/generate=true` à l’import et vérifier `texture.get_image().has_mipmaps()` ; V0.15 possède réellement sept niveaux pour les maps 128px.


## 20. Étendre une texture validée sans uniformiser la pièce — V0.16

Le parquet 128px est validé et devient une référence à préserver. Choisir des sources par usage, puis comparer dans la lumière réelle : le premier acajou sombre produisait des bandes trop fortes ; un bois de meuble à grain fin le remplace. Ne pas confondre U et direction du grain : wood_table_worn suit U, wood_table_001 suit V. Un groupe fusionné peut contenir plusieurs densités UV ; employer une projection métrique ciblée sur ses faces existantes avec tangentes recalculées, sans déplacer les sommets ni changer les indices/collisions. Contrôler la petite quantification des normales lors du stockage GPU.

Pour la literie et les accessoires cousus, conserver coutures, motifs et boucles ; composer une trame de matériau réel avec cette identité et documenter les deux entrées. Réduire les quatre maps, renormaliser les normales, vérifier les vrais mipmaps. Ne pas appliquer un métal de ruine à des appareils domestiques, ni perdre les évents d’un CRT en remplaçant son atlas. Le comparatif avant doit garder toutes les décisions déjà validées, ici le parquet, et n’isoler que la nouvelle passe. V0.16 : neuf couples de vues, géométrie 7 970 triangles, vingt surfaces groupées. Détails dans le document 25.


Pour les matériaux émissifs, recopier aussi `emission_operator` lors d’un remplacement : conserver couleur, texture et énergie ne suffit pas. Le défaut ADD au lieu de MULTIPLY rendrait l’abat-jour excessivement lumineux sans toucher aux lampes de la scène. Le comparateur V0.16 contrôle cette propriété.


## V0.17 — Densité des détails et contraste des bois

Ne pas confondre résolution de texture et taille des pixels dans le monde : 128px sur 1,5m contre 0,55m produisent un écart de densité de 2,727. Comparer côte à côte les objets voisins, puis harmoniser les texels/m sans uniformiser leurs essences. Dix groupes de bois à 224 texels/m, contraste adouci, finitions sombres relevées ; parquet approuvé et 7 970 triangles conservés. Aucune acquisition réseau. Neuf avant/après depuis le PCK, avant V0.16 reproduit exactement, 82 contrôles runtime sans échec. Guide et commandes : document 26.


## V0.18 — Raccorder une zone à la campagne

Conserver le contrôleur visuel comme base réutilisable et ajouter un adaptateur de campagne, sans copier les règles sociales et d'enquête. Les scènes possèdent leurs vues, le noyau possède les faits et les coûts. Une session PC doit survivre à une fermeture : restaurer son état sans recommencer l'activité, puis consommer le créneau seulement à la sortie. Sauvegarder la pose d'exploration avant zoom, jamais remplacer le retour de caméra par la pose devant l'écran. Tester la reprise dans un autre processus, pas seulement dans un second objet mémoire. Donner un slot séparé à la campagne et aux tests ; préserver l'ancienne revue. Protéger les doubles actions et les chemins de fermeture de journal à la fin d'un lot. Dithering retenu : doux 32 niveaux/canal, Bayer 4×4 fixe dans les pixels monde, interface native indépendante. Les coûts d'activité et la sauvegarde ne prouvent pas encore une semaine ou une rencontre sociale jouable.


## V0.19 — Une interface diégétique ne doit pas facturer sa consultation

Lorsque le PC devient le centre de l'agenda et des notes, séparer entrer dans l'écran de commencer une activité de recherche. Une intention de planning ne doit pas déplacer le temps ou appliquer les effets ; l'action reste attachée à son objet physique. Le retour de caméra doit être identique pour consultation gratuite et recherche payante, mais seule cette dernière consomme un créneau. Persister l'ouverture du PC indépendamment de session.activity_id, sinon une sauvegarde pendant une consultation réapparaîtrait dehors. Garder pause/quitter et autosave indépendants du lieu. Montrer la confirmation d'une sauvegarde dans le CRT, pas dans un toast caché derrière lui. Pour les tests souris, attendre le layout des Control ; pour les captures, attendre le rendu imbriqué du SubViewport. Conserver une référence de revue indépendante pour vérifier que les changements de campagne ne cassent pas la physique et la pluie.
