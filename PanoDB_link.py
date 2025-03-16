import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError



################################################################
# DB HANDLING
################################################################
# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

# Récupérer l'environnement
environment = os.getenv("ENVIRONMENT", "windows")  # Par défaut, considérer que c'est Windows

# Configuration selon l'environnement
if environment == "windows":
    db_user = "pc_wind"
    db_password = os.getenv("DB_PASSWORD")
    db_host = "192.168.1.193"  # IP du serveur MySQL
    db_name = "PanoDB"
elif environment == "server":
    db_user = "localuser"  # Utilisateur sur le serveur
    db_password = os.getenv("SERVER_DB_PASSWORD")
    db_host = "localhost"  # MySQL est accessible localement sur le serveur
    db_name = "PanoDB"
else:
    raise ValueError(f"Environnement inconnu : {environment}")

# Créer l'URL de connexion
connection_string = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"

# Créer le moteur SQLAlchemy
# engine = create_engine(connection_string, echo=False)


# criteres={
#         'Élément': ['terre', 'cc', 'eau'], 
#         'Classe': 'enutrof', 
#         'Lvl': ['200', '199', '198-195', '189-185'], 
#         'PA': '11', 
#         'PM': '6', 
#         'PO': '4', 
#         'Invo': '1'
#         }

def stuff_query(criteres : dict):
    elt_exclusifs=['terre', 'feu', 'eau', 'air', 'dopou']
    elt_nonexclusifs=['cc', 'initiative', 'pp', 'sagesse', 'pods', 'pvp', 'pvm', 'retrait pa', 'retrait pm', 'esquive pa', 'esquive pm', 'repou', 'recri', 'tank']

    #Query building
    select=f"""SELECT 
    s.DB_id
    ,max(s.DB_surl) as DB_surl
    ,max(s.Nom) as Nom
    ,max(s.PA) as PA
    ,max(s.PM) as PM
    ,max(s.PO) as PO
    ,max(s.Invo) as Invo
    ,max(s.Lvl) as Lvl
    ,GROUP_CONCAT(DISTINCT c.Nom
        ORDER BY c.Nom ASC
        SEPARATOR ',')  as Classe
    ,GROUP_CONCAT(DISTINCT e.Nom
        ORDER BY e.Nom ASC
        SEPARATOR ',') as Elements\n"""
    from_q="FROM Stuff as s\n"
    from_q+="left join Stuff_Classe as sc on s.DB_id=sc.DB_id\n"
    from_q+="left join Classe as c on sc.ClasseID=c.ClasseID\n"
    from_q+="left join Stuff_Element as se on s.DB_id=se.DB_id\n"
    from_q+="left join Element as e on se.ElementID=e.ElementID\n"

    where="WHERE\n"
    group="GROUP BY s.DB_id\n"
    having=""
    
    first_having=True

    lvl=['200']        
    if 'Lvl' in criteres.keys():
        lvl=criteres["Lvl"]
    
    first_lvl=True
    for lvl_slice in lvl:
        if first_lvl:
            where+='('
            first_lvl=False
        else:
            where+=" OR "
        if len(lvl_slice)==3:
            where+="Lvl="+lvl_slice
        else:
            spl_lvl=lvl_slice.split("-")
            where+="(Lvl<="+spl_lvl[0]+" AND "+"Lvl>="+spl_lvl[1]+')'
    where+=')\n'

    for crit in ["PA","PM","PO","Invo"]:
        if crit in criteres.keys():
            where+=" AND "+crit+">="+criteres[crit]+"\n"

    if 'Classe' in criteres.keys():
        if first_having:
            having+="HAVING\n"
            first_having=False
        else:
            having+="AND\n"

        having+=f"""-- check que le stuff ait la classe demandée
sum(CASE WHEN c.Nom = '{criteres["Classe"]}' 
        THEN 1 
        ELSE 0 END) >0\n"""



    if 'Élément' in criteres.keys():
        #check que chaque élément demandé soit dans les éléments du stuff
        
        if len(criteres["Élément"])==1 and criteres["Élément"][0]=="dopou":
            if first_having:
                    having+="HAVING\n"
                    first_having=False
            else:
                having+="AND\n"
            having+="""sum(CASE WHEN e.Nom = 'dopou' THEN 1 ELSE 0 END) >0\n"""
        else:
            for elt in criteres["Élément"]:
                if first_having:
                    having+="HAVING\n"
                    first_having=False
                else:
                    having+="AND\n"
                
                having+=f"""sum(CASE WHEN e.Nom = '{str(elt)}' THEN 1 ELSE 0 END) >0\n"""

            exclusifs_non_inclus=[x for x in elt_exclusifs if x not in criteres["Élément"]]
            if len(exclusifs_non_inclus)>0:
                having+=f"""AND
-- check que le stuff n'ai pas un autre élément exclusif (=terre,feu,eau,air,dopou)
sum(CASE WHEN e.Nom IN ({str(exclusifs_non_inclus).replace("[",'').replace("]",'')}) THEN 1 ELSE 0 END) = 0\n"""


    query=select+from_q+where+group+having+";"

    return query

def find_stuff(criteres : dict):
    engine = create_engine(connection_string, echo=False)

    query=stuff_query(criteres)

    # print(query)

    with engine.connect() as conn:        
        result = conn.execute(text(query)).fetchall()
        conn.close()
    engine.dispose()
    return [dict(r._mapping) for r in result]

# if __name__ == "__main__":
#     print(find_stuff(criteres))
        

