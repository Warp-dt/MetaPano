import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy import Column, Integer, BigInteger, String, TIMESTAMP, JSON, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timezone


BIBLI_DEFAULT={
    "biblio_id" : "996244"
    ,"nom_biblio" : "MetaPano"
    ,"dossier" : "tout"
    ,"dossier_id": "-1"
    ,"jeu" : "Dofus Touch"
}

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
CONNECTION_STRING = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"

# Créer le moteur SQLAlchemy
# engine = create_engine(CONNECTION_STRING, echo=False)


# criteres={
#         'Élément': ['terre', 'cc', 'eau'], 
#         'Classe': 'enutrof', 
#         'Lvl': ['200', '199', '198-195', '189-185'], 
#         'PA': '11', 
#         'PM': '6', 
#         'PO': '4', 
#         'Invo': '1'
#         }

def stuff_query(criteres : dict,biblio=BIBLI_DEFAULT):
    elt_exclusifs=['terre', 'feu', 'eau', 'air', 'dopou']
    elt_nonexclusifs=['cc', 'initiative', 'pp', 'sagesse', 'pods', 'pvp', 'pvm', 'retrait pa', 'retrait pm', 'esquive pa', 'esquive pm', 'repou', 'recri', 'tank','soin']
    
    try:
        biblio_id=biblio["biblio_id"]
        biblio_name=biblio["nom_biblio"]
        dossier=biblio["dossier"]
        dossier_id=biblio["dossier_id"]
    except Exception as e:
        print("Erreur dans la biblio",e)
        biblio_id=BIBLI_DEFAULT["biblio_id"]
        biblio_name=BIBLI_DEFAULT["nom_biblio"]
        dossier=BIBLI_DEFAULT["dossier"]
        dossier_id=BIBLI_DEFAULT["dossier_id"]


    # print("query",biblio_id,biblio_name)
    # print(criteres)
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

    where+="AND s.bibli_id="+biblio_id+"\n"

    for crit in ["PA","PM","PO","Invo"]:
        if crit in criteres.keys():
            where+=" AND "+crit+">="+criteres[crit]+"\n"

    if dossier_id!="-1":
        where+="AND dossier_id="+dossier_id+"\n"


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
            if len(exclusifs_non_inclus)>0 and len(exclusifs_non_inclus)<5:
                having+=f"""AND
-- check que le stuff n'ai pas un autre élément exclusif (=terre,feu,eau,air,dopou)
sum(CASE WHEN e.Nom IN ({str(exclusifs_non_inclus).replace("[",'').replace("]",'')}) THEN 1 ELSE 0 END) = 0\n"""


    query=select+from_q+where+group+having+";"

    return query

def find_stuff(criteres : dict,biblio=BIBLI_DEFAULT):
    engine = create_engine(CONNECTION_STRING, echo=False)

    query=stuff_query(criteres,biblio=biblio)

    # print(query)

    with engine.connect() as conn:
        try:        
            result = conn.execute(text(query)).fetchall()
        except:
            conn.close()
            engine.dispose()
            return []
        conn.close()
    engine.dispose()
    return [dict(r._mapping) for r in result]

# if __name__ == "__main__":
#     print(find_stuff(criteres))
        

Base = declarative_base()

class CommandLog(Base):
    __tablename__ = 'command_logs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    executed_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    user_id = Column(BigInteger, nullable=False)
    user_name = Column(String(100), nullable=False)
    guild_id = Column(BigInteger, nullable=False)
    guild_name = Column(String(100), nullable=False)
    channel_id = Column(BigInteger, nullable=False)
    channel_name = Column(String(100), nullable=False)
    command = Column(String(50), nullable=False)
    arguments = Column(JSON)


# Créer le moteur SQLAlchemy
engine = create_engine(CONNECTION_STRING, echo=False)
# Création du sessionmaker (à faire une seule fois dans ton script principal)
Session = sessionmaker(bind=engine)

# def command_log(user_name,user_id,server_name,server_id,channel_name,channel_id,command_name,arguments,date="CURRENT_TIMESTAMP"):
#     engine = create_engine(CONNECTION_STRING, echo=False)



def command_log(user_name, user_id, server_name, server_id, channel_name, channel_id, command_name, arguments, date=None):
    """
    Enregistre l'exécution d'une commande Discord dans la base de données.
    
    :param user_name: Nom visible de l'utilisateur
    :param user_id: ID Discord unique de l'utilisateur
    :param server_name: Nom du serveur (guild)
    :param server_id: ID Discord du serveur
    :param channel_name: Nom du channel
    :param channel_id: ID Discord du channel
    :param command_name: Nom de la commande exécutée
    :param arguments: Dictionnaire des arguments de la commande
    :param date: Date d'exécution (optionnelle, default = CURRENT_TIMESTAMP)
    """
    session = Session()
    
    try:
        # On prépare les arguments du constructeur
        log_kwargs = {
            "user_id": user_id,
            "user_name": user_name,
            "guild_id": server_id,
            "guild_name": server_name,
            "channel_id": channel_id,
            "channel_name": channel_name,
            "command": command_name,
            "arguments": arguments
        }
        
        # Si date fournie, on l'ajoute
        # Si aucune date fournie, on laisse MySQL mettre CURRENT_TIMESTAMP
        if date:
            log_kwargs["executed_at"] = date
        
        log_entry = CommandLog(**log_kwargs)
               
        session.add(log_entry)
        session.commit()
        # print(f"[LOG] Commande '{command_name}' exécutée par {user_name} enregistrée avec succès.")
    
    except SQLAlchemyError as e:
        session.rollback()
        # print(f"[ERREUR LOG] Impossible d'enregistrer la commande '{command_name}': {e}")
    
    finally:
        session.close()

