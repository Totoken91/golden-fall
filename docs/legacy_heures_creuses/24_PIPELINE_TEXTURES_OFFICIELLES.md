# Textures officielles — pipeline permanent Poly Haven + ambientCG

Outil de fabrication ajouté le 9 octobre 2026 au projet V0.14. Il recherche et télécharge à la demande des fichiers réels, puis prépare des matériaux Godot réutilisables. Il ne tourne pas pendant le jeu. Les scènes, modèles et exécutable de la chambre sont conservés ; les applications visibles dans `captures/textures/` sont des contrôles temporaires en mémoire.

## Utilisation à chaque nouvelle texture

1. Décrire la surface réelle : usage, matériau, ancienneté, couleur, dimensions et densité UV. Vérifier le manifeste pour réutiliser un matériau déjà acquis et adapté. Ne pas employer le même bois pour parquet, meubles, écorce et papier.
2. Lancer `search` ou directement `acquire`. Les deux API sont recherchées ; le classement utilise pertinence, usure, contexte et mots à éviter. C'est une présélection par métadonnées, pas un jugement visuel automatique. Toute source indisponible apparaît dans `search_errors`.
3. Inspecter les maps téléchargées et le panneau `review_tiling_2x2.png`. Écarter un matériau inadapté, même bien classé. Les mesures de bord sont des diagnostics, pas une certification seamless. Choisir un autre candidat si le raccord ou le motif répété ne convient pas.
4. Appliquer le matériau à la surface concernée, avec ses UV et une période exprimée en mètres. Inspecter le rendu dans Godot, sous la lumière du lieu, de près, à distance et en mouvement si nécessaire. Enregistrer la capture et les réserves avec `review`.
5. Consigner sources, licence, transformations et preuve visuelle. Ne jamais avancer un matériau au statut « approuvé par l'utilisateur » après un simple test technique.

## Installation et commandes

Depuis la racine du projet, avec **Python 3.11+ et Pillow** :

```powershell
python -m pip install -r scripts/textures/requirements.txt
python scripts/textures/pipeline.py search --brief wood_floor
python scripts/textures/pipeline.py acquire --brief wood_floor --size 256
python scripts/textures/pipeline.py verify --offline
```

`scripts/textures/textures.ps1` transmet les mêmes arguments à Python. Codex peut utiliser le Python fourni par son environnement ; aucun chemin utilisateur n'est codé en dur dans le pipeline.

Briefs disponibles : `wood_floor`, `aged_plaster`, `weathered_metal`. Pour un nouveau besoin, ajouter un brief à `assets/textures/config.json`, ou employer `--brief-json` avec un objet JSON contenant `query`, `ambientcg_query`, `usage`, `require_any`, `prefer`, `avoid`. Les mots de classement doivent être minuscules et simples, adaptés aux tags des catalogues. `--query` remplace la recherche des deux sources, mais garde les contraintes du brief : choisir ou définir un brief de la bonne famille.

```powershell
python scripts/textures/pipeline.py acquire --brief aged_plaster --provider ambientcg --tile-m 2 2
python scripts/textures/pipeline.py acquire --brief wood_floor --provider polyhaven --id wood_planks --reason "Bois use retenu pour une surface de parquet precise"
```

Même avec un fournisseur ou un ID explicite, les deux catalogues sont recherchés. Un ID explicite exige une raison enregistrée. Sans ID, le meilleur candidat du fournisseur choisi, ou des deux en mode `auto`, est retenu après vérification des maps, du budget et de l'échelle disponible.

`--tile-m WIDTH HEIGHT` indique la taille physique d'une tuile source. Si la donnée manque, le téléchargement est interrompu avant les fichiers : fournir une mesure ou une hypothèse de travail explicite, puis la contrôler en jeu. `--surface-m WIDTH HEIGHT` prépare un matériau pour une surface dont les UV couvrent 0..1. Ces deux options n'effectuent pas de dépliage UV.

## API et provenance

