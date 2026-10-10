**État courant V0.18 — démarrage du prototype, 9 octobre 2026.** L'utilisateur valide le dithering, puis autorise à commencer le prototype suivant les priorités recommandées. Variante douce retenue : Bayer 4×4 fixe dans les pixels monde 640×360, 32 niveaux par canal, amplitude 1. Parquet approuvé, bois 224 texels/m, palette et géométrie conservés. Première livraison de cette phase : socle de campagne dans la chambre actuelle, avec activités, CRT, notes, sauvegarde/reprise et sommeil. La journée sociale intégrée et les sept jours ne sont PAS encore livrés. Lire `docs/27_SOCLE_CAMPAGNE_V018.md` et le plan de lots ci-dessous ; ne pas confondre un état testé avec une approbation artistique.

La pause de progression pour revue visuelle est levée par la nouvelle demande. Les sept jours restent la cible P0. La V0.18 raccorde le parcours domestique seulement ; elle ne valide pas encore la rencontre, le trajet ou l’anomalie.

# 06 — Plan du premier prototype : de 7 jours à l'automne complet

**État V0.14 :** chambre PSX en première personne, PC physique, forêt/pluie/audio et passe de contacts livrés. La première journée avec agenda, relations, enquête et sauvegarde demeure dans la scène historique ; elle n'est pas encore raccordée à la chambre actuelle. Les sept jours ci-dessous restent une cible. Prochaine priorité recommandée : intégrer et vérifier une journée complète dans la présentation actuelle avant de développer la semaine. Cette recommandation n'est pas une commande d'implémentation ni une approbation artistique. État détaillé : `23_ETAT_PROTOTYPE_ET_PROCHAINES_ETAPES.md`.

## Principe : ne pas démarrer par 6 semaines

L'objectif immédiat est une **vertical slice de 7 jours jouables**, avec une vraie atmosphère et une conséquence observable. Ensuite seulement, 14 jours ; ensuite un acte de 6 semaines ; ensuite l'automne entier. « First playable » ≠ jeu complet.

## Cible P0 — une semaine jouable (première livraison Codex)

### Contenu obligatoire

- **Trois espaces 3D** très compacts : chambre du protagoniste (hub), segment de rue forestière, diner (même scène ou scène distincte).
- **Un personnage principal actif : Hannah** (modèle 3D temporaire cohérent et portrait illustré 2D de 2 expressions). **Eli et June :** données prêtes, interactions étendues plus tard ; ne pas créer 3 routes complètes en P0.
- **Calendrier :** une semaine de l'automne 2003 (jours exacts définis dans la scène d'essai), possibilité d'accomplir une action après les cours et plus le week-end. Avance temporelle visible et cohérente.
- **Activités :** au minimum étudier, diner, PC, repos, promenade. Effets simples mais persistants sur fatigue, observation/sociabilité, mémoire.
- **Dialogue à portrait 2D :** minimum deux variantes selon `met_hannah` / `hannah_mentions_tape` ; une décision à conséquence.
- **Journal :** mémoriser une information et la date ; revoir le souvenir ultérieurement.
- **PC 2003 :** écran CRT physique avec transition de caméra et souris sur un bureau 2D fictif d'époque ; champ de recherche, pages locales et résultats cliquables ; rechercher « black alder » ou « scierie » → accéder à une archive datée et enregistrer explicitement un indice dans le journal persistant.
- **Anomalie subtile :** après relation et/ou indice, silhouette lointaine visible sur la rue, ou reflet anormal dans la vitre du diner. Elle **ne poursuit pas** ; conséquence mémorielle : constat, doute, conversation alternative. La scène est préparée par le quotidien.
- **Save/load :** quitter puis reprendre conserve date, stats, relations, flags, indices et recherches.
- **Feedback visuel et sonore :** ambiance golden hour/pluie, vent discret et un son d'intérieur. Un prototype neutre gris sans ambiance ne valide pas la promesse.

### Chaîne jouable minimale souhaitée

