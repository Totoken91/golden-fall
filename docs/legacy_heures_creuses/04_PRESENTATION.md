# 04 — Présentation exacte : 2D, 3D, dialogues et caméra

**Actualisation V0.14 :** première personne et PSX constituent la direction courante. Le CRT est physique et interactif. La chambre de revue existe ; les autres espaces et le parcours de campagne décrits ici restent à intégrer dans cette présentation. Voir `23_ETAT_PROTOTYPE_ET_PROCHAINES_ETAPES.md`.

## Décision ferme

**Hybride encadré, pas patchwork.** Un seul monde 3D, avec des surfaces 2D diégétiques ou superposées : agenda, choix de dialogue, portraits, journal, ordinateur. Le jeu n'alterne pas entre deux univers visuels incohérents.

## Matrice des modes

| Situation | Décor | Personnage | UI | Contrôle |
|---|---|---|---|---|
| Choisir l'activité de l'après-midi | panneau 2D calendrier / chambre 3D en arrière-plan | — | agenda papier / encarts sobres | souris/clavier, rapide |
| Rue / diner / intérieur | zone 3D low-poly PSX | PNJ 3D low-poly | interaction minimale | 1re personne |
| Conversation sociale majeure | **même décor 3D** cadré | PNJ 3D visible | portrait **2D illustré** + dialogue / choix | sélection réponses |
| Conversation anormale | même décor 3D | PNJ 3D | souvent sous-titres sobres, **sans règle systématique** | dialogue + observation |
| Inspection d'objet | 3D avec caméra rapprochée | main/objet facultatif | libellé discret / journal | rotation, zoom simple |
| PC de 2003 | chambre 3D → caméra devant le CRT physique | — | bureau 2D fictif, navigateur/archives | souris sur écran, saisie texte |
| Journal | carnet 2D | — | souvenirs et preuves | consultation |

**Pourquoi les portraits ?** Expressivité et coût maîtrisé ; permet une écriture relationnelle soignée sans animation faciale haut de gamme. **Pourquoi les PNJ 3D ?** Silhouettes réelles dans le lieu : l'horreur naît des comportements et distances.

## Exemple de dialogue social

1. Le joueur entre dans le diner 3D, Hannah est assise à la table près de la fenêtre.
2. En s'approchant, une invitation discrète : « Parler à Hannah ».
3. La caméra s'immobilise avec un cadrage suffisamment beau pour laisser exister pluie et vitres.
4. Son portrait 2D semi-réaliste, dessiné avec une texture cohérente à 2003, apparaît en marge (ne pas recouvrir son visage 3D ou la zone d'anomalie).
5. Texte et jusqu'à trois options (souvent deux suffisent), variantes selon les souvenirs ; ne pas afficher +5 amitié.
6. Fin de dialogue → la caméra et le contrôle retournent au même état ; le journal peut recevoir un souvenir si événement significatif.

### Cas horreur

Certains dialogues se font sans portrait, plus près du corps du personnage, avec sons spatialisés, mais **ne pas rendre l'absence de portrait synonyme garanti de danger**. L'interface peut rester « normale » alors qu'une mémoire diverge.

## Caméra et mouvements

- Vue **première personne** à hauteur humaine, vitesse de marche tranquille. Contrôle adapté à l'observation et aux interactions quotidiennes.
- Zone 3D de taille modeste ; plan composé et légère profondeur de champ si le budget performance permet.
- Les silhouettes lointaines doivent rester lisibles sans être grotesques ; budget d'éclairage sur le feuillage, le brouillard, les fenêtres et les lampes sodium.
- Intérieurs : conserver le regard libre en exploration ; cadrages temporaires pour interactions, avec retour cohérent à la position précédente.
- Inspection locale à la première personne/zoom autorisée si cela améliore la lecture ; pas une boucle FPS distincte.

## UI non négociable

- Bois tabac, ivoire délavé, brun foncé, cuivre et gris papier ; typographie sobre, hiérarchie claire.
- HUD minimal en exploration : texte « Interagir » et accès agenda/journal, pas de HUD de survival horror.
- Menus rapides, entrée/sortie immédiates, navigation clavier/souris (manette possible plus tard).
- In-game screen 16:9 recommandé, éviter panneaux géants au milieu du champ visuel.
- Filtres rétro optionnels, doux ; **ne pas masquer le texte** ni dégrader volontairement lisibilité/contraste.
- Options : vitesse du texte, réduction tremblement / effets de caméra, sous-titres, réglage d'ambiance sonore.

## Prototype des écrans clés

**Écran 1 : chambre 3D (hub)** — pluie et feuillage visibles, bureau avec CRT, lit, poster, petite pile de CD, lampe chaude. Accès agenda, repos, PC, porte vers carte.  
**Écran 2 : agenda 2D** — jour + heure fictionnelle, deux ou trois activités significatives, coût/effet indiqués qualitativement.  
**Écran 3 : rue 3D** — trottoir, feuilles, magasin/diner, silhouette d'un habitant, signalétique crédible.  
**Écran 4 : diner 3D** — PNJ 3D, un échange avec portrait 2D et conséquence mémorisée.  
**Écran 5 : PC physique** — transition vers le CRT, bureau Cedar 03 avec souris, navigateur avec saisie texte, résultats et liens ; retour à l'exploration en quittant le PC.  
**Écran 6 : journal 2D** — photographies, dates, souvenirs, faits et pistes, sans révéler les variables cachées.

## Réduire les animations sans rendre le jeu mort

2–3 animations universelles (idle, marche, s'asseoir), gestes légers, regard vers une fenêtre, déplacement d'une tasse. Les gros événements utilisent cadrage et montage, pas la quantité d'animations.
