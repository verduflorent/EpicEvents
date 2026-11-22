# Epic Events — CRM sécurisé

Application CRM Python en ligne de commande, sans Django.

## Jalon actuel : J1 — environnement

### Prérequis
- Python 3.10+ (inférieur à 4)
- Poetry 2.x
- PostgreSQL local

### Installation sous PowerShell

```powershell
git pull origin chore/setup-project
poetry install
Copy-Item .env.example .env
```

Dans `.env`, remplacer `CHANGE_ME` par le mot de passe de votre rôle PostgreSQL non privilégié. Créer au préalable la base `epicevents` et le rôle `epicevents_user`, avec les droits nécessaires sur cette seule base. Ne jamais committer `.env`.

### Vérification

```powershell
poetry run pytest
poetry run ruff check .
poetry run black --check .
poetry run epicevents db-check
```

`db-check` exécute un `SELECT 1` : aucune table métier n'est encore créée. Les modèles et migrations seront réalisés au jalon J2.

### Sécurité
Les secrets sont chargés depuis l'environnement. Les exceptions de connexion ne sont pas affichées telles quelles dans la CLI. Les rôles applicatifs et contrôles d'accès seront implémentés aux jalons suivants.

Voir [ROADMAP.md](ROADMAP.md) et [fiche de révision J1](docs/revisions/01-environnement.md).