- Poly Haven : `/search?q=...&t=textures` pour le classement initial, `/info/{id}` pour les métadonnées, **`/files/{id}` pour chaque URL, taille et MD5 de map**. Les dimensions de l'API sont en millimètres. User-Agent identifiant Les Heures Creuses ; fournisseur nommé dans les résultats et rapports. [API officielle](https://polyhaven.com/our-api), [schéma OpenAPI](https://api.polyhaven.com/api-docs/swagger.json).
- ambientCG : **`/api/v2/full_json`**, paramètres `q`, `type=Material`, `limit` et `include=downloadData,tagData,dimensionsData`. Lecture de `downloadFolders` et des liens de ZIP réels ; extraction sélective Color, NormalGL, Roughness, AmbientOcclusion quand disponible. Les dimensions v2 sont traitées en centimètres ; zéro signifie inconnu. [Documentation officielle v2](https://docs.ambientcg.com/api/v2/full_json/).
- Aucune URL de fichier n'est devinée à partir du nom. Les champs preview/thumbnail ne servent jamais de texture finale. Pas de scraping de pages Web ni de clé/API payante.
- Les fichiers d'assets sont CC0-1.0 ; les pages de politique sont enregistrées dans chaque entrée : [Poly Haven](https://polyhaven.com/license), [ambientCG](https://docs.ambientcg.com/license/). Les conditions de l'API restent distinctes de la licence des fichiers.

## Organisation et cache

```text
assets/textures/config.json                 briefs, profils et budgets
assets/textures/manifest.json               provenance, hashes, transformations, revues et exécutions
assets/textures/cache/api/                  réponses JSON horodatées, clés par URL
assets/textures/sources/<source>/<id>/       fichiers originaux, reçus SHA256, archives et maps extraites
assets/textures/optimized/<clé>/            PNG optimisés et planche de contrôle 2×2
game/assets/textures/library/<clé>/         seules maps utiles au moteur + material.tres
game/assets/textures/library/catalog.json   catalogue hors ligne du composant Godot
captures/textures/                         captures réelles des essais
```

Une demande identique vérifie les hashes du manifeste et réutilise les fichiers sans réseau. Changer le profil, la résolution, l'échelle ou le brief crée une variante ; les originaux identiques restent réutilisés. Le cache HTTP des métadonnées dure sept jours. `--refresh` renouvelle métadonnées et sélection ; les fichiers déjà intègres et correspondant aux métadonnées restent en cache. `--offline` autorise uniquement les données présentes ; un manque produit un échec explicite.

Limites : une acquisition, 32 MiB transférés maximum ; fichier individuel, 48 MiB maximum ; 1K source par défaut, option 2K. Recherche bornée à six candidats par source, ajustable de 1 à 12 ; aucune aspiration du catalogue entier. HTTPS, délai réseau de 25 s, reprises bornées des erreurs transitoires et respect de Retry-After court ; arrêt explicite pour un délai supérieur à dix secondes. JSON et reçus écrits atomiquement ; verrou empêchant deux mutations concurrentes du manifeste.

Le SHA256 local est vérifié avant réutilisation. Le MD5 fourni par Poly Haven, les tailles déclarées et le CRC des membres ZIP ambientCG sont contrôlés quand disponibles. Un HTML, une image illisible, une archive dangereuse ou un transfert incomplet ne devient jamais un asset réussi dans le manifeste. Un blocage réseau doit être signalé avec l'erreur réelle ; ni placeholder, ni capture de prévisualisation ne le remplace.

## Conversion et direction artistique

Profil par défaut `retro_realistic` : 256 px maximum, aspect conservé, aucune montée en résolution, Lanczos pour l'albedo, filtrage linéaire avec mipmaps dans le matériau. Saturation ×0,88 et gains RGB [1,02 ; 1 ; 0,94] uniquement sur l'albedo, pour un vieillissement discret. Le profil `neutral` préserve la couleur ; `psx_faceted` active nearest avec mipmaps et un relief plus faible. `--size 512` est disponible pour une grande surface qui le justifie.

**La géométrie et le rendu global restent PSX.** Ces profils permettent une matière réaliste sans transformer systématiquement chaque texture en pixel art. La palette doit venir du matériau et de la lumière ; ne pas jaunir roughness, normale ou AO. Pas de grain aléatoire ajouté partout, de dégradation arbitraire ou d'éclairage cuit dans l'albedo.

Les normales sont converties en OpenGL, avec inversion Y uniquement si la source est DirectX, puis renormalisées après réduction. Roughness et AO sont des données linéaires en niveaux de gris. Maps PBR alignées à la même taille ; refus si les dimensions source divergent. AO est facultative. Pas de displacement, tessellation, nouveaux polygones ou surbrillance générique. Ajuster les paramètres métalliques selon l'objet réel lors de son intégration ; le matériau généré est une base diélectrique, adaptée notamment au bois, à l'enduit et à la peinture/rouille.

## Application à un objet Godot

Les `.tres` sont prêts à charger mais ne modifient aucune scène automatiquement. Le composant réutilisable `game/scripts/world/texture_library.gd` applique une surface précise en respectant une période UV connue :

```gdscript
var library = load("res://scripts/world/texture_library.gd").new()
var result = library.apply_surface(mesh_instance, surface_index,
    "polyhaven/wood_planks/retro_realistic_256_65dacce0", Vector2(1.8, 1.8))
assert(result == OK)
```

Ici un cycle des UV existants couvre 1,8 m, alors que la tuile source couvre 1,5 m : le matériau reçoit une échelle UV de 1,2. Le composant refuse une surface sans UV et duplique le matériau avant changement. Il ne déplace pas les sommets, n'écrase pas les autres surfaces et n'altère pas l'UV atlas d'un asset. Pour un atlas, un dépliage irrégulier ou une direction de fil spécifique, préparer le matériau/UV adapté dans Blender plutôt que plaquer une répétition automatique. Vérifier aussi tangentes, normales, orientation du grain, densité texel et ombres.

## Tests réels de cette livraison

| Fournisseur | Asset obtenu via API | Fichiers utiles | Octets téléchargés |
|---|---|---|---:|
| Poly Haven | `wood_planks` | albedo, normal GL, roughness, AO | 7 141 479 |
| ambientCG | `Plaster007` | archive 1K-JPG, quatre maps extraites | 8 071 422 |

Les huit maps optimisées occupent **442 279 octets** avant import Godot. Recherche des deux fournisseurs réussie pour les deux demandes. Relances des deux acquisitions en `--offline` : **0 requête, 0 octet transféré**, hashes vérifiés. Rapports et reçus conservent les URL réellement utilisées, la redirection, les tailles, hashes et transformations.

Godot : 18 contrôles réussis, dont chargement des maps, canaux PBR, échelle UV physique, application au sol réel et résolution du laboratoire 640×360. Captures : référence chambre, parquet temporaire, vue proche et panneaux 2×2. Le bois conserve un joint et un motif reconnaissable à répétition ; limiter son usage au parquet et contrôler les grandes surfaces. L'enduit conserve des bandes/taches répétées : usage secondaire localisé, pas de remplacement du papier peint personnel. La tuile de l'enduit, inconnue dans l'API, est fixée à 2 m pour cet essai. Ces réserves sont enregistrées dans les revues du manifeste.

```powershell
python scripts/textures/run_tests.py
godot --headless --path game --editor --import --quit
godot --path game --script res://scripts/qa/texture_lab.gd
python scripts/textures/pipeline.py verify --offline
```

Le script QA nécessite les deux assets d'essai ci-dessus ; il applique le parquet seulement en mémoire et ferme sa propre instance après les captures. Le script de tests confine les fichiers temporaires au dossier `work/` du projet.

Pour consigner une revue réellement effectuée :

```powershell
python scripts/textures/pipeline.py review --key polyhaven/wood_planks/retro_realistic_256_65dacce0 --capture captures/textures/02_chambre_parquet_test.png --notes "UV, echelle, raccords et lumiere inspectes; reserves a preciser"
```

La commande enregistre une preuve et une note ; elle ne peut pas remplacer l'inspection humaine/visuelle. Les quatre captures de test ne constituent pas une refonte du jeu.


## Actualisation V0.15 — parquet intégré

Les essais de la section précédente décrivent V0.14. À la demande suivante du porteur de projet, wood_planks est désormais appliqué au sol en 128px, profil `parquet_psx`. Ce profil conserve les mêmes saturation, gains RGB et force normale que retro_realistic ; seul le filtrage passe à nearest avec mipmaps, la résolution étant réglée à 128. La variante 64px reste un essai. Les deux transformations réutilisent les fichiers du cache : 0 requête, 0 octet téléchargé. La liaison permanente est dans `game/data/room_materials.json` ; comparaison actuelle dans `captures/parquet_psx/index.html`. Les statuts artistiques ne sont pas automatiquement avancés par le remplacement.