```text
JOUR 1 : joueur dans la chambre ; agenda ; aller au diner ; rencontre avec Hannah
JOUR 2 : choix activité / retour chambre / ordinateur accessible
JOUR 3 : conversation avec Hannah ; souvenir de cassette ; proposition de recherche
JOUR 4 : Internet local ; découverte archive Black Alder ; ajout au journal
JOUR 5 : choix social OU recherche ; petit effet mesurable sur la confiance
JOUR 6 : visite de la rue au crépuscule ; anomalie lointaine conditionnelle
JOUR 7 : conversation sur ce qui a été vu, avec deux variantes ; fin de l'essai
```

**Important :** cette progression décrit des **possibilités et portes d'accès**, pas une chaîne forcée d'un événement par jour. Au moins une piste essentielle doit pouvoir être retrouvée si l'utilisateur manque la première occasion.

### Prototype d'événement : « Quelqu'un dans le jardin » — P1, PAS P0

Cette séquence est notre référence d'horreur majeure, **à réserver à la phase 14 jours ou 6 semaines** : nécessite maison d'un personnage, rapport émotionnel préalable, cadrage, silhouettes et branchements.

Situation : soirée dans la chambre d'un ami ; une silhouette identique à l'ami semble se tenir dehors ; l'ami revient de la cuisine et demande « Il est toujours là ? » sans avoir vu la fenêtre. Branches : regarder/ignorer/parler ; aucune explication ; souvenir et confiance mis à jour ; soupçon diffus persiste. Ne pas la transformer en jumpscare.

## Spécification de l'anomalie P0 — la rue

- Une silhouette humanoïde indistincte peut se tenir près de la forêt/du lampadaire **lors d'une soirée déterminée** après un ou plusieurs déclencheurs.
- Distance et mise en scène rendent la présence inquiétante mais pas grotesque. Pas de sourire/visage forcé.
- Lorsque le joueur la voit : il peut continuer, inspecter de loin ou rentrer. **Pas de combat et pas de chase.**
- L'événement n'est jamais un soft-lock ; une fois résolu, il est enregistré (`street_watcher_seen`) et le journal l'évoque sans certitude (« Quelqu'un près du virage ? »).
- Le lendemain, Hannah peut avoir un dialogue bref qui dépend de ce que le joueur raconte.

## P0 — contenu qui **ne doit pas** être implémenté

- Carte ouverte complète, montagnes et centaines de maisons, conduite de voiture.
- Quatre saisons, cycle météo simulation lourde.
- Romance complète, choix de partenaire, scènes amoureuses finales.
- Combat, arme, inventaire façon RPG, crafting, jauge de folie.
- Vraie navigation sur Internet, moteur de génération de pages par IA.
- Dix PNJ en routine complexe, arbres de dialogues géants.
- « Révélation » sur l'entité, boss, surnaturel spectaculaire.

## P1 — 14 jours jouables

- Ajouter June ou Eli en personnage relationnel, une invitation simple et un événement d'initiative de PNJ.
- Ajouter la maison de Hannah ou d'un ami, la scène « Quelqu'un dans le jardin » avec deux sorties, mémoires suivies et variantes de dialogue.
- Ajouter une seconde piste Web et une contradiction qui ne dépend pas du hasard.
- Mettre le calendrier à l'épreuve : journées où l'on ne peut pas tout faire, premier rendez-vous manqué possible avec conséquence équitable.

## P2 — acte de 6 semaines

- Trois personnages complets, 4–5 zones petites mais variées, magazine local, un concert ou une fête d'automne, un accès limité à la lisière forestière, 2–3 manifestations distinctes.
- Différencier au moins 2 parcours jouables ; un joueur curieux de l'enquête et un joueur très social ne doivent pas observer les mêmes dialogues.
- Un point culminant local avec résultat lié aux faits et relations, sans expliquer toute la Stillness.

## P3 — jeu complet ciblé

- Une seule saison, septembre–novembre 2003 ; densité et rejouabilité à valider après P2.
- Parcours social, enquête et temps limité ; cohérence globale de la mythologie ; choix de conclusion sans toute-puissance sur l'entité.

## Critère « on a notre jeu »

Un joueur testeur doit pouvoir décrire après vingt minutes : un lieu auquel il commence à s'attacher, au moins une personne qu'il distingue des autres, un souvenir qui a eu une conséquence, une information trouvée par lui-même, et un phénomène anormal qu'il n'est pas certain d'avoir compris.
