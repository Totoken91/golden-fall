# État technique courant — V0.14, 9 octobre 2026

Plafond de travail chambre/extérieur/pluie : 8 000 triangles, révisable ; résultat livré : 7 250 + 720 = 7 970. Ce chiffre remplace le plafond de 16 000 de la passe V0.10 ci-dessous. Veste toujours retirée, CRT physique Cedar 03 conservé. Passe de supports et contacts, mobilier rapproché du mur, rideaux dégagés, ventilation en texture et pluie à 360 gouttes indépendantes. Sources et limites dans `22_GUIDE_CREATION_ZONES.md`.

La chambre de revue ne sauvegarde pas une campagne. Les systèmes de la première journée restent dans la scène historique ; leur raccordement est une priorité proposée, pas une fonctionnalité livrée. Voir `23_ETAT_PROTOTYPE_ET_PROCHAINES_ETAPES.md`. Les sections suivantes constituent l'historique des décisions et ne réactivent ni la veste ni les anciens budgets ou caméras.

# V0.10 — Retrait de la veste et budget

Veste retirée à la demande explicite de l’utilisateur. Budget de projet fixé à 16 000 triangles pour la chambre et tout son extérieur, hors maillages procéduraux de pluie. Objectif de style et de discipline de production, sans émulation ou certification PS1. Sac : rabat conformé aux facettes et sangle plate ; boucles et coutures dans la texture. Pas d’agrandissement des textures.

# V0.9 — Accessoires de la chambre

Veste de travail en velours côtelé tabac, ouverte sur le dossier ; choix visuel à tester, pas nouvelle biographie validée. Pans et manches modélisés, sans simulation de tissu. Clavier, tasse en grès et sac souple remodélisés. La composition, les lumières et la météo de V0.8 sont conservées. Aucun service de génération externe utilisé.

# Journal des décisions de prototypage (non validées par l'utilisateur)

Codex : ajouter ici chaque choix effectué pour construire le prototype lorsqu'il n'est pas explicitement validé dans `docs/00_DECISIONS.md`, avec date, motif, conséquence, réversibilité et alternative rejetée. Ne jamais reclasser automatiquement un choix technique en canon narratif.

## 2026-10-09 — V0.8, passe ciblée autorisée

- **Demande humaine :** conserver la scène et le cadrage qui commencent à fonctionner ; améliorer extérieur, lumière, literie, matières, détails personnels, pluie animée et manteau qui traverse la chaise. Livrer capture identique en cadrage et vidéo courte.
- **Invariants :** même scène fermée, mobilier principal aux mêmes emplacements, caméra de comparaison à partir de `(-1.68,.03,2.30)` vers `(-.05,.95,-1.45)`, FOV vertical 62°, monde 640×360, sortie 1280×720. La capsule se pose sur le même sol avant la capture.
- **Extérieur :** premiers troncs à environ 14 m de la vitre, sous-bois à plusieurs distances et brume calculée dans les seuls matériaux extérieurs. Clôture discrète de premier plan, sans nouveau lieu explorable.
- **Météo :** trois plans de pluie derrière la fenêtre, ruissellement sur la vitre et vent discret du feuillage. Horloge explicite pour geler la météo à 2 s lors des captures comparables ; elle tourne normalement en jeu et en vidéo.
- **Lumière :** ambiance plus faible, chevet localisé, lumière de fenêtre directionnelle avec ombres et faible rebond. Palette tabac, cuivre, ivoire usé et gris extérieur conservée.
- **Modèles :** couverture maillée avec bords hors du matelas, oreillers pincés/cousus ; manteau passant au-dessus de la traverse, manches et revers. Deux contrôles d'intersection géométrique avant export.
- **Détails :** photos de paysage originales, cassette annotée et casque. Propositions de décoration, pas une biographie du protagoniste ni du nouveau lore.
- **Vidéo :** capture du moteur avec caméra automatisée dans la scène, 30 images/s imposées pour l'export, environ 21 s ; cela ne sert pas de benchmark de fluidité en temps réel.

## 2026-10-09 — Chambre V0.7 PSX, proposition après rejet

