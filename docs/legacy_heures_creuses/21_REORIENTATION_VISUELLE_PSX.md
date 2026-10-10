# Direction visuelle courante — PSX, première personne (actualisée V0.14)

La direction issue du pack PSX fourni le 9 octobre 2026 et des demandes suivantes remplace les anciennes consignes PS2 / troisième personne. Gameplay, histoire et données sont conservés. La livraison V0.14 contient le projet Godot, les sources d'assets et une chambre jouable de revue. L'adoption de cette direction ne signifie pas que chaque rendu produit est approuvé.

## Cible
Exploration à la première personne, caméra à hauteur humaine, esthétique PSX texturée et pixelisée, moody golden brown. Géométrie anguleuse aux proportions humaines. Bois tabac, cuivre, ocre, ivoire sale, ombres olive/brun ; lumière ambrée localisée, contrepoint extérieur gris. Atmosphère quotidienne, habitée et mélancolique en automne 2003.

La référence générée `reference/visuel_cible_psx.png` exprime une intention artistique, pas une capture réelle ni une promesse de fidélité moteur. Les choix de détail qu’elle introduit ne constituent pas du canon narratif.

## Critères visuels
- Chambre fermée à échelle humaine ; aucune vue isométrique ou mur découpé.
- Formes travaillées, UV et textures basse résolution : aucun assemblage de cubes nus accepté comme rendu final.
- Première base à tester : rendu 640×360 agrandi sans lissage ; textures 64–256 px selon objet et densité, filtrage nearest ; dithering subtil. Tester 320×180 seulement si cela améliore le rendu. Valeurs ajustables sur captures, pas des normes PSX historiques.
- Pixelisation du monde 3D ; texte et interface lisibles à résolution native.
- Éclairage doux et composé, brouillard extérieur progressif ; pas de filtre orange uniforme, de noir brutal ou de bloom excessif.
- Personnages polygonaux avec silhouettes humaines et textures faciales lisibles ; portraits 2D conservés pour les échanges importants.
- Agenda et journal en 2D. L'ordinateur est un CRT physique : la caméra se place devant, puis le joueur contrôle la souris sur l'OS fictif Cedar 03, inspiré de l'époque XP sans reprendre ses graphismes. Aucun ajout de combat ou de mécanique FPS.

## Acquis des demandes V0.10–V0.14

- Conserver la scène et le cadrage de référence ; palette golden brown, matières distinctes et détails personnels.
- Améliorer les silhouettes et textures sans lisser les volumes ni multiplier les subdivisions. Les détails fins passent en texture ; la literie reste facettée.
- Pas de veste sur la chaise. Les objets reposent sur un support réel, sans clipping visible ; vérifier aussi rideaux, plinthes et volumes derrière le mobilier.
- Forêt dense en plusieurs profondeurs, pluie forte et moody, gouttes animées indépendamment sans grille, ambiance audio fournie par l'utilisateur.
- Comparer dans Godot au même cadrage et inspecter en mouvement. Sources et contrôles conservés dans le guide `22_GUIDE_CREATION_ZONES.md`.
- Réglages actuels : monde 640 × 360 nearest, UI lisible ; plafond de travail chambre + extérieur + pluie de 8 000 triangles, avec 7 970 mesurés en V0.14. Ce plafond est un choix de production révisable, pas une norme historique PS1 ni un budget global du jeu.

## Étape initiale de revue (historique V0.7)
Suspendre les nouvelles fonctionnalités. Préserver les systèmes, refaire uniquement la chambre : marche, regard souris, interactions bureau/PC/lit/porte. Valider caméra et proportions, puis modèles/textures, puis lumière et décoration. Fournir trois captures réelles Godot (porte, bureau, fenêtre), vérifier collisions et interactions et consigner les lacunes. Ne pas étendre la refonte à rue/diner avant validation de la chambre. Une capture technique réussie ne valide pas la beauté.

## État actuel et suite proposée

Les passes de chambre ont abouti à la V0.14. Le rendu reste à apprécier humainement. Le raccordement de cette base à la première journée puis à la semaine est décrit dans `23_ETAT_PROTOTYPE_ET_PROCHAINES_ETAPES.md` ; aucune nouvelle zone n'est déclarée réalisée ou approuvée par cette documentation.
