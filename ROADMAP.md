# Epic Events CRM — Roadmap de développement

## Objectif
Créer une application CRM sécurisée en ligne de commande (Python 3, sans Django), gérant collaborateurs, clients, contrats et événements, conformément au cahier des charges Epic Events.

## Méthode de travail
Pour chaque jalon : (1) préciser le périmètre et les critères d'acceptation, (2) développer et tester sur une branche dédiée, (3) contrôler `git status` et les tests, committer puis fusionner dans `main`, (4) rédiger une fiche de révision dans `docs/revisions/`, (5) actualiser cette roadmap. Les fiches de révision font partie du jalon et doivent être incluses dans le commit ou dans un commit de documentation avant fusion.

## Stack envisagée
Python 3, Poetry, PostgreSQL, SQLAlchemy, Alembic, Click, Rich, Argon2, pytest, pytest-cov, Sentry, Black/Ruff, Git/GitHub. Choix à valider au jalon 1 ; PostgreSQL et les bibliothèques ne sont pas tous imposés par les sources.

## Jalons

### J1 — Initialisation et environnement
Branche : `chore/setup-project`
- [ ] Créer dépôt GitHub, README initial, `.gitignore`, structure de projet.
- [ ] Configurer Python, Poetry et dépendances.
- [ ] Installer/configurer PostgreSQL et un utilisateur non privilégié.
- [ ] Configurer `.env.example`, variables d'environnement, secrets exclus de Git.
- [ ] Vérifier la connexion SQLAlchemy à la BDD et ajouter un test de connexion.
- [ ] Documenter installation et commandes de démarrage.
- [ ] Fiche `docs/revisions/01-environnement.md`.
Validation : installation reproductible, connexion fonctionnelle, aucun secret suivi par Git.

### J2 — Modélisation et migrations
Branche : `feat/database-models`
- [ ] Modéliser `Role/Department`, `Employee`, `Client`, `Contract`, `Event`.
- [ ] Définir clés, cardinalités, contraintes et relations ORM.
- [ ] Couvrir champs clients (nom, email, téléphone, entreprise, dates, commercial), contrats (montants, statut, date, client, commercial), événements (contrat, nom, dates, lieu, participants, notes, support).
- [ ] Initialiser Alembic, créer et appliquer une migration.
- [ ] Produire le diagramme ERD et tester les relations.
- [ ] Fiche `docs/revisions/02-modelisation.md`.
Validation : schéma créé par migration, relations et contraintes testées, ERD à jour.

### J3 — Collaborateurs et rôles
Branche : `feat/user-management`
- [ ] Définir les trois départements : gestion, commercial, support.
- [ ] Créer le modèle de comptes avec identifiant, nom, email, rôle relationnel et mot de passe haché/salé.
- [ ] Implémenter création, modification, changement de rôle et suppression contrôlée des collaborateurs (gestion uniquement).
- [ ] Prévoir l'initialisation sécurisée d'un premier compte gestion.
- [ ] Tester validation, unicité, hachage et restrictions.
- [ ] Fiche `docs/revisions/03-collaborateurs.md`.
Validation : cycle de vie des comptes et protections vérifiés.

### J4 — Authentification et autorisation
Branche : `feat/authentication`
- [ ] Implémenter login/logout et session persistante en CLI.
- [ ] Gérer stockage sûr du jeton, expiration, invalidation et secrets.
- [ ] Centraliser les contrôles de permissions (RBAC) et de propriété des ressources.
- [ ] Garantir l'accès en lecture authentifié à tous les collaborateurs.
- [ ] Tester accès anonyme, rôle incorrect, ressource d'autrui et jeton expiré.
- [ ] Fiche `docs/revisions/04-authentification.md`.
Validation : aucun accès aux données sans authentification, droits appliqués côté logique métier.

### J5 — Lecture et filtres
Branche : `feat/read-operations`
- [ ] Lire/lister clients, contrats et événements.
- [ ] Ajouter filtres : événements sans support, événements assignés à l'utilisateur, contrats non signés, contrats impayés.
- [ ] Implémenter une couche de services/repositories séparée de la CLI.
- [ ] Tester les lectures autorisées, filtres et absence d'injection SQL.
- [ ] Fiche `docs/revisions/05-lecture.md`.
Validation : lecture globale authentifiée et filtres corrects.

