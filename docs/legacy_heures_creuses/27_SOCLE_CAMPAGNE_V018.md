**Actualisation V0.19 :** ce document décrit le lot V0.18. Les commandes J/Tab/F5 hors PC et l'agenda externe sont remplacés par les applications Cedar ; consulter le PC ne démarre plus la recherche. Voir le document 28 pour le contrat courant. Les coûts du noyau, la borne du premier jour et la séparation du slot historique sont conservés.

# Socle de campagne dans la chambre — V0.18

## Périmètre

Nouvelle demande : garder le dithering et commencer le prototype par les priorités recommandées. Premier lot livré : après les cours → étude/repos → soirée → CRT/recherche/note explicite → fin de soirée → sommeil → lendemain/fin du lot. Une sortie anticipée par le sommeil reste possible après la première activité. Ni la rencontre sociale, ni les nouvelles zones, ni la semaine ne sont encore livrées. La porte informe de la limite de cette version.

## Architecture

`campaign.tscn` devient le point d'entrée, avec `campaign.gd` qui hérite du contrôleur de chambre pour conserver construction, collisions, pluie, matériaux et ordinateur physique. Il branche les interactions domestiques aux mêmes `LifeState`, `ContentDB` et `WebArchive` que le prototype historique. Les scènes futures doivent recevoir ce même état ; aucune copie locale des relations/flags/clues. `room_review.tscn` et `main.tscn` restent séparées pour la revue et l'historique.

Pas de changement du moteur de règles historiques dans cette étape. `LifeState.start()` vérifie la disponibilité et applique les effets ; les actions rapides finissent immédiatement. La recherche coûte au début, et le créneau avance seulement à la sortie du CRT. Un verrou de même frame empêche les doubles appels rapides ; un PC actif ou en transition refuse de redémarrer une activité. Le retour de caméra utilise la transition existante puis termine la session une seule fois. `finish()` sans session est idempotent.

La borne de sommeil historique est conservée explicitement : elle termine au lendemain. Le futur calendrier de sept jours doit être développé avec les événements et dialogues, pas en retirant seulement `completed=true`.

## Sauvegarde

Slot utilisateur `user://campaign_day_v1.json`, distinct du slot historique `first_day_v2.json`. Écriture temporaire puis remplacement via SaveManager. `campaign_id=home_day_v1` distingue le contrat de cette étape. Autosave à la nouvelle partie, après action, sortie CRT, sommeil et fermeture ; F5 disponible même dans l'OS physique. Un échec d'écriture est affiché. Une nouvelle partie depuis une session ou avec un slot existant demande confirmation de remplacement dans le jeu.

État sauvegardé : date, créneau, stats, relations, flags, indices, souvenirs datés, pages visitées, recherches, session, journal d'activités ; position/yaw/pitch d'exploration ; page et requête CRT ainsi que présence du navigateur/carnet. Le chargement restaure la session directement sans rappeler start(), donc sans repayer. La caméra sauvegardée est celle de l'exploration, pas celle du zoom PC. La validation se fait dans un candidat avant remplacement de l'état courant ; format, date, lieu, activité et valeurs de position/rotation sont contrôlés.

Limites assumées : un slot, deux fenêtres restaurées avec leur placement par défaut ; la pile Retour et les positions des fenêtres ne sont pas sérialisées. Pas de migration automatique d'une sauvegarde historique vers cette campagne. Pas de sauvegarde future rue/diner tant que ces scènes ne sont pas raccordées.

## Dithering accepté

Shader `room_pixels.gdshader` issu de l'essai doux : Bayer fixe 4×4, 32 niveaux RGB par canal, amplitude 1. Trame à 640×360, puis agrandissement nearest. L'interface native reste hors du shader ; l'écran du CRT, qui appartient au monde, est filtré. Aucun bruit animé ajouté. Le parquet, les fichiers des matières, la lumière et les modèles V0.17 sont conservés. Inspiration console ancienne, sans assertion de simulation matérielle exacte.

## Vérification et reproduction

`scripts/qa/campaign_check.gd` est exécuté depuis le PCK final, successivement dans trois processus : seed / resume / end. `LHC_QA_DIR` donne le dossier des captures ; `LHC_CAMPAIGN_SAVE` un fichier isolé dans ce dossier ; `LHC_CAMPAIGN_STAGE` la phase. Passer `-- --campaign-check`. Le chemin de test n'est accepté qu'en mode QA. Les tests ne touchent pas au slot du joueur.

Contrôles : menu verrouillé, activité refusée sans coût, effets et créneaux, double action, entrée CRT unique, recherche, pas d'indice automatique à la lecture, bouton de note explicite, déduplication, F5 dans le CRT, reprise réelle, absence de coût supplémentaire, page/carnet, retour exact de caméra, sortie de session idempotente, sommeil unique, reprise terminale, journal terminal, sauvegarde invalide refusée sans modifier l'état courant, parcours repos/sommeil et remise à zéro du bureau. Les captures sont des rendus Godot. La suite de chambre vérifie séparément collisions/raycast/WASD, pluie et gestes souris/clavier du CRT.

Résultats, nombre exact de contrôles et hash PCK dans `verification/campaign_summary.json`. Captures actuelles : `captures/campagne_v018/index.html`. Les autres médias sont historiques. Les tests sont des parcours techniques automatisés ; ils ne constituent pas une validation de la semaine ni un test narratif par un joueur.
