# 19 — Assurance qualité 3D : critères vérifiables

Un script qui termine avec un code retour 0 ne valide **ni la beauté**, ni la jouabilité d'un asset. La QA doit avoir un volet automatisé et un volet humain, avec le rendu dans **Godot**, pas seulement sous Blender.

## Automatisation (minimum)

- Fichier `.blend` source présent pour chaque asset « finalisé » (sauf contenu tiers explicitement documenté).
- `.glb` exporté et structure binaire saine (outil `scripts/assets/inspect_glb.py`).
- Identifiant unique, `source`, `export`, `status`, `license`, `category` et `generation_method` présents dans `assets/asset_manifest.json` (outil `validate_manifest.py`).
- Asset à l'échelle et au pivot attendus ; présence de meshes ; squelette/clips pour asset animé selon les besoins.
- Fichiers non copiés arbitrairement depuis des jeux / films ; origine et droits consignés.
- Une même graine d'entrée produit la même géométrie de base pour un générateur déterministe (les différences de versions de Blender peuvent changer certains outputs).

## Contact sheet obligatoire pour validation visuelle

Pour chaque asset important ou famille, livrer :

1. Trois-quarts en éclairage studio neutre, vue face, vue profil.
2. Même asset au crépuscule ambre avec ciel couvert (couleurs et matériaux réels du jeu).
3. Capture *dans Godot* à l'échelle du joueur, sous la vraie caméra.
4. Pour PNJ : pose de repos, marche en cours, silhouette de profil, assise si concerné.
5. Pour building kit : modules répétés trois fois sans raccord visible aberrant.

Produire captures à partir des outils disponibles et mentionner s'il manque Blender ou Godot. **Ne pas fabriquer des captures de tests fictifs.**

## Critères d'acceptation

| ID | Contrôle | Passe si |
|---|---|---|
| A01 | Source/export | source éditable et GLB lisible présents après génération |
| A02 | Géométrie | normales, UV si nécessaires, pas de surfaces invalides visibles |
| A03 | Proportions | portes, tables et PNJ crédibles ensemble dans Godot |
| A04 | Style | golden brown + contrepoints froids, pas filtre orange uniforme |
| A05 | Rendement | mesure fps/mémoire en Godot et budget consigné, pas estimé |
| A06 | Rig | si animé : pas de skinning incohérent majeur |
| A07 | Animation | si animé : boucle propre, orientation et contacts plausibles |
| A08 | Réemploi | un même type d'asset peut être placé au moins deux fois sans casser la scène |
| A09 | Licences | usages autorisés ; dépendances tierces documentées |
| A10 | Ambiance | scène convaincante *sans* événement horrifique ni surcharge UI |

## Ne pas bloquer le premier prototype sur les assets

Si le rigging n'est pas terminé, garder un mannequin stylisé sans animation sophistiquée et consigner clairement sa nature provisoire. Si Blender ne peut pas être lancé, construire une scène cohérente avec les primitives Godot, puis remplacer les placeholders au fil des sprints. **Aucune dépendance obligatoire à un service payant**.

## Rapport asset recommandé dans `DEVLOG.md`

- Asset/ID/version, générateur ou méthode, sources et licence.
- Capture 3/4 studio + capture Godot (+ captures anim si besoin).
- Tests automatiques exécutés avec commandes et résultats.
- Problèmes observés, améliorations prioritaires, validation humaine restante.
- Coût API réel si autorisé ; sinon « aucun coût externe ».
