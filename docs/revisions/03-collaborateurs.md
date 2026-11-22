# Fiche J3 — Collaborateurs et rôles

## Ce que nous avons construit
Epic Events possède maintenant des fonctions Python pour créer, modifier et supprimer des collaborateurs. Chaque collaborateur appartient à un département : `gestion`, `commercial` ou `support`. La première commande accessible depuis le terminal est `bootstrap-manager`, qui crée le premier responsable gestion sur une installation locale de confiance.

## Les mots de passe
Le mot de passe original n'est pas enregistré. Argon2id calcule une empreinte avec un sel aléatoire : même avec deux mots de passe identiques, les empreintes diffèrent. La fonction `verify_password` permet de vérifier un mot de passe lors d'une future connexion. Le programme exige au moins 12 caractères.

## La différence entre rôle et authentification
Le département détermine ce qu'un collaborateur est autorisé à faire. Les fonctions de gestion vérifient que l'acteur appartient à `gestion`. En revanche, l'identité de cet acteur n'est pas encore prouvée par une connexion : ce sera l'objet du J4. Pour cette raison, nous n'exposons pas encore les opérations administratives de création/modification/suppression dans la CLI.

## Premier compte et protection
La commande `poetry run epicevents bootstrap-manager` demande un nom, un email et un mot de passe masqué. Elle ne fonctionne que lorsqu'aucun collaborateur n'existe. Les départements sont créés si nécessaire. Sur la base locale, le premier compte gestion a été créé et vérifié sans afficher l'empreinte.

## Tests et limites
16 tests automatisés ont réussi au total, dont six pour le J3 : sel et vérification des mots de passe, longueur minimale, initialisation unique, opérations autorisées, refus des opérations hors gestion, refus des doublons et de l'auto-suppression. Ruff et Black sont validés.

Les contraintes de clés étrangères protègent les collaborateurs déjà référencés par des clients ou contrats. L'authentification persistante, les sessions et le contrôle des droits à l'entrée de la CLI appartiennent au J4.

## Questions pour la soutenance
1. Pourquoi stocker une empreinte plutôt qu'un mot de passe ?
2. Pourquoi deux empreintes d'un même mot de passe peuvent-elles être différentes ?
3. Quelle différence entre authentification et autorisation ?
4. Pourquoi l'initialisation du premier gestionnaire n'est-elle possible qu'une fois ?
5. Pourquoi séparer les opérations métier de l'interface CLI ?
