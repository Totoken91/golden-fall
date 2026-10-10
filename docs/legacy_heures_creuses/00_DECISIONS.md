**V0.19 — interfaces regroupées sur le PC, demande utilisateur autorisée.** Agenda, journal et sauvegarde manuelle sont des applications Cedar 03 accessibles sur le CRT physique. Consultation gratuite à tous les créneaux ; la recherche est une activité explicitement commencée dans CedarSearch. L'agenda enregistre une intention sans exécuter l'activité ; étude au bureau, repos/sommeil au lit. Aucune barre flottante Agenda/Journal/Sauvegarder, aucun panneau de gestion via J/Tab dans la chambre, aucune sauvegarde manuelle dans la pause. Échap conserve pause, son, retour au titre et quitter ; le titre conserve nouvelle partie/chargement. Autosave conservée. F5 dans le CRT ouvre la sauvegarde avec retour visible, hors CRT il indique où la trouver. Un petit carnet hors de la chambre reste une possibilité pour les futures zones, pas une fonctionnalité déjà livrée. Lire `docs/28_INTERFACES_PC_V019.md`.

**État courant V0.18 — démarrage du prototype, 9 octobre 2026.** L'utilisateur valide le dithering, puis autorise à commencer le prototype suivant les priorités recommandées. Variante douce retenue : Bayer 4×4 fixe dans les pixels monde 640×360, 32 niveaux par canal, amplitude 1. Parquet approuvé, bois 224 texels/m, palette et géométrie conservés. Première livraison de cette phase : socle de campagne dans la chambre actuelle, avec activités, CRT, notes, sauvegarde/reprise et sommeil. La journée sociale intégrée et les sept jours ne sont PAS encore livrés. Lire `docs/27_SOCLE_CAMPAGNE_V018.md` et le plan de lots ci-dessous ; ne pas confondre un état testé avec une approbation artistique.

# 00 — Décisions, statut et arbitrages

**État au 9 octobre 2026 — V0.14 :** la direction courante est **première personne / PSX / golden brown**, avec formes anguleuses, détails portés par les textures, éclairage localisé et extérieur pluvieux gris. Le CRT est un écran physique interactif avec transition de caméra vers l'OS fictif Cedar 03. La veste est retirée. La chambre actuelle reste une scène de revue séparée de la première journée historique : les sept jours ne sont pas encore jouables. Voir `23_ETAT_PROTOTYPE_ET_PROCHAINES_ETAPES.md` pour l'état réel et les priorités proposées. Les paragraphes V0.7/V0.8 ci-dessous retracent les demandes antérieures ; ils ne constituent pas l'état de livraison actuel.

**V0.8 — demande actuelle :** conserver la scène et le cadrage V0.7, faire une passe ciblée d'extérieur/lumière/matières/literie/manteau, animer la pluie extérieure, ajouter quelques détails personnels, livrer comparaison au même angle et courte vidéo du moteur. Cette demande ne constitue pas une approbation anticipée du résultat de la passe.

**V0.7 — direction actuelle :** le pack PSX fourni après rejet du rendu V0.6 demande une exploration en première personne et une esthétique PSX texturée. `21_REORIENTATION_VISUELLE_PSX.md` remplace les mentions antérieures de caméra troisième personne/PS2 ci-dessous pour l'étude de chambre. Les captures V0.7 sont une proposition à examiner, pas un style accepté par l'utilisateur. La progression de sept jours est suspendue pendant cette revue visuelle.

## VALIDÉ — ne pas modifier sans demande explicite

- **Titre de travail :** Les Heures Creuses.
- **Genre :** **Mystery Life Sim** ; le mystère et le mood passent avant la romance. On ne construit pas trois jeux séparés.
- **Cadre :** petite ville du Nord-Ouest américain, en **automne 2003**.
- **Durée fictionnelle visée :** **un automne unique**. Pas d'hiver, printemps ou été à produire.
- **Stillness Continuum :** la ville donne l'impression de vivre dans un automne suspendu, coupée du reste du monde ; exploiter l'idée sur le plan narratif ET production. Le fonctionnement exact reste mystérieux.
- **Esthétique :** **Golden Autumn Gothic** ; rouille, ambre, brun doré, jaune tungstène, vert sapin, ciel gris chaud. Twilight pour la sensibilité mélancolique/forestière, **pas la teinte bleue**.
- **Culture :** début des années 2000, grungecore, vêtements usés, folk/slowcore/rock alternatif, CRT, vieux Web, CD, appareils photo numériques.
- **Horreur :** omniprésente comme tension ; disparitions + phénomènes de mémoire/imitations liés à une présence présumée dans la forêt.
- **Nature de la présence :** **ambiguë**. Même l'enquête avancée ne doit pas tout expliquer.
- **Présentation :** mélange 2D/3D. Monde et PNJ 3D low-poly PSX, exploration à la **première personne** ; dialogues sociaux importants avec **portraits 2D dessinés** sur décor 3D ; agenda et journal en 2D, bureau et navigation Web affichés sur le CRT physique interactif.
- **Internet 2003 :** navigation et recherches crédibles sur le PC domestique ; recherche réellement utilisable dans un Web fictif local.
- **Production :** fournir un dossier réutilisable par Codex et extensible vers le jeu final, pas seulement une démo jetable.

