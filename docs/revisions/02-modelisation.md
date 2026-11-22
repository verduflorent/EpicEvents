# Fiche de révision n°2 — Modélisation de la base de données

## Pourquoi modéliser ?
Avant d'enregistrer les données, nous devons décider quelles informations stocker et comment elles sont reliées. C'est comme dessiner le plan d'une maison avant de la construire.

## Une table, une classe
Avec l'ORM SQLAlchemy, la classe Python `Client` décrit la table `clients`. Un objet `Client` représente un client concret.

## Les cinq tables
- `departments` : les équipes de l'entreprise.
- `employees` : les collaborateurs et leur département.
- `clients` : les clients et leur commercial.
- `contracts` : les contrats d'un client, avec leurs montants et signature.
- `events` : les événements d'un contrat et leur éventuel support.

## Clés et relations
Une **clé primaire** (`id`) identifie une ligne de manière unique. Une **clé étrangère** relie une ligne à une autre table : par exemple, `client_id` indique à quel client appartient un contrat.

Une relation « un à plusieurs » signifie qu'un client peut avoir plusieurs contrats, mais qu'un contrat appartient à un seul client.

## Pourquoi des contraintes ?
Elles évitent d'enregistrer des données absurdes, par exemple un événement qui se termine avant de commencer ou un montant restant négatif.

## À quoi sert Alembic ?
Alembic garde l'historique des changements de structure. Une **migration** crée ou modifie les tables, sans avoir à refaire toute la base à chaque évolution.

## À retenir
Nous avons créé la structure des données, pas encore les commandes pour gérer les clients. Les permissions et les règles métier seront ajoutées aux prochains jalons.

## Questions de soutenance
1. Quelle différence entre une clé primaire et une clé étrangère ?
2. Pourquoi relier un contrat à un client plutôt que recopier ses coordonnées ?
3. Pourquoi utiliser `Numeric` pour les montants ?
4. Pourquoi un événement peut-il ne pas avoir de support ?
5. Quelle différence entre un modèle SQLAlchemy et une migration Alembic ?
