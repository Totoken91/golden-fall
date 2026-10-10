# 07 — Architecture technique recommandée (Godot 4.x)

## Pourquoi Godot ?

Petit projet hybride avec zones 3D, UI 2D, JSON data-driven, PC simulé et rapidité d'itération. **Choix technique recommandé, non imposé par l'utilisateur.** Si le projet est porté sous Unity, conserver la même séparation conceptuelle et les mêmes IDs de données.

## Arborescence cible (à produire par Codex)

```text
game/
  project.godot
  scenes/
    main.tscn
    world/bedroom.tscn
    world/main_street.tscn
    world/diner.tscn
    actors/player.tscn
    actors/hannah.tscn
    ui/agenda.tscn
    ui/dialogue_portrait.tscn
    ui/pc_desktop.tscn
    ui/pc_browser.tscn
    ui/journal.tscn
  scripts/
    core/game_state.gd
    core/calendar.gd
    core/action_resolver.gd
    core/event_director.gd
    core/relationship_system.gd
    core/memory_log.gd
    core/web_archive.gd
    core/save_manager.gd
    ui/... ; world/...
  data/  # copie ou chemin d'import explicite depuis ../data
  assets/
    environment/ portraits/ audio/ ui/
```

À côté de `game/`, la chaîne de production conserve des fichiers séparés `assets/source_blender/`, `assets/exported/`, `assets/asset_manifest.json` et `scripts/assets/`. Le jeu Godot référence les `.glb` via une scène de composition/héritage ; l'import 3D et l'animation sont traités dans les docs 17–20.

Cette structure est une **cible**, pas une liste de scènes déjà codées dans ce pack.

## États à garder cohérents

```text
GameState
  date: "2003-10-13"                      # date d'essai possible
  day_slot: "after_school" | "evening"
  stats: {social, observation, practical, stamina, fatigue, stress, cash}
  relationships: {hannah: {friendship, trust, resentment, attraction, memories}}
  flags: ["met_hannah", "hannah_mentions_tape", ...]
  clues: ["mill_archives_1978", ...]
  visited_pages: ["history_mill", ...]
  seen_events: ["...", ...]
  active_location: "bedroom" | "main_street" | "diner"
  seed: entier  # variations reproductibles
```

`game/data/save_example.json` montre un snapshot de travail. Ne pas confondre modèle de sauvegarde et contenu canonique.

## Responsabilités

| Service | Responsabilité |
|---|---|
| `GameState` | Source unique d'état, flags et valeurs ; exposer signaux de changement |
| `Calendar` | Passages de jour/slot, limites d'activités, événements prévus |
| `ActionResolver` | Coûts/gains d'activités, disponibilité, effets différés |
| `RelationshipSystem` | Liens, mémoire partagée, contrôle des conditions de dialogue |
| `MemoryLog` | Observations vécues datées, contradictions, indices acquis |
| `EventDirector` | Déterminer événements admissibles, priorités, cooldowns, once-only |
| `WebArchive` | Recherche textuelle locale, pages fictives, flags d'accès |
| `SaveManager` | Versionner, sérialiser, charger, migrer sauvegardes |

Les scènes 3D sont **des vues/contrôleurs** qui délèguent les changements d'état ; elles ne dupliquent pas des états cachés différents du `GameState`.

## Événements data-driven

Les fichiers `game/data/events.json` servent d'exemples. Chaque événement :

- `id` stable ; `location` et `slot` ; `conditions` composables ; `once` ; `priority` ; `effects` ; `dialogue_id` ; `fallback` ou `alternative_access` lorsqu'un indice principal est nécessaire.
- **Conditions** : flags, date, stats, relation, indices, lieu, jour.
- **Priorité** : événement majeur > social contextualisé > ambient ; mais ne pas déclencher automatiquement un événement dangereux si le joueur ne fait que consulter l'agenda.
- **Idempotence** : un événement `once: true` ne se reproduit pas après chargement ou réentrée dans une zone.
- **Reproductibilité** : événements stochastiques seulement avec seed consignée, pas `random()` caché dans dix scripts.

## Dialogues data-driven

- IDs stables, lignes, locuteur, expression de portrait optionnelle, choix, conditions, effets.
- Les choix affectent données **à la fin d'une option validée** ; retour scène 3D après sortie.
- Les variations utilisent les souvenirs réellement acquis ; jamais de référence à un souvenir absent.
- Chaque personnage ne devient romantique que si le joueur fait un choix explicite ; amitié et confiance ont leur propre trajectoire.

## Recherche Web locale

- Index construit à l'initialisation depuis les `game/data/web_pages.json` (ne pas appeler Google).
- Normaliser texte unicode, accents, majuscules, espaces et ponctuation ; score titres > tags > corps.
- Aucun indice unique ne peut être verrouillé derrière une formulation exacte : synonymes et double entrée par dialogue.
- Pages consultées enregistrées ; HTML enrichi optionnel, **sanitiser toute entrée** ; ne pas implémenter un vrai navigateur Web complet si une UI de pages suffit.

## Temps et scènes

- Activité de gestion → appliquer delta et consommer slot, sans téléportation abusive pour joueur qui visite une scène.
- Entrée en zone 3D → instancier éléments selon date et flags, sans modifier les relations à la simple entrée.
- Dialogue → choix → `GameState` mis à jour une fois → mémoire datée si pertinent.
- PC → recherche et navigation, action « sauvegarder dans le journal » explicite ; retour chambre.
- Fin de soirée → `Calendar.advance()` → résolution d'événements calendaires → autosave facultatif.

## Données et sauvegardes

- Stocker horodatage, version de schéma (`save_version`), IDs stables et seed.
- Éviter les chemins de scènes dans les fichiers de sauvegarde ; `location_id` abstrait.
- Un `load` doit toujours reproduire date, actifs, dialogue et disponibilité.
- Prévoir une solution pour **recharger une sauvegarde antérieure à un changement de données** (migration, valeurs par défaut).

## Architecture de test

- Scripts hors jeu `scripts/validate_content.py` vérifient JSON : IDs uniques, références et contrat minimal.
- Tests Godot (à ajouter par Codex) : progression calendrier, coûts d'action, flags, disponibilité, priorité d'événements, absence de répétitions, préservation des relations par sauvegarde.
- Debug overlay : date/slot, flags, relation avec Hannah, page visitée, événement déclenché (désactivé en build joueur).
- Essais manuels : enchaînement de 7 jours, recherche, revenir au diner, charger sauvegarde, regarder l'anomalie, repérer une incohérence.

## Priorités du code

1. Calendar/GameState et tests ; 2. scène chambre+rue de test ; 3. action à coût ; 4. dialogue avec portrait ; 5. memory/event ; 6. web ; 7. save ; 8. habillage artistique solide et polissage. Ce n'est **pas** une invitation à repousser le mood visuel après toute la technique : dès le premier écran, les lumières et couleurs doivent être représentatives.
