# Fiche de révision — J1 : environnement

## Objectifs
- Versionner le projet sur une branche dédiée, sans secrets.
- Isoler les dépendances avec Poetry.
- Connecter une application CLI Python à PostgreSQL via SQLAlchemy.

## Notions à maîtriser
**Poetry** : gère les dépendances, l'environnement virtuel et le verrouillage des versions (`poetry.lock` à générer et committer).

**PostgreSQL** : serveur de base de données relationnelle. L'utilisateur applicatif doit être non privilégié, avec uniquement les droits nécessaires.

**SQLAlchemy** : bibliothèque Python de communication avec la BDD. `create_engine` configure un moteur, `engine.connect()` ouvre une connexion et `text("SELECT 1")` prépare une requête SQL.

**Variables d'environnement** : `DATABASE_URL` est chargée depuis un `.env` local, ignoré par Git. `.env.example` contient uniquement des valeurs fictives.

**CLI / Click** : `epicevents db-check` est une commande de diagnostic.

## Questions de soutenance
1. Pourquoi ne pas stocker le mot de passe PostgreSQL dans le code ?
2. Quelle différence entre un moteur SQLAlchemy et une connexion ?
3. Pourquoi créer un utilisateur PostgreSQL non superutilisateur ?
4. À quoi sert `poetry.lock` ?
5. Pourquoi tester la CLI sans nécessiter PostgreSQL dans tous les tests ?

## Validation locale à compléter
- [ ] `poetry install`
- [ ] `poetry run pytest`
- [ ] `poetry run ruff check .`
- [ ] `poetry run black --check .`
- [ ] `poetry run epicevents db-check`
- [ ] `poetry.lock` généré et versionné
