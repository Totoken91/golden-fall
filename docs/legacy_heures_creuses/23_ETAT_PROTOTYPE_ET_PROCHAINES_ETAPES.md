**V0.19 — interfaces regroupées sur le PC, demande utilisateur autorisée.** Agenda, journal et sauvegarde manuelle sont des applications Cedar 03 accessibles sur le CRT physique. Consultation gratuite à tous les créneaux ; la recherche est une activité explicitement commencée dans CedarSearch. L'agenda enregistre une intention sans exécuter l'activité ; étude au bureau, repos/sommeil au lit. Aucune barre flottante Agenda/Journal/Sauvegarder, aucun panneau de gestion via J/Tab dans la chambre, aucune sauvegarde manuelle dans la pause. Échap conserve pause, son, retour au titre et quitter ; le titre conserve nouvelle partie/chargement. Autosave conservée. F5 dans le CRT ouvre la sauvegarde avec retour visible, hors CRT il indique où la trouver. Un petit carnet hors de la chambre reste une possibilité pour les futures zones, pas une fonctionnalité déjà livrée. Lire `docs/28_INTERFACES_PC_V019.md`.

Cette passe modifie les interfaces et la séparation consultation/recherche, sans ajouter rue, diner, Hannah ou jours. Les priorités de contenu ci-dessous restent actives.

# État et priorités — V0.18

Le porteur de projet valide le dithering et demande de commencer le prototype complet. Première priorité implémentée : un socle domestique réellement persistant, plutôt que de continuer les passes décoratives.

| Élément | État vérifié |
|---|---|
| Chambre PSX, parquet et bois harmonisés | Conservés ; 7 970 triangles. Dithering doux choisi après essai et validation utilisateur du dithering. |
| Activités de chambre | Étudier / repos : coûts et effets une seule fois, créneau après les cours → soirée. PC : soirée → fin de soirée à la sortie. |
| PC physique et enquête | Même CRT avec transition et souris ; archives locales, ajout explicite d'indice, mémoire datée. |
| Sauvegarde campagne | Slot dédié, autosave nouvelle partie/activité/fin/sommeil/fermeture et F5. Reprise dans un nouveau processus, y compris session CRT et page en cours. |
| Sommeil | Passage au 14 octobre et écran de fin du premier lot. Ne débloque pas six journées sans contenu. |
| Relations / dialogues | Systèmes historiques conservés ; non accessibles dans le parcours chambre courant. |
| Rue, diner, Hannah | Prochain lot. La porte du parcours courant ne simule pas une sortie fonctionnelle. |
| Semaine / anomalie | À implémenter et à mettre en scène. |

## Ordre de travail restant

1. Construire rue courte et diner dans la direction PSX, en réutilisant le pipeline officiel des matières, les budgets et contrôles de contact. Hannah 3D cohérente, animations minimales et portrait à deux expressions. Raccorder les scènes au même état et à un retour de porte fiable. Ne pas annoncer une journée intégrée complète avant la rencontre et ses conséquences.
2. Raccorder le choix social, sa mémoire et les effets observables ; conserver session et position lors d'une reprise entre zones. Tester deux choix contradictoires sans récompense automatique de relation.
3. Étendre réellement à sept jours. Horloge en données, dialogue qui varie, piste récupérable si le joueur rate une occasion. Remplacer la borne de sommeil du premier lot seulement avec cette extension.
4. Anomalie distante conditionnelle dans la rue, sans poursuite ; doute écrit et conversation différente ensuite.
5. Parcours P0 complet : nouvelle partie, choix sociaux/enquête différents, sauvegardes entre lieux/jours, aucun blocage, build autonome et preuves moteur.

## Condition de prototype complet

Sept jours jouables et reprenables, chambre/rue/diner cohérents, Hannah avec choix et conséquence, archive trouvée par recherche et notée volontairement, anomalie ambiguë avec conséquence ultérieure. V0.18 est un socle utile, pas ce résultat complet.

Voir le document 27 pour les contrats et les tests de cette première étape. Les observations V0.14 restent dans les versions précédentes.
