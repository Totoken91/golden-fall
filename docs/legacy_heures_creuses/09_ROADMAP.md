# 09 — Roadmap et backlog priorisé

## État V0.14

La chambre PSX, le PC physique et les passes météo/assets sont livrés dans une scène de revue séparée. La première journée historique décrite ci-dessous existe encore, mais son intégration dans cette présentation reste à faire. Le suivi actuel et l'ordre recommandé sont dans `23_ETAT_PROTOTYPE_ET_PROCHAINES_ETAPES.md`. Les cases de semaine ci-dessous décrivent le backlog de P0, pas l'absence de tout composant existant.

## État historique V0.6

La première journée intermédiaire est jouable et testée : lancement, deux créneaux, trois espaces provisoires, dialogue à portrait, mémoire, PC/recherche et sauvegarde. Les cases ci-dessous portent sur la **semaine complète** et ne sont pas automatiquement cochées par cette livraison. L’anomalie et les essais humains de rythme restent à réaliser.

## Phase 0 — Préparation (livraison actuelle)

- [x] Vision et décisions validées documentées.
- [x] Recherche Tokimeki jointe et différenciée de l'original.
- [x] Boucle nouvelle version décrite.
- [x] UX 2D / 3D clairement définie.
- [x] Exemple de données extensibles et validateur.
- [ ] Décider du pipeline final d'illustration/3D à partir d'une **capture prototype réelle**.

## Phase 1 — FIRST PLAYABLE 7 JOURS : à donner à Codex maintenant

- [ ] `P01` Créer projet Godot 4.x lançable, résolution 16:9, menu « Continuer / Nouveau » minimal.
- [ ] `P02` Implémenter `GameState` + calendrier 7 jours + journal de debug.
- [ ] `P03` Activités (étudier, diner, maison/PC, promenade, repos) avec coûts et choix temporel.
- [ ] `P04` Chambre 3D golden autumn et transition vers segment de rue/diner 3D.
- [ ] `P05` Déplacement première personne PSX + interaction PNJ 3D.
- [ ] `P06` Dialogue avec portrait 2D de Hannah, deux expressions, deux choix persistants.
- [ ] `P07` Mémoire sociale et journal 2D consultable.
- [ ] `P08` PC CRT 2003 + moteur local + cinq pages + indice historique.
- [ ] `P09` Anomalie discrète dans la rue + conséquences si observée.
- [ ] `P10` Sauvegarde/reprise et tests des enchaînements.
- [ ] `P11` Polissage : pluie, éclairage, son, typographie, aucune UI générique.

**Dépendances :** P01→P02→P03 ; P04→P05→P06 ; P02+P06→P07 ; P02+P07→P08/P09 ; P10 fin de chaîne. Le polissage doit commencer dès P04.

## Phase 2 — 14 jours

- [ ] Deuxième PNJ disponible en routine.
- [ ] Invitation / initiative PNJ et une conséquence de disponibilité.
- [ ] « Quelqu'un dans le jardin » : vraie mise en scène en 3D.
- [ ] Forum local/archives Web avec deux pistes et contradiction cohérente.
- [ ] Une petite épreuve d'enquête à solutions multiples.

## Phase 3 — Acte d'automne (6 semaines)

- [ ] Trois PNJ avec arcs distincts, choix d'amitié et de romance facultative.
- [ ] Quelques activités de club et travail, vrais arbitrages.
- [ ] Lisière de forêt, deux lieux additionnels, un concert local.
- [ ] Vie sociale réactive, conversations basées sur souvenirs.
- [ ] Enquête ouverte avec plusieurs pistes qui convergent sans tout expliquer.
- [ ] Test de rejouabilité sur au moins deux stratégies différentes.

## Phase 4 — Automne complet

- [ ] Étendre après preuve que le rythme fonctionne, jamais juste pour allonger.
- [ ] Réécrire les événements moyens, pas seulement ajouter des scènes.
- [ ] Production des portraits, musiques originales, bruitages et assets.
- [ ] Localisation, sauvegardes robustes, accessibilité, QA, distribution.

## Livraison de fin d'étape

Codex remet `DEVLOG.md` à jour : builds/fichiers modifiés, instructions lancement, tests, éléments réels versus provisoires, dette technique, captures si possible, trois problèmes de design constatés, prochaine priorité. Ne jamais dire « terminé » si un test central échoue.

## Volet transversal « pipeline d'assets » (ne remplace aucune phase)

- [x] **A00** Décrire production Blender/Codex/Godot, alternatives de rigging et QA dans les docs 17–20 ; scripts de démonstration livrés en V0.5.
- [ ] **A01** Exécuter `generate_streetlamp.py` dans Blender installé localement, inspecter le `.glb`, tester l'échelle dans Godot ; conserver une capture.
- [ ] **A02** Décliner une deuxième famille : banquette de diner ou module de façade ; produire deux variantes à partir d'un générateur.
- [ ] **A03** Construire ou importer UN personnage pilote cohérent avec un portrait 2D, puis Idle/Walk dans Godot ; valider le rig.
- [ ] **A04** Ajouter un clip assis et un petit geste de dialogue ; tester le retargeting avant de généraliser.
- [ ] **A05** Générer des contact sheets et journaliser métriques/performance sur les décors P0.

**Garde-fou :** la P0 ne doit pas attendre A03–A05 pour être jouable. Pas de casting complet, pas d'API payante ni d'autorig « magique » en premier sprint.
