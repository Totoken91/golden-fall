# AGENTS.md — Instructions pour Codex et agents de développement

## Source d'autorité

**V0.20 — écran du PC lisible, Cedar 03 mi-2000, demande utilisateur.** Bureau affiché en pleine résolution par-dessus le tube une fois zoomé ; OS redessiné (fond peint, barre brillante, fenêtres à ombres, bulles, navigateur d'époque), sons synthétisés. Contrats V0.19 inchangés. Lire `docs/29_OS_CEDAR_V020.md`. Présenter chaque passe visuelle en galerie avant/après (modèle `captures/cohesion_v017`).

**V0.19 — interfaces regroupées sur le PC, demande utilisateur autorisée.** Agenda, journal et sauvegarde manuelle sont des applications Cedar 03 accessibles sur le CRT physique. Consultation gratuite à tous les créneaux ; la recherche est une activité explicitement commencée dans CedarSearch. L'agenda enregistre une intention sans exécuter l'activité ; étude au bureau, repos/sommeil au lit. Aucune barre flottante Agenda/Journal/Sauvegarder, aucun panneau de gestion via J/Tab dans la chambre, aucune sauvegarde manuelle dans la pause. Échap conserve pause, son, retour au titre et quitter ; le titre conserve nouvelle partie/chargement. Autosave conservée. F5 dans le CRT ouvre la sauvegarde avec retour visible, hors CRT il indique où la trouver. Un petit carnet hors de la chambre reste une possibilité pour les futures zones, pas une fonctionnalité déjà livrée. Lire `docs/28_INTERFACES_PC_V019.md`.

**État courant V0.18 — démarrage du prototype, 9 octobre 2026.** L'utilisateur valide le dithering, puis autorise à commencer le prototype suivant les priorités recommandées. Variante douce retenue : Bayer 4×4 fixe dans les pixels monde 640×360, 32 niveaux par canal, amplitude 1. Parquet approuvé, bois 224 texels/m, palette et géométrie conservés. Première livraison de cette phase : socle de campagne dans la chambre actuelle, avec activités, CRT, notes, sauvegarde/reprise et sommeil. La journée sociale intégrée et les sept jours ne sont PAS encore livrés. Lire `docs/27_SOCLE_CAMPAGNE_V018.md` et le plan de lots ci-dessous ; ne pas confondre un état testé avec une approbation artistique.

**Priorités de prototype autorisées :** 1) campagne persistante raccordée à la chambre ; 2) rue courte + diner PSX + Hannah 3D/portrait et choix à conséquence ; 3) sept journées avec accès alternatif aux indices ; 4) anomalie discrète et conséquence le lendemain ; 5) deux parcours et sauvegarde/reprise validés de bout en bout. V0.18 livre seulement le premier socle domestique. Le point d'entrée jouable est `game/scenes/campaign.tscn`, contrôleur `campaign.gd` héritant de la chambre ; la scène `room_review.tscn` reste une revue/QA indépendante. Réutiliser le même `LifeState` et `WebArchive`, sans recréer des données sociales ou des indices dans les scènes. Slot dédié `user://campaign_day_v1.json`, distinct de `first_day_v2.json`. Les scripts de test utilisent une sauvegarde isolée. Ne pas activer simplement les jours suivants : `LifeState.sleep()` termine encore au 14 octobre ; l'extension doit venir avec le contenu et les contrôles de la semaine. Lire le document 27 avant cette modification.

**Priorité actuelle V0.17 — cohésion :** le retour utilisateur préfère V0.16 mais demande moins de contraste et une taille de détail cohérente entre chevet et bureau. Parquet validé inchangé. Dix groupes de bois à 224 texels/m, maps 128px, contraste 0,72 et exposition 1,06. Lire `docs/26_COHESION_MATIERES_V017.md`. Après `prepare_room_materials.py`, lancer `harmonize_room_wood.py` puis `--verify` avant import/export. Comparaison courante `captures/cohesion_v017/index.html` : avant V0.16, après V0.17. Une résolution commune ne suffit pas : contrôler la densité métrique réelle et l'axe du grain. Aucun ajout géométrique, lumière ou sol modifié. V0.17 inspectée en moteur, pas encore approuvée par l'utilisateur.

**Demande actuelle V0.16 — matières de la chambre :** le parquet téléchargé réduit à 128px est explicitement validé par l’utilisateur ; conserver exactement sa liaison et ses fichiers. Étendre le principe aux objets quand le matériau convient, sans nouveaux polygones ni changement de disposition. 20 surfaces groupées sont traitées en 128px : bois distincts de bureau et de meubles, rideaux, literie, sac, abat-jour, haut-parleur, corbeille et plafond. Les textures d’identité sont conservées et composées avec la trame réelle lorsque nécessaire. Règles dans `game/data/room_materials.json`, préparation reproductible `scripts/textures/prepare_room_materials.py`, provenance des compositions `assets/textures/room_derived_manifest.json`, intégration `room_material_pass.gd`. Lire `docs/25_MATIERES_CHAMBRE_V016.md`. Comparaison actuelle : `captures/matieres_v016/index.html`, avant = V0.15 avec parquet déjà validé, après = nouvelles matières. Les nouvelles matières restent soumises au retour artistique de l’utilisateur.

