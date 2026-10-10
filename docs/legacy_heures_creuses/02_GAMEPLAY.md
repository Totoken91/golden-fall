# 02 — Gameplay et boucle de Mystery Life Sim

## Principe de design

Reprendre de **Tokimeki Memorial 1994** : le temps limité, l'émergence des rencontres, l'interdépendance statistiques/relations, le calendrier d'événements, les conséquences différées et la rejouabilité. **Ne pas reprendre** les trois années, la mécanique exacte lundi-samedi/dimanche, la punition sociale à bombes telle quelle, les seuils personnages ou la nécessité d'une confession romantique finale.

## La vraie boucle

```text
JOUR / AGENDA
  -> choisir une action cohérente avec le temps disponible
  -> activité résolue rapidement OU entrée dans une zone 3D
  -> rencontrer / observer / discuter / enquêter
  -> mettre à jour compétences + énergie + mémoires sociales + indices
  -> traiter les événements planifiés et les conséquences
  -> soirée à la maison / PC 2003 / repos -> JOUR SUIVANT
```

Le mystère est le **fil rouge principal** ; chaque jour apporte de la vie ordinaire et parfois des anomalies. Le joueur doit pouvoir choisir une soirée légère, travailler ou creuser une piste. L'intrigue garde son propre calendrier ; elle n'attend pas que le joueur active un bouton « quête ».

## Calendrier proposé (prototype)

- Calendrier fictionnel final : **septembre–novembre 2003**, un automne. Pour rendre le 1er prototype contrôlable, écrire une séquence **de sept jours consécutifs**, intégrant au moins un week-end.
- Lundi–vendredi : cours auto-résolus en début de journée, possibles scènes spéciales ; **une action principale après les cours** ; possibilité d'interaction courte au domicile le soir, si non épuisé.
- Samedi/dimanche : **deux blocs** de temps (après-midi et soir). Certains événements occupent les deux.
- Une action représente une allocation temporelle significative, pas une promenade en temps réel. Une visite 3D débute une session, dont la sortie valide l'action. Un trajet de cinq minutes ne doit pas être répété quotidiennement.
- Les rendez-vous et invitations sont des événements horodatés, pas une obligation hebdomadaire.
- Pas de saisons alternatives à l'écran ; pluie/soleil/brume et heure du jour changent l'impression.

## Actions possibles à terme

| Action | Mode | Gain | Coût / dilemme |
|---|---|---|---|
| Étudier | résolution d'agenda | observation (parfois), progression scolaire éventuelle | temps, fatigue |
| Travailler en boutique | résolution d'agenda ou événement | argent, rencontre | temps, fatigue |
| Répéter à la guitare | résolution courte / événement | liens sociaux, culture locale | occupe la soirée |
| Marcher / se promener | 3D | humeur, rencontres, indices | temps, météo |
| Aller au diner | 3D | sociabilité, infos, liens | argent éventuel |
| Faire une recherche PC | 2D ordinateur | piste, documents, message d'ami | consomme un créneau du soir |
| Explorer la lisière | 3D | observation, preuves | fatigue, risque narratif |
| Se reposer | résolution rapide | fatigue/stress ↓ | renonce à autre chose |

Ne pas ajouter toutes les actions dès le 1er sprint. Garder des choix **comparables** avec coûts compréhensibles.

## États du joueur — hypothèse de test

**Compétences (0–100) :** sociabilité, observation, débrouillardise, endurance.  
**Ressources :** fatigue (0–100), stress (0–100), argent (dollars), objets/preuves (liste).  
**Mystère :** faits mémorisés, indices connus, hypothèses consultées, informations contradictoires ; **pas une jauge globale « horreur 73 % »**.

- Les quatre compétences ouvrent des options ou facilitent certaines actions. Elles **n'imposent pas une réponse** : le joueur doit interpréter.
- L'observation peut révéler un détail, pas résoudre automatiquement le problème.
- La sociabilité peut permettre une question délicate ; elle ne force jamais la romance.
- Une énergie faible réduit les sorties possibles. Ne pas punir par maladie arbitraire en semaine 1.
- Valeurs/deltas de `game/data/activities.json` **inventés pour test de rythme**, à ajuster après playtest.

## Relations, mémoire, initiative

Pour chaque PNJ important :

- `friendship` (amitié/proximité), `trust` (confiance), `resentment` (déception), `attraction` (optionnel, non obligatoire pour l'intrigue) ; le joueur voit surtout le **comportement**.
- `memories[]` : événements réellement vécus, cadeau, promesse, anecdote, observation, scène partagée.
- `schedule` : disponibilité et lieux plausibles selon créneau ; ne pas tout simuler en temps réel.
- `initiative` : PNJ qui écrit un message, invite, change de plan, ou refuse si occupé.
- `knowledge` : certains PNJ savent des faits que le joueur ignore ; ils ne doivent pas se transformer en bornes d'exposition.

### Exemple de causalité

Le joueur prend le temps de parler d'une cassette → mémorise `hannah_mentions_tape` → recherche un groupe sur le faux Web → découvre une coupure concernant Black Alder → possibilité d'une question ciblée à Hannah → sa réaction dépend de la confiance ET de ce qu'elle a dit auparavant.

### Refus de l'ancien système « bombe » à l'identique

Les gens peuvent se lasser, refuser une invitation ou vivre leur vie, mais le joueur n'a pas à entretenir systématiquement dix relations sous menace de pénalité en chaîne. Les conséquences doivent être **compréhensibles et proportionnées**.

## Enquête : observation, preuves, contradictions

- Chaque indice possède un ID stable ; le journal enregistre **comment** il a été obtenu.
- Une anomalie peut être signalée indirectement par deux données qui ne concordent pas (photo vs témoignage, blog vs souvenir, plan vs couloir).
- Le jeu ne colore pas chaque indice important en jaune et n'affiche pas systématiquement « INCOHÉRENCE DÉTECTÉE ».
- Une piste principale a au moins **deux voies d'accès** : dialogue OU Web, Web OU observation, etc. Éviter le soft-lock parce qu'un PNJ était absent.
- Événements de fond selon date + lieu + mémoire : certains peuvent être ratés, mais pas tous les chemins principaux.

## Progression finale envisagée (hors prototype)

Premier automne : installation, routine, découverte des disparitions, mystère local, crise, choix de quitter/rester/enquêter. Plusieurs résolutions locales, vérité globale partiellement ouverte. Romance et amitié influencent l'expérience mais ne remplacent pas le mystère.

## Principe anti-répétition

Une activité banale se règle en **quelques clics** et un feedback utile. N'ouvrir une scène 3D que si elle offre observation, choix, conversation ou atmosphère qui mérite d'être vécue. Un joueur qui travaille trois soirs peut accélérer le calendrier sans perdre le fil de l'histoire.
