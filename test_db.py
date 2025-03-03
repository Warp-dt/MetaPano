import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Récupérer le mot de passe depuis les variables d'environnement
db_password = os.getenv("DB_PASSWORD")

# Configuration de la connexion
db_user = "pc_wind"
db_host = "192.168.1.193"
db_name = "test_db"

# Créer l'URL de connexion
connection_string = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"

# Créer le moteur SQLAlchemy
engine = create_engine(connection_string, echo=False)

def upsert_stuff_data(stuff_list):
    """
    Met à jour ou insère les données de stuff dans la base de données.
    
    Args:
        stuff_list: Liste de dictionnaires contenant les données de stuff
    """
    inserted_count = 0
    updated_count = 0
    error_count = 0
    
    # Utiliser une transaction pour s'assurer que les opérations sont atomiques
    with engine.begin() as connection:
        for stuff in stuff_list:
            try:
                # Vérifier si le stuff existe déjà
                result = connection.execute(
                    text("SELECT DB_id FROM Stuff WHERE DB_id = :db_id"),
                    {"db_id": stuff["DB_id"]}
                ).fetchone()
                
                if result:
                    # Update existing stuff
                    connection.execute(
                        text("""
                        UPDATE Stuff 
                        SET DB_surl = :db_surl, Nom = :nom, PA = :pa, PM = :pm, PO = :po, Invo = :invo
                        WHERE DB_id = :db_id
                        """),
                        {
                            "db_id": stuff["DB_id"],
                            "db_surl": stuff["DB_surl"],
                            "nom": stuff["Nom"],
                            "pa": stuff["PA"],
                            "pm": stuff["PM"],
                            "po": stuff["PO"],
                            "invo": stuff["Invo"]
                        }
                    )
                    updated_count += 1
                else:
                    # Insert new stuff
                    connection.execute(
                        text("""
                        INSERT INTO Stuff (DB_id, DB_surl, Nom, PA, PM, PO, Invo)
                        VALUES (:db_id, :db_surl, :nom, :pa, :pm, :po, :invo)
                        """),
                        {
                            "db_id": stuff["DB_id"],
                            "db_surl": stuff["DB_surl"],
                            "nom": stuff["Nom"],
                            "pa": stuff["PA"],
                            "pm": stuff["PM"],
                            "po": stuff["PO"],
                            "invo": stuff["Invo"]
                        }
                    )
                    inserted_count += 1
                
                # Gérer les relations avec les classes
                # D'abord, supprimer les anciennes relations pour mettre à jour proprement
                connection.execute(
                    text("DELETE FROM Stuff_Classe WHERE DB_id = :db_id"),
                    {"db_id": stuff["DB_id"]}
                )
                
                # Insérer les nouvelles relations
                for classe_id in stuff["classes"]:
                    connection.execute(
                        text("""
                        INSERT INTO Stuff_Classe (ClasseID, DB_id)
                        VALUES (:classe_id, :db_id)
                        """),
                        {"classe_id": classe_id, "db_id": stuff["DB_id"]}
                    )
                
                # Gérer les relations avec les éléments
                # D'abord, supprimer les anciennes relations pour mettre à jour proprement
                connection.execute(
                    text("DELETE FROM Stuff_Element WHERE DB_id = :db_id"),
                    {"db_id": stuff["DB_id"]}
                )
                
                # Insérer les nouvelles relations
                for element_id in stuff["elements"]:
                    connection.execute(
                        text("""
                        INSERT INTO Stuff_Element (ElementID, DB_id)
                        VALUES (:element_id, :db_id)
                        """),
                        {"element_id": element_id, "db_id": stuff["DB_id"]}
                    )
                
            except IntegrityError as e:
                print(f"Erreur d'intégrité pour le stuff {stuff['DB_id']}: {e}")
                error_count += 1
            except Exception as e:
                print(f"Erreur lors du traitement du stuff {stuff['DB_id']}: {e}")
                error_count += 1
    
    return {
        "inserted": inserted_count,
        "updated": updated_count,
        "errors": error_count
    }

# Exemple d'utilisation
if __name__ == "__main__":
    # Exemple de données (à remplacer par tes vraies données)
    exemple_stuffs = [
        {
            "DB_id": 123456,
            "DB_surl": "abcd",
            "Nom": "Stuff de test",
            "PA": 10,
            "PM": 5,
            "PO": 3,
            "Invo": 2,
            "classes": [1, 3],
            "elements": [2, 4]
        },
        {
            "DB_id": 789012,
            "DB_surl": "efgh",
            "Nom": "Autre stuff",
            "PA": 8,
            "PM": 6,
            "PO": 4,
            "Invo": 1,
            "classes": [2],
            "elements": [1, 3]
        }
    ]
    
    # Appeler la fonction avec les données
    result = upsert_stuff_data(exemple_stuffs)
    print(f"Résultat: {result['inserted']} insérés, {result['updated']} mis à jour, {result['errors']} erreurs")


# import mysql.connector
# import os
# from dotenv import load_dotenv

# load_dotenv()
# pwd= os.getenv('DB_CO')
# # Informations de connexion
# config = {
#     'host': '192.168.1.193',
#     'user': 'pc_wind',
#     'password': pwd,
#     'database': 'test_db'
    
# }

# try:
#     # Connexion à la base de données
#     connection = mysql.connector.connect(**config)
#     print("Connexion réussie !")

#     # Exécuter une requête test
#     cursor = connection.cursor()
#     cursor.execute("SHOW TABLES;")
#     print("Tables disponibles :")
#     for table in cursor.fetchall():
#         print(table)

# except mysql.connector.Error as err:
#     print(f"Erreur : {err}")
# finally:
#     if 'connection' in locals() and connection.is_connected():
#         connection.close()
