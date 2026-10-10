# 08 — Direction artistique & sonore : Golden Autumn Gothic

**Actualisation V0.14 :** appliquer la direction PSX texturée, première personne et golden brown de `21_REORIENTATION_VISUELLE_PSX.md` à la production des zones. Les détails fins sont portés par les textures ; améliorer un asset ne signifie pas arrondir sa géométrie. Les rendus livrés ne sont pas automatiquement approuvés.

## Manifeste visuel

Une ville chaleureuse, ancienne, habitée, qui donne la sensation que l'automne a avalé le reste du calendrier. Le jeu ne doit pas ressembler à un jeu PS1 horrifique standard avec skybox noire, ni à une visual novel avec sprites sur photographies, ni à une compilation d'images générées incohérentes.

## Palette de production (couleurs guides, pas LUT imposée)

| Fonction | Couleur | Hex |
|---|---|---|
| Lumière golden hour | ocre doré | `#D49A4A` |
| Feuillage | orange rouille | `#A65B30` |
| Bois / papier ancien | brun tabac | `#76523C` |
| Conifères | vert sapin | `#39483B` |
| Ombres | brun noir | `#29231F` |
| Papier/interface | ivoire chaud | `#E8D9BD` |
| Ciel couvert | gris beige | `#B5B0A5` |
| Lampadaire sodium | ambre profond | `#C87933` |

### Règles colorimétriques

- Pas de bleu « Twilight » omniprésent. Le bleu/gris n'est qu'un contrepoint dans les ombres et le ciel.
- Pas de color grading orange écrasant partout. L'orange doit être une **lumière** et un **matériau**, pas un filtre global.
- Textures avec petites imperfections, rouille, bois humide, peintures délavées, feuilles irrégulières ; varier les tailles de motifs.
- Conserver des contrastes solides dans les scènes de nuit, sans murs noirs artificiels : éclairage doux, falloff naturel, coins obscurs jamais coupés brutalement.

## Look 3D

- Low-poly **PSX**, silhouettes anguleuses à échelle humaine, textures basse résolution cohérentes et matières distinctes. Les détails fins passent en texture plutôt qu'en subdivisions.
- Personnages 3D riggés simples : vêtements grunge, silhouettes naturelles, cheveux crédibles, visages assez lisibles pour les gestes et le regard sans mimique réaliste haute fidélité.
- Feuillage géométriquement économique (billboards/mesh low-poly) ; vent subtil ; sol humide, caniveaux, vieux panneaux en bois, vitrines.
- Décors composés par « plans » : premier plan feuillu, décor lisible, masse sombre de la forêt au loin.

## Portraits 2D — CHOIX VALIDÉ

- Illustrations 2D semi-réalistes et modestes, traits imparfaits contrôlés, ombres peintes/texture papier ; pas anime générique ni rendu photoréaliste qui ne colle pas aux personnages 3D.
- Portraits poitrine/épaules, plusieurs expressions utiles ; palette du personnage et vêtements cohérents avec le modèle 3D.
- Seuls personnages clés nécessitent des portraits à l'initial ; personnages de fond sont 3D sans portrait.
- Aucun portrait ne remplace le personnage dans le monde 3D.

## Sound design et musique

- Indice de son : guitare folk fingerpicked, lente, légèrement « room recording », guitare électrique grunge discrète, ambient aux fréquences étroites, cliquetis du chauffage, bruit de disques, pluie sur verre, vent dans les conifères.
- Ne pas recopier les thèmes d'Iron & Wine, Elliott Smith, Mazzy Star, Duster ou Akira Yamaoka.
- Le son est géolocalisé dans la 3D (chaîne hi-fi, voiture, ventilation, rue) et mixé pour permettre à de longues périodes silencieuses de fonctionner.
- La musique d'un personnage peut se reconfigurer musicalement selon l'intimité ; pas nécessaire pour le prototype initial.

## Priorité des assets pour la tranche 7 jours

1. **Une chambre réutilisable** : bureau/CRT, lampe, lit, piles de CD, fenêtre vers les feuillages.
2. **Un tronçon de rue** : arbres d'automne, trottoir, lampadaire sodium, porte du diner, panneau de ville.
3. **Un diner compact** : deux banquettes, table, comptoir, fenêtre pluvieuse, éclairage doux.
4. **Un PNJ 3D** (Hannah) et **un portrait 2D** d'au moins deux expressions ; un joueur simple 3D.
5. **Son** : pluie, vent, bruit de diner, bourdonnement PC, boucle folk originale ou silence si indisponible.
6. **Interface** : agenda ivoire/brun, dialogue sobre, navigateur 2003 crédible.

**Ne pas chercher des centaines d'assets d'un coup.** Créer une première image représentative forte, puis décliner une grammaire de formes cohérente.

## Contrôle qualité artistique

À vérifier à chaque livraison : lumière chaude convaincante sans saturation excessive ; une scène de rue immédiatement reconnaissable ; PC clairement daté 2003 ; dialogue lisible ; personnage 2D/3D qui paraît appartenir au même univers ; ambiance qui fonctionne même sans « événement paranormal ».

## Pipeline 3D à utiliser comme référence de production

Voir `17_PIPELINE_ASSETS_3D.md` : kit modulaire procédural sous Blender, sources `.blend`, exports `.glb` vers Godot ; `18_RIGGING_ANIMATION.md` : un personnage pilote, animations réutilisables ; `19_QUALITE_ASSETS.md` : contact sheets + captures en moteur. **Les concept arts ne fixent pas un budget de triangles ni une topologie**. Viser leurs couleurs, silhouettes et cadrages, pas une densité de détails impossible pour une petite équipe.
