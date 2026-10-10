# Écran du PC lisible et Cedar 03 mi-2000 — V0.20

Demande utilisateur : le PC était illisible ; améliorer l'OS, la visibilité de l'écran, son ambiance et son interface, dans un esprit nostalgique milieu des années 2000.

Cause de l'illisibilité : le bureau 640×480 était rendu sur le tube 3D, puis tout le monde 3D réduit à 640×360 et tramé (Bayer). Une fois zoomé, le texte passait par ~300 px de haut avant d'être agrandi.

## Changements

- `room_computer.gd` : à la fin du zoom, le bureau est affiché en pleine résolution dans un `CanvasLayer` posé exactement sur la projection du tube (boîte englobante de la surface `screen`, recalculée chaque image). Fondu d'entrée 0,28 s, de sortie 0,18 s. Une fois le fondu terminé, le tube 3D passe en verre sombre (`covered` dans `physical_crt.gdshader`) pour qu'aucune image basse résolution ne transparaisse. Dithering et monde 640×360 inchangés ; seule l'interface du PC zoomé sort du filtre, comme l'interface native.
- `crt_overlay.gdshader` : courbure légère, lignes de balayage verrouillées sur les 480 lignes, halo de phosphore, grille d'ouverture, barre de ronflement lente, scintillement secteur, vignettage et reflet froid. Volontairement discret pour garder le texte lisible.
- `cedar_desktop.gd` : refonte visuelle originale (pas de copie d'un OS existant). Fond d'écran peint en shader (`cedar_wallpaper.gdshader`, crête boisée au crépuscule ambre), barre des tâches et barres de titre brillantes (`cedar_gloss.gdshader`), bouton « démarrer » ambre, fenêtres encadrées avec ombres portées et état actif/inactif, icônes redessinées, zone de notification (son, connexion, horloge), bulles de notification (note ajoutée, sauvegarde), curseurs flèche/main/texte. Navigateur : menus, Précédent/Accueil, barre d'adresse, barre CedarSearch, liens bleus, URL vertes, barre d'état « Connecté · 56 Kbit/s » avec chargement. Agenda avec jour de la semaine et jauges ; journal sur papier à marge ; sauvegarde avec disquette et confirmation.
- `pc_audio.gd` : sons synthétisés (aucun fichier) : ronflement du tube, clics souris, touches clavier, carillon des bulles. Suivent l'option son existante.
- Légère lueur du tube sur le bureau (`CrtGlow`, OmniLight sans ombre, faible portée).

Positions des icônes, de la barre des tâches, du menu Démarrer et des fenêtres conservées : les tests historiques utilisent des coordonnées physiques. Noms de nœuds et contrats V0.19 inchangés (consultation gratuite, recherche explicite, note explicite, F5).

## Vérification

148 contrôles, zéro échec : `verification/v020_pc_hub.log` (66, quatre processus) et `verification/v020_room.log` (82). Galerie : `captures/os_cedar_v020/index.html`, captures des PCK V0.19 et V0.20 avec `scripts/qa/pc_gallery_capture.gd` (même script, même météo figée).

## Retour de jeu : freeze et recherche perdue

Retour utilisateur : freezes ponctuels pendant une recherche du soir, puis CedarSearch n'offrait plus de recherche. Sa sauvegarde montre repos après les cours, recherche commencée en soirée, aucune requête enregistrée, puis créneau « Fin de soirée » : la sortie du PC a, comme prévu depuis V0.19, terminé la soirée de recherche.

- Quitter le PC (Échap ou menu Démarrer) pendant une recherche payante demande maintenant confirmation : « Continuer à chercher » / « Terminer la soirée ». Échap ferme la boîte. La revue indépendante et les sorties scriptées restent directes.
- La page CedarSearch indique pourquoi la recherche est indisponible (pas encore le soir, soirée déjà utilisée, trop tard, journée terminée).
- `frame_watch.gd` (hors QA) note dans `user://logs/godot.log` chaque image > 60 ms avec temps script, physique, rendu CPU/GPU et contexte. Les sondes `scripts/qa/frame_probe.gd` et `pc_input_probe.gd` n'ont pas reproduit de freeze durable (≈ 7 ms par image) ; seul gel mesuré : compilation des shaders au premier lancement après export (≈ 2,4 s), mise en cache ensuite. Les sons synthétisés ont été mesurés à ≈ 0,1 ms par appel.

QA : 151 contrôles, zéro échec (deux contrôles ajoutés pour la confirmation).