**Clarification avant/après V0.15 :** l’utilisateur veut comparer le plancher avant tout matériau téléchargé au parquet téléchargé et réduit à 128px. Comparaison de référence : `captures/parquet_origine_vs_128/index.html`. Restaurer temporairement le matériau `floor` d’origine du GLB pour capturer l’avant ; ne pas le confondre avec l’essai téléchargé en 256px. Le jeu reste sur le parquet 128px. Les comparaisons 256/128/64 de `captures/parquet_psx/` sont des essais techniques séparés.

**Demande actuelle V0.15 — parquet plus PSX :** l'utilisateur apprécie le parquet réel de l'essai 256px et demande de réduire sa texture avec avant/après. Intégration ciblée du sol en 128px, nearest avec mipmaps ; variante 64px examinée mais non retenue car les joints perdent trop de définition. Conserver taille des lames, UV, couleurs, normale, éclairage et géométrie. Liaison du sol : `game/data/room_materials.json`, appliquée après préparation des meshes. Comparaisons réelles au même cadrage dans `captures/parquet_psx/`. La V0.14 reste intacte. Cette demande autorise le remplacement du parquet, sans refonte des autres surfaces.

**Demande actuelle — pipeline permanent de textures (9 octobre 2026) :** pour tout besoin de nouvelle texture de matériau, lire `docs/24_PIPELINE_TEXTURES_OFFICIELLES.md`, vérifier `assets/textures/manifest.json`, puis utiliser `scripts/textures/pipeline.py` avec un brief adapté. Rechercher automatiquement sur **Poly Haven et ambientCG via leurs API officielles**, sélectionner selon la surface et la direction artistique, télécharger les vraies maps via métadonnées de fichiers, optimiser et inspecter dans Godot avant intégration. Réutiliser le cache lorsqu'un matériau adapté existe. Les commandes `acquire`, `verify --offline` et `review` assurent provenance et preuves ; le composant Godot `texture_library.gd` applique une surface avec période UV en mètres. Aucun réseau nécessaire en jeu. Signaler un accès bloqué sans prétendre au téléchargement. Ne pas remplacer les textures d'identité (posters, photos, illustrations) par des matériaux génériques. Cette tâche autorise le pipeline et ses essais, **aucune refonte de la chambre**.

**Direction matière :** préserver les silhouettes PSX et le golden brown ; rechercher des surfaces anciennes, sales et réalistes adaptées à leur usage. Employer une résolution et un filtrage choisis par surface, sans imposer du pixel art à toutes les maps. Ne pas multiplier les polygones, ne pas appliquer un filtre jaune global et ne pas réutiliser un matériau générique partout. Le classement par métadonnées ne vaut pas validation visuelle, seamless ou artistique.

**État des lieux documentaire V0.14 :** lire `docs/23_ETAT_PROTOTYPE_ET_PROCHAINES_ETAPES.md` pour distinguer la chambre de revue, les systèmes de la première journée historique et la semaine future. La direction courante première personne / PSX / golden brown et le PC physique sont synchronisés dans les décisions et la présentation. La feuille de route reste une recommandation ; cette mise à jour ne commande pas de nouvelles fonctionnalités.

**Étape actuelle V0.14 :** corriger les contacts et placements signalés par l'utilisateur : casque posé, ventilation intégrée à la coque, petits accessoires sur leurs supports ; remplacer la pluie en grille par une distribution libre. Corriger aussi l'encodage de l'interface visible dans ses captures. Conserver PSX, cadrage, forêt, lumière, PC physique, audio, absence de veste et budget de travail de 8 000 triangles, pluie comprise. La V0.13 reste intacte.

**Étape actuelle V0.13 :** l'utilisateur demande une meilleure qualité de l'extérieur, une forêt plus dense et une pluie plus convaincante, avec capture V0.12 fournie. Recomposer plusieurs profondeurs de forêt et sous-bois, enrichir les textures et la pluie, conserver le style PSX, la palette, la chambre, le PC interactif, le son fourni et le plafond de travail de 8 000 triangles. Préserver les versions précédentes et documenter les acquis.