- La direction est tirée du pack PSX fourni ; l'acceptation du nouveau résultat appartient au porteur de projet.
- Nouvelle scène `room_review.tscn`, caméra à 1,62 m, champ vertical de 62°, marche 1,85 m/s, monde 640×360 agrandi en nearest et UI native. Réglages à revoir sur ressenti de jeu.
- Chambre originale sous Blender : environ 5,6 × 5,8 m, table 0,77 m, porte 2,20 m. UV, textures 128/256 px, CRT à coque effilée, couverture maillée et rideaux plissés. Le mobilier est une proposition de décor, sans ajout de canon narratif.
- Lampe locale ambre, remplissage de fenêtre gris, lumière réfléchie faible ; pas de bloom. Décor extérieur limité à des arbres en géométrie/cartes de feuillage derrière la fenêtre.
- La scène démarre dans une session de revue indépendante le soir. PC/recherche et notes utilisent les classes existantes ; quitter efface cette session. Le lit ouvre une pause narrative courte et la porte reste fermée. Le calendrier et la sauvegarde de la première journée restent dans la scène historique `main.tscn`.
- Aucun service payant ou envoi d'assets. Géométrie et textures créées localement, source `.blend` et générateurs fournis. Le concept cible n'est pas réutilisé comme texture ou fond.
- Rue, diner, PNJ et portraits n'ont pas reçu cette refonte. Aucun changement aux JSON corrigés.

## 2026-10-09 — Première journée V0.6

- **Périmètre autorisé :** le porteur de projet valide les corrections et la priorité « première journée complète ». Les sept jours sont reportés à l’étape suivante ; aucune nouvelle décision de lore n’est verrouillée.
- **Moteur :** Godot 4.6 portable, renderer Compatibility, pour tester effectivement la 3D et les UI sur cette machine. Réversible ; l’absence de Godot installé ne justifie pas une substitution par un jeu Web.
- **Temps :** lundi 13 octobre, une action principale après les cours puis une soirée ; quitter la session consomme le créneau. Les coûts sont appliqués une fois à l’ouverture, les menus restent gratuits. Le coucher termine l’essai au réveil suivant.
- **Accroche jour 1 :** demander les sujets photographiques de Hannah ouvre une petite conversation sur une photo de la route de Black Alder. La cassette conserve sa date future ; la nouvelle scène remplace provisoirement son rôle d’amorce pour ce jalon. Alternative : annonce au diner et annuaire municipal.
- **Image :** caméra orthographique à la troisième personne, monde en primitives et portraits SVG originaux pour vérifier composition et lisibilité. Réversible ; aucun de ces visuels ne définit l’apparence finale du protagoniste ou du casting. La marche n’est pas une animation de rig approuvée.
- **Son :** deux ambiances synthétiques locales, aucune API ; musique finale reportée. Les sources de régénération sont incluses.
- **Sauvegarde :** v2, migration de l’exemple v1, session et dialogue sauvegardés ; dernière page du navigateur non restaurée automatiquement, historique de recherches conservé.
- **Distribution :** binaire officiel Godot renommé + PCK, solution portable plus lourde qu’un export final. Pas d’installation système ni de paiement.

## V0.12 — Choix de réalisation, 9 octobre 2026

Demandes humaines : alléger les assets tout en conservant leur qualité et le PSX de la deuxième image ; vrai PC physique avec caméra rapprochée et OS fictif époque XP ; pluie plus forte/moody ; audio fourni. Choix techniques de réalisation : budget chambre+extérieur 8 000 triangles, modèle final 6 680 ; viewport PC 640 × 480, FOV 40° pendant l'interaction/62° au retour ; palette propre à Cedar 03, originaux des posters conservés ; WAV mono 22 050 Hz avec fondu de deux secondes et crête −3 dBFS. Ces paramètres ne sont pas de nouvelles décisions créatives validées pour toutes les futures zones.

## V0.13 — Réalisation de l'extérieur

Demande humaine : améliorer qualité extérieure, densité de forêt et pluie. Choix de réalisation : 90 arbres répartis sur trois profondeurs, 28 groupes de sous-bois, deux masses lointaines et ciel procédural quantifié ; sept nouvelles textures, modèle complet 7 406 triangles sous le cap de travail 8 000. Pluie sur les trois plans existants avec variations par goutte, ruissellements irréguliers, sol humide stylisé. Ces choix sont soumis au retour artistique, sans validation de nouveaux lieux ou de nouveaux éléments de lore.
