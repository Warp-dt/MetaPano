# RoxxBot
A Discord bot created to offer build recommendations for the game Dofus Touch.

The recommandations are stored in a simple database :   
[DB diagram](https://dbdiagram.io/d/PanoDB-67c5d9b5263d6cf9a010af9b)

```mermaid
erDiagram
    STUFF {
        DB_id INT PK
        DB_surl CHAR
        Nom VARCHAR
        PA INT
        PM INT
        PO INT
        Invo INT
    }
    ELEMENT {
        ElementID INT PK
        Nom VARCHAR
    }
    STUFF_ELEMENT {
        ElementID INT FK
        DB_id INT FK
    }
    CLASSE {
        ClasseID INT PK
        Nom VARCHAR
    }
    STUFF_CLASSE {
        ClasseID INT FK
        DB_id INT FK
    }

    STUFF_ELEMENT }|..|{ STUFF : has
    STUFF_ELEMENT }|..|{ ELEMENT : relates
    STUFF_CLASSE }|..|{ STUFF : has
    STUFF_CLASSE }|..|{ CLASSE : relates