### J6 — CRUD métier et règles d'accès
Branche : `feat/crud-operations`
- [ ] Commercial : créer un client automatiquement attribué, modifier uniquement ses clients.
- [ ] Gestion : créer et modifier tous les contrats ; commercial : modifier les contrats de ses clients.
- [ ] Commercial : créer un événement seulement pour un de ses clients dont le contrat est signé.
- [ ] Gestion : affecter un support et modifier les événements.
- [ ] Support : modifier uniquement ses événements assignés.
- [ ] Valider les données, relations, montants et dates ; empêcher les accès hors périmètre.
- [ ] Vérifier les opérations de suppression explicitement demandées (collaborateurs) ; ne pas inventer d'autres suppressions obligatoires.
- [ ] Tester chaque permission et les cas limites.
- [ ] Fiche `docs/revisions/06-crud.md`.
Validation : toutes les règles métier et autorisations sont couvertes par tests.

### J7 — Interface CLI
Branche : `feat/cli-interface`
- [ ] Exposer login/logout, comptes, clients, contrats et événements via Click.
- [ ] Afficher listes, détails, erreurs et confirmations avec Rich.
- [ ] Ajouter aide CLI et validations d'entrées ; ne jamais exposer de secrets.
- [ ] Tester les parcours utilisateur de bout en bout.
- [ ] Fiche `docs/revisions/07-cli.md`.
Validation : parcours complet réalisable depuis un terminal sans manipuler directement la BDD.

### J8 — Sécurité, tests et Sentry
Branche : `feat/security-logging`
- [ ] Auditer permissions, validation, injection SQL, secrets et erreurs.
- [ ] Compléter tests unitaires, intégration et parcours CLI ; mesurer couverture.
- [ ] Intégrer Sentry pour exceptions inattendues et journalisation utile.
- [ ] Journaliser créations/modifications de collaborateurs et signature des contrats si pertinente.
- [ ] Vérifier l'absence de données sensibles dans logs, événements Sentry et dépôt.
- [ ] Fiche `docs/revisions/08-securite-tests.md`.
Validation : suite de tests verte, couverture documentée, événements de test Sentry vérifiés.

### J9 — Livraison et soutenance
Branche : `docs/final-delivery`
- [ ] Finaliser README : prérequis, installation, migrations, création du premier compte, utilisation et tests.
- [ ] Fournir `requirements`/verrouillage des dépendances, `.env.example`, scripts de création des tables via migrations.
- [ ] Livrer ERD actualisé et lien GitHub.
- [ ] Préparer scénario de démonstration avec données fictives et matrice de permissions.
- [ ] Contrôler le dépôt propre, les secrets et la reproductibilité depuis un clone neuf.
- [ ] Fiche `docs/revisions/09-soutenance.md` et index des fiches.
Validation : dépôt public/partageable, installation documentée et démo reproductible.

## Matrice de permissions de référence
- Tous les collaborateurs authentifiés : lecture de tous les clients, contrats et événements.
- Gestion : CRUD collaborateurs (dont suppression), création/modification de tous les contrats, modification des événements et attribution du support.
- Commercial : création de clients avec attribution automatique, modification de ses clients, modification des contrats de ses clients, création d'événements pour ses clients ayant signé.
- Support : modification des seuls événements attribués.
- Filtres : gestion (sans support), commercial (contrats non signés / non payés), support (ses événements).

## Suivi
| Jalon | Branche | Statut | Commit/PR | Fiche |
|---|---|---|---|---|
| J1 | `chore/setup-project` | À faire | — | — |
| J2 | `feat/database-models` | À faire | — | — |
| J3 | `feat/user-management` | À faire | — | — |
| J4 | `feat/authentication` | À faire | — | — |
| J5 | `feat/read-operations` | À faire | — | — |
| J6 | `feat/crud-operations` | À faire | — | — |
| J7 | `feat/cli-interface` | À faire | — | — |
| J8 | `feat/security-logging` | À faire | — | — |
| J9 | `docs/final-delivery` | À faire | — | — |

## Références
- `Backend sécurisé — Cahier des charges [2.0].pdf`
- `Texte collé(7).txt` — scénario et étapes OpenClassrooms

**Note :** les tests et la sécurité sont transversaux dès J1. La roadmap peut évoluer avec justification et historique Git ; ne pas confondre fonctionnalités explicitement exigées et choix techniques proposés.
