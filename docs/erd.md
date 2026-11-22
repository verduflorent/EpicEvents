# Diagramme relationnel — Epic Events (J2)

```mermaid
erDiagram
    DEPARTMENTS ||--o{ EMPLOYEES : "regroupe"
    EMPLOYEES ||--o{ CLIENTS : "commercial responsable"
    EMPLOYEES ||--o{ CONTRACTS : "commercial du contrat"
    CLIENTS ||--o{ CONTRACTS : "possede"
    CONTRACTS ||--o{ EVENTS : "organise"
    EMPLOYEES o|--o{ EVENTS : "support assigne"

    DEPARTMENTS {
        int id PK
        string name UK
    }
    EMPLOYEES {
        int id PK
        string full_name
        string email UK
        string password_hash
        int department_id FK
    }
    CLIENTS {
        int id PK
        string full_name
        string email
        string phone
        string company_name
        datetime created_at
        datetime updated_at
        int sales_contact_id FK
    }
    CONTRACTS {
        int id PK
        int client_id FK
        int sales_contact_id FK
        decimal total_amount
        decimal remaining_amount
        datetime created_at
        boolean is_signed
    }
    EVENTS {
        int id PK
        string name
        int contract_id FK
        datetime starts_at
        datetime ends_at
        string location
        int attendees
        text notes
        int support_contact_id FK
    }
```

## Choix de modélisation
- Un client est rattaché à un commercial ; un contrat conserve aussi une référence explicite à son commercial.
- Un contrat peut avoir plusieurs événements ; chaque événement référence exactement un contrat.
- Le support d'un événement est facultatif, notamment avant l'affectation par la gestion.
- Les montants sont des `Decimal` en base (`Numeric`) plutôt que des flottants.
- Des contraintes SQL empêchent les montants négatifs, les paiements restants supérieurs au total, les dates d'événement inversées et les participants négatifs.
- La cohérence métier (un commercial appartient au bon département, le commercial du contrat correspond à celui du client, signature préalable) sera contrôlée par les services métier aux jalons J3–J6.
