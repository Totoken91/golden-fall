# Fabrication — V0.14

Modèles fabriqués localement par scripts Blender/Python, sans générateur texte-vers-3D ni API payante. Les posters imagegen des passes précédentes restent identiques. Les 52 textures V0.13 sont conservées ; crt_side.png ajoute les évents dans le matériau de la face existante du CRT. Les dix anciennes barrettes séparées sont retirées, économisant 120 triangles.

Le casque utilise un arceau facetté et deux coussinets à huit côtés, orientés à plat sur le livre supérieur. Les pages suivent la transformation de leur livre. Les détails minces des CD et des livres sont des plans texturés. Le cadre possède une vraie inclinaison, un support arrière et un pied. Les papiers de la corbeille sont des plans pliés sur un fond intérieur ; les poignées rejoignent leurs tiroirs par des supports. Les câbles rejoignent la tour et reposent sur le bureau entre leurs points de raccordement.

Les ensembles lit et chevet sont déplacés intégralement ; la lumière suit la lampe. Les rideaux terminent au-dessus de l'appui et dégagent le bureau et la lampe. Le contact du matelas avec le sommier et la hauteur de la literie sont corrigés. Les quatre accessoires principaux gardent leurs silhouettes et leurs budgets : chaise 116, clavier 804, tasse 134, sac 232 triangles. Pas de veste.

La pluie remplace les trois grands plans à shader de cellules par trois MultiMesh de gouttes individuelles : 100 proches, 120 intermédiaires, 140 lointaines. Chaque goutte est un quad à deux triangles, animé dans un vrai volume extérieur par une phase, une vitesse et une graine propres. Les positions de réapparition changent à chaque cycle individuel. Longueurs, largeurs, inclinaisons et opacités varient ; le shader ne contient plus de grille spatiale. Géométrie totale : 7 250 + 720 = 7 970 triangles. Le coût de mise à jour et le remplissage alpha sont mesurés séparément des triangles.

Reconstruction : Python/Pillow avec scripts/assets/make_room_textures.py, puis Blender 4.2 avec scripts/assets/build_room.py. Les deux sources éditables et les exports sont livrés. Le générateur complet inclut toutes les corrections ; aucun script du dossier de travail n'est nécessaire. Attendre la fin effective de Blender avant import/export Godot. Le dernier export a été réalisé depuis le même assemblage, avec le raccordement final des câbles repris du générateur livré.


## Pipeline de textures officielles ajouté après la passe V0.14

Le projet inclut désormais une recherche/acquisition à la demande via Poly Haven et ambientCG, cache et manifeste de provenance, conversions PBR par type de map, génération de matériaux et composant Godot pour une période UV physique. Deux matériaux réels ont été téléchargés et contrôlés dans une instance QA ; les textures du modèle et le build de chambre sont conservés. Voir `docs/24_PIPELINE_TEXTURES_OFFICIELLES.md`, `assets/textures/manifest.json` et `captures/textures/index.html`.
