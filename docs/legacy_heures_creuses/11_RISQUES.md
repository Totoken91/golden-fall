# 11 — Risques, arbitrages, garde-fous

## 1. Trop de genres à la fois — RISQUE ÉLEVÉ

**Parade :** un jeu de gestion du temps et de rencontres, dont l'enquête se fait via les mêmes actions et lieux ; horreur par événements rares. Pas de système de survie autonome.

## 2. Trop de 3D — RISQUE ÉLEVÉ

**Parade :** 3 zones pour P0, chargées séparément ; déplacement facultatif pour activités répétitives. Toute nouvelle zone doit offrir interactions/événements récurrents ou une scène majeure indispensable.

## 3. Portraits 2D déconnectés de la 3D — RISQUE MOYEN

**Parade :** palette commune, tenue identique, même silhouette, compositions cohérentes, un personnage pilote avant le reste du casting.

## 4. Internet fictif qui ressemble à un wiki à quêtes — RISQUE ÉLEVÉ

**Parade :** contenus banals, articles imparfaits, pages datées, liens hors-sujet, recherche par mots naturels. Aucun « indice découvert » pour chaque clic.

## 5. Horreur tellement omniprésente qu'elle tue la détente — RISQUE ÉLEVÉ

**Parade :** peur d'arrière-plan et malaise environnemental quasi continus, mais **véritables scènes chaleureuses non sabotées**. La peur vient du contraste et du souvenir.

## 6. Autre piège : le « générateur de lore incohérent »

**Parade :** faits prouvés, rumeurs et hypothèses séparés. Matrice d'événements. Une anomalie peut être inexplicable, mais pas arbitraire.

## 7. Trop d'assets saisonniers

**Parade :** un seul automne 2003. Diversité par météo/heure, pas par 4 saisons. L'immobilité automnale est aussi un thème.

## 8. Copie d'œuvres et marques connues

**Parade :** *Tokimeki* comme inspiration systémique ; *Twilight* comme inspiration mood ; pas de personnages, dialogues, designs, titres, musiques ou logos repris. Le navigateur 2003 est fictif, pas une réplique distribuée de Google/Windows.

## 9. Rendu générique « AI slop »

**Parade :** bible palette/matériaux, prototype artistique très petit mais fini, arrêt des fonctionnalités si la rue et la chambre ne sont pas déjà convaincantes. Ne pas masquer la pauvreté d'une scène par des tableaux UI.

## 10. Trame verrouillée sur un seul choix

**Parade :** indices essentiels avec deux voies d'accès ; conséquence réelle si raté, mais progression minimale toujours possible. Pas de soft-lock à 80 % d'une partie.

## Arbitrages de portée déjà faits

| À conserver | À reporter / couper |
|---|---|
| Temps, relations, mémoire, indices | Faim, soif, craft, combat |
| Chambre / rue / diner | Open world et conduite |
| Portrait 2D d'un PNJ | Portraits du casting entier |
| 5 pages Web fonctionnelles | Internet fictif infini |
| 1 anomalie forte | Bestiaire, boss, 20 jumpscares |
| 7 jours rejouables | 3 ans de simulation |

## 11. Industrialisation 3D trop précoce — RISQUE ÉLEVÉ

**Parade :** preuve minimale par un lampadaire + une banquette, personnage pilote ensuite. Faire fonctionner le calendrier, les dialogues et la rue en greybox avant d'élargir le pipeline.

## 12. Auto-rig/IA 3D incohérents — RISQUE ÉLEVÉ

**Parade :** Mixamo et Rigify = procédures avec intervention/QA ; Meshy/Tripo = options externes soumises à licences, coûts et restrictions. Garder une base humanoïde et un squelette commun. Tester Godot réellement, ne jamais déclarer « riggé/animé » sur la seule base d'une API.

## 13. Outillage MCP avec exécution de code — RISQUE DE SÉCURITÉ

**Parade :** MCP for Blender tiers, local et facultatif ; ne pas permettre scripts externes ni télécharger des assets/licences à l'aveugle. Éviter les clés dans le dépôt. Usage de crédits externes uniquement après autorisation explicite.
