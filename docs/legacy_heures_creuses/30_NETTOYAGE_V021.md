# Nettoyage du code — V0.21

Demande utilisateur : auditer puis nettoyer le code hérité de Codex avant la rue et le diner. Aucun changement visuel ni de règle de jeu.

- `game/scripts/room_scene.gd` (RoomScene) : chambre partagée (vue 640×360, lumières, matières, pluie, joueur, PC, audio, entrées scriptées). `campaign.gd` (jeu) et `room_review.gd` (revue + QA + films) en héritent séparément ; le jeu n'hérite plus du code de test. Mode QA via `detect_qa_mode()` surchargé, plus de recalcul après coup.
- `autumn_ui.gd` réduit à l'invite, aux notices et aux panneaux : ancienne barre flottante, navigateur, agenda, carnet et dialogues supprimés (doublons du PC). Plus de recherche de bouton par son texte.
- Supprimés : prototype historique (`main.gd`, `main.tscn`, `world_builder.gd`, `actor.gd`), tests GDScript obsolètes, `texture_lab.gd`, `parquet_compare.gd` (non référencés). Les versions précédentes les conservent.
- `core/calendar_fr.gd` : dates en français calculées (« Mardi 14 octobre »), plus de dates écrites en dur dans le PC ; bornes du lot en constantes `FIRST_DAY`/`LAST_DAY`.
- `start_location` dans les données d'activité remplace le cas codé en dur du diner.
- Sauvegarde : un `activity_id` de mauvais type est refusé au lieu de planter.
- Lumière d'écran en double (V0.20) supprimée ; l'OmniLight `crt` d'origine suffit.
- Icônes, pointeur et zone de notification du PC dans leurs propres fichiers (`cedar_icon.gd`, `cedar_pointer.gd`, `cedar_tray.gd`).
- Données : `game/data/` devient la source unique ; le dossier racine `data/` est supprimé, validateur et tests Python pointent sur `game/data/`.
- Indentation par tabulations partout.

Non fait volontairement : animation de la pluie en shader (pluie validée, risque visuel), découpage des applications du PC en fichiers séparés.

Vérification : 151 contrôles moteur (PC 69 en quatre processus + chambre 82), zéro échec ; 31 tests Python OK. PCK SHA256 1d7c6a861ed9a979cab040e14b6eec44744491ad54b52b9a73f0bef7ac9cf091.
