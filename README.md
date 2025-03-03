# RoxxBot
A Discord bot created to offer build recommendations for the game Dofus Touch.

The recommandations are stored in a simple database :   
[DB diagram](https://dbdiagram.io/d/PanoDB-67c5d9b5263d6cf9a010af9b)

```mermaid
erDiagram
    STUFF {
        INT DB_id PK
        CHAR DB_surl
        VARCHAR Nom
        INT PA
        INT PM
        INT PO
        INT Invo
    }
    ELEMENT {
        INT ElementID PK
        VARCHAR Nom
    }
    CLASSE {
        INT ClasseID PK
        VARCHAR Nom
    }
    STUFF_ELEMENT {
        INT ElementID FK
        INT DB_id FK
    }
    STUFF_CLASSE {
        INT ClasseID FK
        INT DB_id FK
    }

    STUFF_ELEMENT }|..|{ STUFF : has
    STUFF_CLASSE }|..|{ STUFF : has
    STUFF_ELEMENT }|..|{ ELEMENT : relates
    STUFF_CLASSE }|..|{ CLASSE : relates
