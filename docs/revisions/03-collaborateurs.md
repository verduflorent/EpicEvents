# Fiche J3 — Collaborateurs et rôles (en cours)

## L'idée
Un collaborateur possède un compte, un département et un mot de passe protégé. Les trois départements sont gestion, commercial et support.

## Pourquoi hacher les mots de passe ?
Nous ne stockons jamais le mot de passe original. Argon2id transforme le mot de passe en une empreinte difficile à inverser, avec un sel aléatoire. Deux utilisateurs ayant le même mot de passe auront normalement des empreintes différentes.

## Pourquoi séparer les permissions ?
Créer un compte n'est pas la même chose que se connecter. Au J3, les services vérifient le département de l'acteur. Au J4, nous construirons l'authentification qui prouvera qui est cet acteur.

## Le premier compte
Un premier compte gestion doit être créé dans une procédure locale de confiance. L'initialisation n'est autorisée que si aucun employé n'existe. Ne pas exposer cette opération dans une interface publique.

## À revoir après validation
- Démontrer création, modification, changement de département et suppression contrôlée.
- Expliquer l'intérêt des tests et des contraintes SQL.
- Distinguer authentification et autorisation.
