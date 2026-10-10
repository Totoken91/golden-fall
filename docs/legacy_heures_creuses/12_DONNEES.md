# 12 — Contrats de données du starter pack

Fichiers de `game/data/` (source unique depuis V0.21) = **exemples fonctionnels**, pas scènes totalement implémentées. Ils portent des IDs stables pour servir de base au projet Godot.

## `characters.json`

Chaque personnage : `id`, `name`, `role`, `home_location`, `hangout_locations`, `likes`, `dislikes`, `base_relationship` (friendship/trust/resentment/attraction), `memory_keys`, `bio`, `portrait_states` ; `romance_available` indique une option future, pas une route existante.

## `locations.json`

`id`, `display_name`, `mode` (`3d` / `2d`), `description`, `unlock_flags` et `mood_tags`. Des lieux peuvent exister sans scène 3D en P0, indiquer `phase`.

## `activities.json`

`id`, `label`, `availability`, `mode` (quick / scene / pc), `location`, `cost_slots`, `stat_deltas`, `effects`, `phase`. Deltas arbitraires à équilibrer par playtest.

## `dialogues.json`

`id`, `npc`, `location`, `conditions`, `lines`, `choices` avec `id`, `text`, `effects`, `next` facultatif ; ne jamais donner des récompenses deux fois.

## `events.json`

`id`, `title`, `location`, `slot`, `priority`, `once`, `conditions`, `effects`, `dialogue_id`, `phase`, `alternative_access`. L'EventDirector doit contrôler et journaliser les déclenchements.

## `web_pages.json`

`id`, `url` fictive, `title`, `date`, `tags`, `synonyms`, `body`, `links[]` (`page_id`), `clue_id` optionnel, `requires_flags` facultatif. Le rendu des pages se fait localement.

## `save_example.json`

Format d'exemple de sauvegarde ; **ne pas le charger comme partie authentique sans adaptation du moteur**.

## Scripts de validation

À la racine du pack :

```bash
python scripts/validate_content.py
python -m unittest discover -s tests -v
```

Ils vérifient la **structure et les références** des données fournies, pas le fonctionnement du moteur 3D. Codex devra compléter par des tests Godot jouables et automatiques.

## Évolution des données

Ne pas faire dépendre la sauvegarde de l'ordre des entrées d'un tableau. Maintenir IDs stables, `save_version`, migrations et log des décisions. Les textes sont français ici ; la fiction peut présenter interfaces et recherches anglo-américaines si cohérent, mais la localisation doit rester data-driven.

## Contrat V0.6 — première journée

- `definitions.json` déclare les statistiques (`stamina` pour l’endurance), bornes, créneaux, routes alternatives et libellés de souvenirs.
- Jour d’essai : lundi 13 octobre 2003. Une action principale après les cours, puis une action du soir ; `night` marque la fin des actions. Le week-end réutilise `weekend_afternoon` puis `evening`.
- Ouvrir l’agenda/journal, sauvegarder et marcher dans le hub ne consomme pas de temps. Commencer une activité applique ses coûts une fois et crée une session ; la quitter consomme le créneau. Une même conversation ne se répète pas dans cette session.
- Le PC constitue une activité du soir ; requêtes, navigation et notes ne coûtent pas de créneau supplémentaire. Un indice est ajouté explicitement au journal ; ouvrir sa page conserve seulement visite et flags associés.
- `min_relationship` et `max_relationship` portent des seuils par personnage et variable ; `memory_age_days` exige un souvenir effectivement acquis depuis le nombre de jours indiqué.
- Sauvegarde v2 : souvenirs datés avec source, historique des recherches, favoris, session et état de fin de tranche. Migration v1 : `endurance` est renommé `stamina` si nécessaire ; valeurs manquantes complétées.
- La livraison jouable actuelle s’arrête au réveil suivant la première journée. Les données des jours suivants préparent P0, mais ne constituent pas une semaine déjà jouable.
