# 18 — Personnages 3D : rigging, animation et portraits 2D

**Principe validé :** PNJ en 3D dans le monde ; illustrations de portraits 2D pour les dialogues importants. Ce pipeline réduit la nécessité d'animations faciales complexes et donne priorité à la gestuelle, aux postures et à la direction du regard.

## Un personnage pilote avant tout le casting

Commencer par Hannah (ou un mannequin humanoïde explicitement temporaire). Valider sa **silhouette** en jeu, sa tenue 2003, sa hauteur, ses proportions, puis seulement décliner Eli/June et figurants. Mettre le costume, coiffure, âge apparent et palette en correspondance avec son portrait 2D ; ne pas faire de capture IA pour « convertir » une illustration en modèle fidèle sans reprise manuelle.

### Chaîne A, recommandée pour le premier humanoïde

1. Modéliser/base low-poly dans Blender, géométrie texturée, forme en A/T-pose, maillage propre.
2. Exporter un fichier de travail adapté à **Mixamo** ; auto-rigging dans l'interface Mixamo (authentification et vérification humaine requises ; ne pas prétendre l'avoir automatisé de bout en bout).
3. Récupérer un rig/une animation de test et l'importer dans Blender pour corriger orientation, poids, pose de repos et cohérence des échelles.
4. Exporter un `.glb` avec squelette + clips utiles ; vérifier en dehors de Blender dans **Godot**.
5. Définir un rig/une convention commune, puis réutiliser les clips avec retargeting quand nécessaire.

**Mixamo** est gratuit avec un Adobe ID selon sa FAQ et permet l'utilisation des personnages/animations dans des jeux commerciaux ; **limité aux humanoïdes bipèdes**. Vérifier régulièrement la FAQ et conserver la preuve de licence pertinente au moment de publier.

### Chaîne B : Rigify Blender

Rigify est intégré à Blender : métarig → positionnement des os → génération du rig. Permet plus de contrôle sur le personnage et l'animation, mais demande un travail de préparation du rig de déformation à exporter (ne pas exporter aveuglément tous les contrôleurs Rigify). Préférer cette voie si des poses spéciales ou des rigs plus spécifiques deviennent indispensables.

### Chaîne C : Meshy API (option payante, après décision)

Meshy offre un rigging automatisé **pour humanoïdes texturés standards**, puis une API d'application d'animations prédéfinies. L'API peut échouer sur modèles atypiques, membres ambigus, maillages sans textures ou budgets dépassés. Les appels sont facturés en crédits et exigent une clé API / un compte approprié ; **ne pas intégrer au chemin critique ni utiliser sans autorisation de coût**. Tripo est une piste distincte pour de la génération 3D ; ne pas supposer un auto-rigging équivalent sans vérification de capacités et licence du service choisi.

## Bibliothèque pilote d'animations

| Clip | Usage | Vérification incontournable |
|---|---|---|
| `idle_breath` | Attente et conversations | Pas de déplacement, respiration discrète |
| `walk_forward` | Navigation de zone | Contact sol, pas de glissement |
| `walk_stop` | Arrêt près du joueur | Alignement feet/root |
| `turn_90` | Réorientation face interlocuteur | Pas de téléportation |
| `sit_down` / `sit_idle` / `stand_up` | Scènes diner | Hanches à bonne hauteur de banquette |
| `talk_small` | Dialogues calmes | Sobre, naturel, pas de grands gestes répétitifs |
| `look_back` | Inquiétude subtile | Rotation tête/torse cohérente |
| `startled_small` | Anomalie lointaine | Pas d'animation de scream exagérée |

**P0** : seuls idle, marche et interaction de base sont nécessaires ; l'assise, la gestuelle et les autres variantes peuvent être simplifiées temporairement. L'objectif P0 reste **7 jours jouables**, non une démo complète d'animation.

## Godot : retargeting et pièges

- Godot 4 utilise `BoneMap` / `SkeletonProfileHumanoid` pour partager des animations entre squelettes ; les noms d'os **ne suffisent pas** : la hiérarchie et la *rest pose* doivent correspondre.
- Importer **un rig pilote** et le faire jouer sur une scène simple ; vérifier root motion, pieds, bras, collisions et transitions avant duplication.
- Préférer une convention stable de taille, d'orientation, de nom des animations et de squelette.
- Les portraits 2D ont un jeu d'expressions distinct (`neutral`, `warm`, `uncertain`, `concerned`) ; ils ne sont pas dérivés directement des animations 3D.
- Le jeu ne doit pas entrer en mode dialogue spécial dès qu'il est paranormal ; l'horreur joue souvent avec le même langage visuel que la vie normale.

## Checklist de validation humanoïde

- [ ] Pivot au sol, échelle et orientation conformes à la scène Godot.
- [ ] Pas de membres inversés, maillage retourné, faces cassées ou poids incohérents.
- [ ] Idle stable 10 secondes ; marche sans patinage évident ; demi-tour sans snapping.
- [ ] Une pose assise fonctionne au diner (si clip produit).
- [ ] Le même modèle fonctionne de jour et sous éclairage sodium sans devenir illisible.
- [ ] Silhouette du modèle 3D et portrait 2D se reconnaissent comme le même personnage.
- [ ] Les clips utilisés ont une origine et une licence consignées dans le manifeste.

**Références** :
- Mixamo FAQ Adobe : https://helpx.adobe.com/creative-cloud/faq/mixamo-faq.html
- Rigify : https://docs.blender.org/manual/en/4.0/addons/rigging/rigify/index.html
- Retargeting Godot : https://docs.godotengine.org/en/4.5/tutorials/assets_pipeline/retargeting_3d_skeletons.html
- Meshy rig : https://docs.meshy.ai/en/api/rigging
- Meshy animations : https://docs.meshy.ai/en/api/animation
