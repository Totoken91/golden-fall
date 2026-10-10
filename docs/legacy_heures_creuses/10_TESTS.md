# 10 — Critères d'acceptation du prototype

## A. Jeux de bout en bout

**T01 — Une journée complète.** Nouveau jeu → voir la date → choisir une activité → en constater le coût → entrer dans la chambre → aller se coucher → date suivante. Aucune erreur ni calendrier bloqué.

**T02 — Deux types d'action.** Une activité rapide passe directement au résultat ; une visite au diner ouvre une zone 3D et revient à l'agenda correctement.

**T03 — Une vraie rencontre.** Parler à Hannah sur le décor 3D affiche un **portrait 2D**, un dialogue et un choix. La deuxième conversation diffère grâce à une mémoire acquise, pas seulement à la date.

**T04 — Recherche utilisable.** Approcher le CRT, ouvrir le faux navigateur, saisir « black alder », « mill », « scierie » ou un synonyme ; trouver l'archive, suivre un lien et noter un indice. Recherche sans réseau réel.

**T05 — Choix signifiant.** Choisir d'interroger Hannah sur la cassette doit rendre disponible un dialogue ou une recherche autrement absente ; un autre choix conserve une voie d'accès alternative à l'enquête.

**T06 — Horreur subtile.** Une silhouette lointaine apparaît en condition définie, le joueur peut observer/ignorer, les deux actions modifient légèrement le journal ou la conversation suivante. Aucun jumpscare imposé.

**T07 — Sauvegarde.** Après 4 jours de jeu, quitter et recharger → même date, valeurs, indices, relations, lieux et statut des événements ; une scène `once` ne rejoue pas.

**T08 — Rejouabilité.** Deux passages de 7 jours avec des choix différents déclenchent au moins une scène/variante différente sans casser le fil rouge.

**T09 — Rythme.** Possibilité de terminer une journée banale rapidement. Ni déplacement obligatoire vers trois lieux pour étudier, ni conversation répétée imposée.

**T10 — Mood.** Sans dialogue horrifique, la scène de chambre/rue donne déjà la sensation automne 2003 : lumière, matériaux, pluie, sons et CRT crédibles. Test humain indispensable.

## B. Contrats de données

- JSON valide, IDs uniques dans chaque collection, `dialogue_id` et `location` existants.
- Aucun événement principal inaccessible sans autre moyen (`fallback` / `alternative_access`).
- Dates au format ISO 2003 cohérentes, un seul automne.
- Variables de relation initialisées et bornées ; deltas appliqués une seule fois.
- Pages Web : aucun lien interne cassé ; termes de recherche naturels réellement indexés.
- Journal : pas de souvenir non vécu par le joueur.

## C. Scénarios négatifs

- Revenir dans la scène 3D ne redonne pas gratuitement de l'affection ni l'indice.
- Cliquer rapidement deux fois sur un choix ne double pas les effets.
- Chercher un mot inexistant n'affiche pas un indice générique.
- Quitter le PC puis le rouvrir conserve historique/flags ; retour caméra/chambre fiable.
- Aucun PNJ ne mentionne « notre discussion d'hier » si elle n'a pas eu lieu.
- L'anomalie reste une scène inquiétante même si le joueur regarde dans une autre direction.

## D. Budget / performance cibles pour test (provisoires)

- PC standard avec GPU raisonnable ; 60 fps cible, 30 fps plancher pendant les panoramiques (à réviser selon matériel).
- Chargement d'une petite zone sans attente longue, animations fluides, textes instantanément lisibles.
- Pas de dépendance serveur ni clé API.
- Aucun asset protégé/copieux depuis des jeux ou films existants.

## Critère de sortie de phase

Les tests T01–T08 sont reproductibles sans mode debug ni édition manuelle des sauvegardes. T09/T10 sont validés en vrai playtest. Le validateur JSON passe.

## E. Pipeline d'assets (ajout V0.5 — tests distincts)

- **A01** : générateur Blender produit `.blend` + `.glb` avec origine stable ; **non vérifié tant que Blender n'a pas été exécuté**.
- **A02** : `inspect_glb.py` accepte un conteneur GLB valide et rejette un fichier tronqué. Ceci n'est qu'un *smoke test*, pas un validateur glTF complet.
- **A03** : `validate_manifest.py` distingue correctement planifié/généré/approuvé ; les chemins d'un asset généré doivent exister.
- **A04** : un aperçu Godot réel prouve une échelle crédible, une orientation correcte, la tenue des textures et de la lumière.
- **A05** : pour un personnage animé, captures Idle/Walk en jeu sans déformation majeure ni patinage visible.
- **A06** : assets tiers avec origine/licence documentées et aucune clé API ajoutée au dépôt.

Les A02/A03 sont automatisables sans Blender ; A01, A04 et A05 **nécessitent les applications correspondantes** et ne sont pas marqués comme réussis par défaut.
