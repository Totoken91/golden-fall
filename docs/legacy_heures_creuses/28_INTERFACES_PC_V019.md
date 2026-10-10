# Le PC comme centre des interfaces — V0.19

## Demande et comportement

L'utilisateur accepte la proposition de regrouper agenda, journal et sauvegarde sur le PC, avec pause et sauvegarde automatique indépendantes. Trois applications dédiées dans Cedar 03, accessibles par icônes et menu Démarrer ; elles emploient les fenêtres existantes, la souris physique et la même transition de caméra. Aucune nouvelle géométrie ou texture de chambre. Dithering doux, parquet et matériaux V0.18 inchangés.

Ouvrir le PC, l'agenda, le journal ou la sauvegarde ne consomme rien. L'agenda montre la date, le créneau et l'intention courante. Prévoir une activité enregistre `planned_activity` sans appliquer d'effet ni avancer l'horloge. Étudier se fait avec E sur les cahiers du bureau ; repos et sommeil avec E sur le lit. Accomplir une activité efface l'intention. Le planning reste une aide, pas une obligation de suivre le choix inscrit.

CedarSearch présente un bouton explicite « Commencer une recherche · soirée ». Ce bouton seul appelle l'activité `computer_research`, applique son coût une fois, puis ouvre la recherche locale. Avant la soirée et après son utilisation, le navigateur ne peut pas démarrer une nouvelle recherche. Une session en cours continue normalement. La lecture de l'archive et la note explicite gardent leur contrat précédent.

Sortir du PC termine une recherche active et consomme le créneau ; sortir d'une consultation sans activité ne change ni stats ni créneau. Une consultation reste possible en fin de soirée et depuis le journal de fin de lot. La date/horloge Cedar suit l'état du jeu plutôt qu'un texte figé au lundi soir.

## Sauvegarde et menus

Application Sauvegarde : bouton dédié et confirmation/erreur dans la fenêtre physique. F5 à l'intérieur du CRT appelle la même action et ouvre son retour visible. F5 hors PC ne sauvegarde pas manuellement ; il indique que la commande se trouve sur le PC. Autosave après activité, planification, consultation, fin de session, sommeil, retour au titre et fermeture. Slot conservé `user://campaign_day_v1.json`, distinct de l'historique. Aucun fichier joueur utilisé par les tests.

La barre flottante est masquée dans toute la campagne, y compris pause et interactions. J/Tab n'ouvrent plus les gros panneaux de gestion dans la chambre. Échap donne une pause indépendante avec reprendre, son, retour au titre et quitter ; le chargement et la nouvelle partie restent sur l'écran titre. Il faut pouvoir quitter même loin du PC. Un petit carnet consultable dans les futures zones demeure à décider lors de leur intégration ; il n'existe pas encore de zone extérieure courante.

## Persistance et compatibilité

Même `LifeState`, `WebArchive`, `SaveManager` ; pas de copie des notes dans l'OS. `campaign_desktop` ajoute `pc_open` et la liste blanche d'applications ouvertes. La reprise distingue une consultation libre d'une session payante : chacune réouvre le PC et les applications, sans rappeler `start()`. Les anciennes sauvegardes sans ces champs conservent le fallback de recherche active ; aucune migration du slot historique. Position/yaw/pitch restent ceux de l'exploration avant zoom.

Fenêtres restaurées avec leurs positions par défaut ; pile Retour et positions/minimisations ne sont pas persistées. La sauvegarde de l'application elle-même est une interface sur le même slot, pas une disquette ou un inventaire supplémentaire. Un format de sauvegarde refusé ne remplace pas l'état vivant.

## Vérification

`scripts/qa/pc_hub_check.gd`, quatre processus successifs : seed, free_resume, paid_resume, end. Variables `LHC_QA_DIR`, `LHC_CAMPAIGN_SAVE` et `LHC_CAMPAIGN_STAGE`, argument `-- --campaign-check`. Tests : absence de barre et panneaux de gestion externes, PC après les cours gratuit, clic réel sur Agenda, intention sans coût, clic réel sur sauvegarde et retour visible, reprise gratuite, sortie gratuite, étude physique, recherche explicitement payée et unique, note explicite/dédupliquée, F5 dans le CRT, reprise payante, journal tardif gratuit, sommeil, journal de fin sur PC, état final persistant, refus d'un chargement invalide et parcours repos.

Les clics attendent la disposition des Control avant de mesurer leurs rectangles ; sinon le test viserait une position provisoire. Les captures attendent plusieurs frames pour que le SubViewport du CRT soit réellement redessiné. Le retour caméra se contrôle au terme du tween, avant que la physique du corps reprenne : une pose encore légèrement au-dessus du sol peut ensuite se poser sans constituer une erreur de transition.

La suite de revue vérifie indépendamment les commandes souris/clavier de l'OS, les collisions, la pluie, le budget et les textures. Nombres exacts et hash du PCK dans `verification/pc_hub_summary.json`. Les tests V0.18 archivés sont historiques ; utiliser le nouveau script pour ce contrat. Le prototype reste borné à la journée domestique ; aucune semaine ou rencontre sociale ajoutée dans cette tâche.
