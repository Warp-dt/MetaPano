import mysql.connector

# Informations de connexion
config = {
    'host': '192.168.1.193',
    'port' : 3333,
    'user': 'pc_wind',
    'password': 'Wr50M=)',
    'database': 'test_db'
}

try:
    # Connexion à la base de données
    connection = mysql.connector.connect(**config)
    print("Connexion réussie !")

    # Exécuter une requête test
    cursor = connection.cursor()
    cursor.execute("SHOW TABLES;")
    print("Tables disponibles :")
    for table in cursor.fetchall():
        print(table)

except mysql.connector.Error as err:
    print(f"Erreur : {err}")
finally:
    if 'connection' in locals() and connection.is_connected():
        connection.close()