**Demandes complémentaires V0.12 autorisées par l'utilisateur :** PC physiquement interactif, caméra devant l'écran, OS fictif old school proche de l'époque XP, souris/clavier ; pluie plus forte et plus moody ; enregistrement MP3 fourni pour son ambiance. Ces demandes priment sur les anciennes limites excluant une nouvelle interaction. Le plafond de 8 000 triangles est un choix de travail de cette passe, pas un chiffre explicitement imposé par l'utilisateur.

**Étape actuelle V0.12 :** l'utilisateur demande explicitement de réduire encore les polygones en conservant la qualité des assets et le caractère PSX de sa deuxième image. Retenir des formes plus facettées, transférer les petits détails géométriques en textures et abaisser le plafond de chambre à 8 000 triangles. Conserver les améliorations de matières, les posters générés, le cadrage, la lumière, la palette golden brown, la pluie et le sac sans clipping ; chaise toujours sans veste. Mettre à jour le guide avec cet apprentissage : améliorer un asset ne signifie pas arrondir ou subdiviser sa silhouette.

**Étape actuelle V0.11 :** l'utilisateur demande explicitement de générer les posters avec imagegen. Remplacer uniquement les deux illustrations de posters par des images originales générées avec l'outil intégré, conserver leurs titres, positions, tailles, le cadrage, la palette golden brown et toute la géométrie V0.10 (13 820 triangles, veste retirée). Préserver les sources d'images et les prompts ; aucune dépendance générative pendant le jeu.

**Étape actuelle V0.10 :** retirer la veste de la chaise à la demande explicite de l'utilisateur. Corriger le rabat et la sangle du sac V0.9 qui traversent son corps. Réduire le nombre de triangles, avec un plafond de projet à 16 000 pour chambre et extérieur, des plafonds par accessoire, des contrôles d'intersections du sac et une inspection sous plusieurs angles. Conserver le cadrage, la palette, l'éclairage et la météo.

**Étape actuelle V0.9 :** l'utilisateur rejette la veste V0.8 et demande d'améliorer les assets, en conservant la chambre et sa direction déjà retenues. Reconstruire le vêtement et améliorer les accessoires visibles ; montrer les modèles dans le jeu et expliquer honnêtement leur fabrication locale. Les anciennes passes restent archivées ; aucun agrandissement du périmètre de jeu.

**Étape actuelle V0.8 :** le porteur de projet demande explicitement de conserver la scène et son cadrage V0.7. La passe autorisée porte sur l'extérieur plus profond et moins géométrique, la pluie animée, l'éclairage moins uniforme, les matières, la literie plus souple, le manteau sans traversée de chaise et quelques détails personnels. Fournir le même point de vue pour comparaison et une courte vidéo réelle du moteur. Ne pas élargir aux autres lieux ou à la progression.

**Étape actuelle V0.7 :** le rendu V0.6 a été rejeté par le porteur de projet, qui a fourni le pack V0.6 PSX. La proposition courante suit sa direction visuelle (`docs/21_REORIENTATION_VISUELLE_PSX.md`) et se limite à la chambre en première personne. Ne pas étendre la refonte à la rue/diner ou la semaine avant retour sur cette chambre. Les données et systèmes corrigés V0.6 restent conservés. Le fichier fourni décrit une direction ; il ne vaut pas acceptation du nouveau rendu produit.

La demande actuelle du porteur de projet prime sur les consignes ci-dessous. Le 9 octobre 2026, il a autorisé les corrections du pack et validé la priorité d’une **première journée complète**. V0.6 réalise cette étape ; les sept jours restent la cible suivante. Ne pas présenter cette étape intermédiaire comme la validation artistique ou ludique de P0.

1. Les décisions validées de `docs/00_DECISIONS.md` priment sur tout.
2. `docs/06_VERTICAL_SLICE.md` définit le périmètre de la livraison en cours.
3. `docs/01_VISION.md`, `docs/02_GAMEPLAY.md`, `docs/03_MYTHOLOGIE.md`, `docs/04_PRESENTATION.md`, `docs/05_WEB_2003.md` définissent les invariants créatifs.
4. `docs/07_TECHNIQUE.md` et `docs/12_DONNEES.md` définissent les contrats et choix techniques proposés.
5. `docs/17_PIPELINE_ASSETS_3D.md` à `docs/20_INSTALLATION_OUTILS.md` définissent une **proposition technique** de chaîne d'assets, sans changer la portée P0 ni les décisions créatives validées.
5. La partie 1–13 de `reference/Tokimeki_Memorial_1994_Analyse_Game_Design.md` est une étude historique. **Les sections 14–16 de cet ancien document sont des idées antérieures et ne constituent pas les spécifications courantes** : notamment 3 années, semaine lundi-samedi et 6–8 personnages ne sont pas les décisions de ce projet.

## Mission de livraison initiale