## CANDIDATS FORTS — adoptés pour prototyper, restent révisables

- Nom de la ville : **Morrow Creek**, Oregon ; population environ 8 000. Nom de travail.
- Lieux : **Morrow Diner**, **The Static Room**, **Morrow Creek High**, **Black Alder Mill**, **The Old Growth**.
- Calendrier final proposé : septembre → novembre 2003, ~13 semaines, à préciser sur la base du rythme testé.
- Moteur : **Godot 4.x** pour combiner 3D, UI 2D et données. Ni Unity ni Unreal n'ont été exclus par l'utilisateur.
- Caméra : première personne à hauteur humaine ; cadrage rapproché lors de l'utilisation du PC, puis retour au contrôle d'exploration. Les anciens prototypes à la troisième personne sont historiques.
- Statistiques : sociabilité, observation, débrouillardise, endurance, avec fatigue, stress et argent comme ressources.
- Personnages prototypes : Hannah (photo), Eli (musique), June (diner). Noms et biographies provisoires.
- Horloge : jour d'école → un choix principal après les cours ; week-end → deux créneaux. Pas de simulation temps réel continue.
- Premier prototype : 7 jours de boucle jouable ; extension ultérieure à 14 jours puis 6 semaines.

## VOLONTAIREMENT OUVERT — ne pas figer par automatisme

- Genre et apparence détaillée du protagoniste, système de personnalisation, pronoms ; ne pas forcer un héros prédéfini sans discussion.
- Nature ultime du phénomène, motivations d'une éventuelle entité, degré de confirmation des théories.
- Nombre de personnages romançables dans le jeu final et contenu exact des routes.
- Destination finale : fin unique, fins multiples, mystère partiellement insoluble ; à tester après le vertical slice.
- Durée réelle d'une partie (heures), budget art et portée commerciale.
- Apparence finale précise des portraits, taille de la zone 3D, résolution cible, voix.
- Le calendrier de la ville : l'automne est-il littéralement répété, prolongé ou seulement perçu comme tel ? Laisser volontairement plusieurs hypothèses.

## RÈGLES DE CONFLIT

- Le fichier Tokimeki étudie un **jeu original de 3 ans**. **Notre jeu se déroule sur un seul automne.**
- Une présentation « hybride 2D/3D » ne veut pas dire déplacements en sprites 2D : portraits 2D et environnements/personnages 3D.
- « Horreur omniprésente » ne signifie pas jumpscare toutes les minutes ; l'inconfort peut venir de l'environnement et des conversations.
- « Mystery Life Sim » signifie que les relations sociales peuvent être amicales, hostiles ou romantiques ; la romance est facultative.
- L'imitation de l'ambiance Web 2003 ne signifie pas intégrer une connexion réelle à Google ni copier son logo.

## NOUVEAU — proposition technique V0.5, pas nouvelle décision créative verrouillée

- **Pipeline recommandé** : Blender `bpy` (scripts batch versionnés) + export `.glb` + Godot ; MCP for Blender **facultatif** pour itérer en GUI.
- **Personnages** : humanoïde pilote, rig Mixamo ou Rigify après essai, bibliothèque d'animations testée dans Godot ; API 3D générative uniquement en option après autorisation de coûts.
- **Qualité** : sources éditables et vérification visuelle dans le moteur ; pas de promesse de modèles déjà générés.
- Ces propositions sont développées dans `docs/17_...` à `docs/20_...` et **n'étendent pas la livraison P0**.


## Actualisation V0.15 — parquet

Le porteur de projet apprécie le parquet réel 256px et demande une réduction PSX avec avant/après. Proposition réalisée : 128px nearest avec mipmaps, appliquée au seul sol ; taille des lames, lumière, géométrie et palette conservées. Le test 64px reste disponible. Voir captures/parquet_psx/index.html ; le rendu 128px ne reçoit pas automatiquement une validation artistique humaine.
