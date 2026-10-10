# 16 — Continuité de développement avec Codex

**Mise à jour V0.14 — 9 octobre 2026 :** lire `AGENTS.md`, `22_GUIDE_CREATION_ZONES.md` et `23_ETAT_PROTOTYPE_ET_PROCHAINES_ETAPES.md` à chaque reprise. Direction courante : PSX / première personne / golden brown, CRT physique, contacts vérifiés et pluie indépendante. Chambre et extérieur : 7 250 triangles de modèle + 720 de pluie = 7 970. Le guide consigne les apprentissages ; le document 23 distingue la scène de revue, la première journée historique et les étapes futures. Mettre ces documents à jour avec les résultats réels.

## Quand on reprend le projet dans une autre conversation

Pour recharger le contexte, remettre à Codex **ce dossier complet** ou son dépôt Git, puis demander d'ouvrir `AGENTS.md`, `docs/00_DECISIONS.md`, `DEVLOG.md` et la livraison en cours. Les documents font foi ; éviter la mémoire orale du développeur.

## Processus Git conseillé

- Branche `main` pour les étapes fonctionnelles ; une branche par tranche (`prototype/p0-agenda`, `prototype/p0-3d`, etc.).
- Commits petits et nommés d'après un résultat (`feat: agenda consumes action slot`).
- Ne pas mélanger réécriture du lore, nouveaux modèles 3D et refactor technique dans le même changement.
- `DEVLOG.md` à chaque livrable ; `docs/DECISIONS_TEMPORAIRES.md` pour tout compromis non validé.
- Inclure captures et métriques de tests quand elles existent réellement ; ne pas inventer le résultat d'un build.

## Règle de dialogue avec le porteur du projet

Présenter chaque nouvelle direction créative comme **proposition**. Les décisions validées ne changent que par son accord. En particulier : portraits 2D sur environnement 3D, un automne en 2003, golden autumn gothic, horreur ambiguë et dominante Mystery Life Sim.

## Dette volontaire

- Noms et personnages prototypes, encore révisables.
- Interface du navigateur fictif sans branding définitif.
- Vitesse de progression stats et relations à équilibrer.
- Cohérence PSX à vérifier dans les futures zones et avec les personnages ; la chambre dispose déjà de captures réelles et de mesures techniques.
- Routes finales, calendrier exact, identité du protagoniste ouverts.

## Plus tard, on pourra demander à Codex

« Étends le prototype P0 validé à P1 en respectant `docs/09_ROADMAP.md`. Garde toutes les décisions de `docs/00_DECISIONS.md`, ajoute les tests, mets à jour DEVLOG. N'implémente pas P2. »

## Continuité du pipeline d'assets (V0.5)

Les règles d'assets sont dans `docs/17_PIPELINE_ASSETS_3D.md` à `docs/20_INSTALLATION_OUTILS.md` ; les sources `.blend`, exports `.glb`, infos de licence et statut vivent dans `assets/`. Le premier objet est uniquement `planned` dans `assets/asset_manifest.json`. Ne pas avancer son statut à `approved` sans capture en jeu. Toute nouvelle version conserve les générateurs et vérifie que les imports Godot n'ont pas cassé la scène existante.