Créer un **prototype Godot 4.x jouable de 7 jours** qui prouve la cohérence entre : agenda 2D → rue/chambre/diner 3D → dialogue avec portrait 2D → conséquence sociale → enquête via ordinateur 2003 → anomalie discrète → sauvegarde/reprise.

## Règles de production

- Garder **une seule boucle temporelle**. Pas de boucles survival, dating et enquête séparées.
- Le contexte est **un automne unique en 2003**, pas 3 ans ni 4 saisons. Éviter des assets hivernaux/estivaux.
- Atmosphère **golden autumn gothic** : cuivre, ambre, bois, vert sombre, brouillard naturel ; ne pas appliquer un filtre bleu uniforme ni une image orange monochrome.
- Pas d'assets dérivés ou copiés de Twilight, Silent Hill, Tokimeki, Windows XP, Google, etc. Utiliser des signes d'époque originaux.
- **Portraits 2D illustrés** sur fonds 3D pour dialogues sociaux importants. Personnages 3D dans le monde. Ne pas employer des sprites 2D pleins pieds comme remplaçants dans l'exploration.
- Interface sobre, lisible et crédible en 2003. **Pas d'AI slop** : pas de dashboards chargés, d'icônes aléatoires, de néons gratuits, de cartes partout ni de texte explicatif permanent.
- Exploration en première personne suivant le pack PSX, petites zones chargées, pas d'open world. L'ancienne caméra orthographique reste uniquement dans la scène historique de tests.
- Personnages avec mémoire des faits et états internes ; pas uniquement une barre d'amour. Romance non imposée.
- Horreur omniprésente dans le cadre et les conséquences, **pas des jumpscares ou poursuites en série**.
- La nature de la présence dans la forêt reste ambiguë. Pas de révélation mécanique « le monstre est X » sans validation créative.
- Internet de 2003 simulé **hors ligne**, sites fictifs, recherche par termes et synonymes ; éviter les marques/graphismes sous licence dans le jeu final.
- Rédiger le code et les contenus dans des fichiers séparés, data-driven, sans énorme script monolithique.
- Pas d'appels réseau réels ni de modèle génératif nécessaire pour fonctionner ; déterminisme et sauvegardes reproductibles.
- Pas d'assets temporaires interchangeables sans identité : les placeholders doivent suivre la composition et la palette, même s'ils sont simples.
- **Pipeline asset recommandé** : générateurs Blender `bpy` hors-ligne → sources `.blend` → exports `.glb` → scènes Godot. Préserver les sources et vérifier en jeu.
- **MCP for Blender facultatif**, seulement si installé et autorisé dans l'environnement accessible à Codex ; ne pas bloquer le prototype si absent.
- Créer un **personnage humanoïde pilote** avant des variantes ; animations et rigs réutilisables, portrait 2D correspondant au modèle 3D.
- Distinguer `planned`, `generated` et `approved` dans le manifeste ; un export valide n'est **pas** une validation visuelle.
- Ne jamais générer via API payante (Meshy/Tripo ou autre), ni consommer des crédits, ni envoyer d'assets hors ligne sans autorisation du porteur de projet.
- Ne pas introduire de mécanique de combat, armes, crafting, faim/soif, jauge de folie ou IA générative sans accord.

## Façon de travailler

**Mémoire de production demandée par l'utilisateur (9 octobre 2026) :** avant une nouvelle zone ou une passe d'assets, lire `docs/22_GUIDE_CREATION_ZONES.md`. Il consigne les acquis et erreurs vérifiés des passes V0.7–V0.14. L'utiliser comme référence, puis le mettre à jour avec les résultats de chaque zone ; ses suggestions ne constituent pas de nouvelles décisions créatives validées et ne remplacent pas la demande courante.

1. Lire les docs, résumer en cinq phrases l'architecture choisie dans `DEVLOG.md`.
2. Construire une étape, exécuter tests disponibles, décrire résultats et lacunes. Pour les assets, faire aussi les contrôles de `docs/19_QUALITE_ASSETS.md` lorsqu'un export est réellement produit.
3. Prioriser **une expérience jouable qui donne le ton** plutôt qu'un grand menu de fonctionnalités inachevées.
4. Avant toute nouvelle fonctionnalité, signaler si elle augmente sensiblement la portée ou exige des assets uniques.
5. Ne pas inventer des « décisions validées ». Consigner les choix faits pour tester dans `docs/DECISIONS_TEMPORAIRES.md`.
6. Garder un mode debug permettant date, lieux, événements, relation et recherche, caché du joueur.
7. À la fin de chaque étape, fournir instructions de lancement, captures du jeu si possible, fichiers changés et tests passés/échoués.

## Première livraison attendue

Voir `docs/06_VERTICAL_SLICE.md` et `docs/10_TESTS.md` : la livraison ne se mesure pas au nombre d'écrans mais au fonctionnement de la chaîne causale complète.
