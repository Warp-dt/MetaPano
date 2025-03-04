import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
import requests as req


################################################################
# SCRAPING
################################################################
FR_KEYS=['Lvl','PA', 'PM', 'PO', 'Initiative', 'Critique', 'Invocation', 'Soin', 'Vitalité', 'Sagesse', 'Force', 'Intelligence', 'Chance', 'Agilité', 'Puissance', 'Fuite', 'Esq. PA', 'Esq. PM', 'Pods', 'Tacle', 'Ret. PA', 'Ret. PM',  'Do Critique', '% Ré Air', '% Ré Feu', 'Do Eau', 'Do Terre', 'Do Neutre', '% Ré Terre', 'Prospection', 'Do Feu', 'Do Air', 'Do Poussée', 'Ré Neutre', '% Ré Neutre', 'Ré Terre', 'Ré Feu', 'Ré Eau', '% Ré Eau', 'Ré Air', 'Ré Critique', 'Ré Poussée', "Do"]
EN_KEYS=['Lvl','AP', 'MP', 'Range', 'Initiative', 'Critical', 'Summon', 'Heal', 'Vitality', 'Wisdom', 'Strength', 'Intelligence', 'Chance', 'Agility', 'Power', 'Dodge', 'AP Res.', 'MP Res.', 'Pods', 'Lock', 'AP Red', 'MP Red',  'Da Critical', '% Re Air', '% Re Fire', 'Da Water', 'Da Earth', 'Da Neutral', '% Re Earth', 'Prospecting', 'Da Fire', 'Da Air', 'Da Pushback', 'Re Neutral', '% Re Neutral', 'Re Earth', 'Re Fire', 'Re Water', '% Re Water', 'Re Air', 'Re Critical', 'Re Pushback', "Da"]
ES_KEYS=['Lvl','PA', 'PM', 'AL', 'Iniciativa', 'Crítico', 'Invocación', 'Cura', 'Vitalidad', 'Sabiduría', 'Fuerza', 'Inteligencia', 'Suerte', 'Agilidad', 'Potencia', 'Huida', 'Esq. PA', 'Esq. PM', 'Pods', 'Placaje', 'Ret. PA', 'Ret. PM',  'Da Crítico', '% Re Aire', '% Re Fuego', 'Da Agua', 'Da Tierra', 'Da Neutro', '% Re Tierra', 'Prospección', 'Da Fuego', 'Da Aire', 'Da Empuje', 'Re Neutro', '% Re Neutro', 'Re Tierra', 'Re Fuego', 'Re Agua', '% Re Agua', 'Re Aire', 'Re Crítico', 'Re Empuje', "Da"]

ALIASES=dict()
for i in range(len(FR_KEYS)):
    ALIASES[EN_KEYS[i]]=FR_KEYS[i]
    ALIASES[FR_KEYS[i]]=FR_KEYS[i]
    ALIASES[ES_KEYS[i]]=FR_KEYS[i]

TRAD_DB_STATS={
    # stats du perso
    'scroll_vi': 'Vitalité',
    'scroll_sa': 'Sagesse',
    'scroll_fo': 'Force',
    'scroll_in': 'Intelligence',
    'scroll_ch': 'Chance',
    'scroll_ag': 'Agilité',
    'base_vi': 'Vitalité',
    'base_sa': 'Sagesse',
    'base_fo': 'Force',
    'base_in': 'Intelligence',
    'base_ch': 'Chance',
    'base_ag': 'Agilité',

    #fm global
    'pa': "PA",
    'pm': "PM",
    'po': "PO",
    'vi': "Vitalité",
    'sa': "Sagesse",
    'fo': "Force",
    'in': "Intelligence",
    'ch': "Chance",
    'ag': "Agilité",
    'pu': "Puissance",
    'ii': "Initiative",
    'cc': "Critique",
    'ic': "Invocation",
    'so': "Soin",
    'pp': "Prospection",
    'fu': "Fuite",
    'ta': "Tacle",
    'dmg': "Do",
    'dnf': "Do Neutre",
    'dtf': "Do Terre",
    'dff': "Do Feu",
    'def': "Do Eau",
    'daf': "Do Air",
    'dc': "Do Critique",
    'dp': "Do Poussée",
    'dw': "non attribué",
    'ds': "non attribué",
    'dm': "non attribué",
    'dd': "non attribué",
    'deg': "non attribué",
    'rn': "Ré Neutre",
    'rt': "Ré Terre",
    'rf': "Ré Feu",
    're': "Ré Eau",
    'ra': "Ré Air",
    'rnp': "% Ré Neutre",
    'rtp': "% Ré Terre",
    'rfp': "% Ré Feu",
    'rep': "% Ré Eau",
    'rap': "% Ré Air",
    'rc': "Ré Critique",
    'rp': "Ré Poussée",
    'rm': "non attribué",
    'rd': "non attribué",
    'rw': "non attribué",
    'epa': "Esq. PA",
    'epm': "Esq. PM",
    'rpa': "Ret. PA",
    'rpm': "Ret. PM",
    'pd': "Pods",
    'pi': "non attribué",
    'pip': "non attribué",
    'rv': "non attribué",
}   
elt_filtre={
    "terre" : "ter"
    ,"feu" : "feu"
    ,"eau" : "eau"
    ,"air" : "air"
    ,"dopou" : "dp"
    ,"cc" : "cc"
    ,"initiative" : "ii"
    ,"pp" : "pp"
    ,"sagesse" : "sa"
    ,"pods" : "pd"
    ,'pvp' : 'pvp'
    ,'pvm' : 'pvm'
    ,'retrait pa' : 'rpa'
    ,'retrait pm' : 'rpm'
    ,'esquive pa' : 'epa'
    ,'esquive pm' : 'epm'
    ,'repou' :'rp'
    ,'recri' : 'rc'
    ,'tank' : 'tank'
    # ,'dodist' : 'dd'
    # ,'domelee' : 'dm'
    # ,'dosort' : 'ds'
}
raw_elt_to_id={
    elt_filtre['terre']      : 1,
    elt_filtre['feu']        : 2,
    elt_filtre['eau']        : 3,
    elt_filtre['air']        : 4,
    elt_filtre['dopou']      : 5,
    elt_filtre['cc']         : 6,
    elt_filtre['initiative'] : 7,
    elt_filtre['pp']         : 8,
    elt_filtre['sagesse']    : 9,
    elt_filtre['pods']       : 10,
    elt_filtre['pvp']        : 11,
    elt_filtre['pvm']        : 12,
    elt_filtre['retrait pa'] : 13,
    elt_filtre['retrait pm'] : 14,
    elt_filtre['esquive pa'] : 15,
    elt_filtre['esquive pm'] : 16,
    elt_filtre['repou']      : 17,
    elt_filtre['recri']      : 18,
    elt_filtre['tank']       : 19
}
classes_filtre={
    "tout" : "A"
    ,"feca" : "1"
    ,"osamodas" : "2"
    ,"enutrof" : "3"
    ,"sram" : "4"
    ,"xelor" : "5"
    ,"ecaflip" : "6"
    ,"eniripsa" : "7"
    ,"iop" : "8"
    ,"cra" : "9"
    ,"sadida" : "10"
    ,'sacrieur' : "11"
    ,"pandawa" : "12"
    ,"roublard" : "13"
    ,"zobal" : "14"
    ,"steamer" : "15"
}

def url_builder(element="rien",classes="rien",page="1",user="996244-metapano"):
    #user="244671-warp"
    base="https://touch.dofusbook.net/stuffs/touch/public/"
    membre="&user="+user+"&sort=update-desc"
    page_base="?page="
    filtre=""
    if type(element)==list:
        filtre+="&include="
        first=True
        for elt in element:
            if not first:
                filtre+="-"
            else:
                first=False
            filtre+=elt_filtre[elt]
    
    if type(classes)==list:
        filtre+="&classes="
        first2=True
        for cla in classes:
            if not first2:
                filtre+="-"
            else:
                first2=False
            filtre+=classes_filtre[cla]
    
    
    return base+page_base+str(page)+membre+filtre


def get_stats(id):
       
    data= req.get("https://touch.dofusbook.net/stuffs/touch/public/"+str(id)).json()

    perso_stats=data["stuffStats"] # 1 element = 1 stat
    fmitems=data["fmItems"] # chaque element est un item sous forme dict, chaque element d'un item est un fm qui lui est rajouté
    fmglobal=data["fmGlobal"] #  1 element = 1 stat
    items=data["items"] #list d'items, chaque item est un dict dont la clef "effects" est une liste d'effets où chaque effet est un dict contenant les clefts suivantes 'name': 'nomdelastat','type': 'E', 'min': 0,'max': 0,
    panos=data["cloths"] # list de pano, chaque item est un dict dont la clef "effects" est une liste d'effets où chaque effet est un dict contenant les clefts suivantes 'name': 'nomdelastat','type': 'E', 'value' : 1
    

    perso={key: 0 for key in FR_KEYS}
    perso["DB_surl"]=data["stuff"]["short_url"]
    perso["Lvl"]=data["stuff"]["character_level"]
    perso["db_name"]=data["stuff"]["name"]
    perso["PA"]=7
    if perso["Lvl"]<100:
        perso["PA"]-=1
    perso["PM"]=3
    perso["Invocation"]=1
    perso["Vitalité"]=50+5*perso["Lvl"]

    for elt in perso_stats:
        perso[TRAD_DB_STATS[elt]]+=perso_stats[elt]
    
    for elt in fmglobal:
        perso[TRAD_DB_STATS[elt]]+=fmglobal[elt]
    
    for item in fmitems:
        for elt in fmitems[item]:
            perso[TRAD_DB_STATS[elt]]+=fmitems[item][elt]
    
    for item in items:
        for stat in item["effects"]:
            if stat["type"]=='E':
                if stat["min"]>=0:
                    perso[TRAD_DB_STATS[stat["name"]]]+=stat["max"]
                else:
                    perso[TRAD_DB_STATS[stat["name"]]]+=stat["min"]

    for pano in panos:
        for stat in pano["effects"]:
            if stat["type"]=='E':
                perso[TRAD_DB_STATS[stat["name"]]]+=stat["value"]

    #bonus dérivés de stats
    # perso["Soin"]+=max(0,perso["Intelligence"]/10//1)
    perso["Fuite"]+=max(0,perso["Chance"]/10//1)
    perso["Tacle"]+=max(0,perso["Agilité"]/10//1)
    perso["Esq. PA"]+=max(0,perso["Sagesse"]/10//1)
    perso["Esq. PM"]+=max(0,perso["Sagesse"]/10//1)
    perso["Ret. PA"]+=max(0,perso["Sagesse"]/10//1)
    perso["Ret. PM"]+=max(0,perso["Sagesse"]/10//1)
    perso["Initiative"]+=max(0,perso["Intelligence"])+max(0,perso["Chance"])+max(0,perso["Agilité"])+max(0,perso["Force"])

    return perso

def get_stuff_base_info(id):
    resp=get_stats(id)
    ans={
        "DB_surl": resp["DB_surl"],
        "PA": resp["PA"],
        "PM": resp["PM"],
        "PO": resp["PO"],
        "Invo": resp["Invocation"],
        "Lvl" : resp["Lvl"]
        }
    return ans

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

# # Charger les variables d'environnement depuis le fichier .env
# load_dotenv()

# # Récupérer le mot de passe depuis les variables d'environnement
# db_password = os.getenv("DB_PASSWORD")

# # Configuration de la connexion
# db_user = "pc_wind"
# db_host = "192.168.1.193"
# db_name = "PanoDB"

# Créer l'URL de connexion
connection_string = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"

# Créer le moteur SQLAlchemy
engine = create_engine(connection_string, echo=False)

def upsert_stuff_data(stuff_list):
    """
    Met à jour ou insère les données de stuff dans la base de données.
    Supprime les stuff qui ne sont pas présents dans la liste d'entrée.
    
    Args:
        stuff_list: Liste de dictionnaires contenant les données de stuff
    """
    inserted_count = 0
    updated_count = 0
    deleted_count = 0
    error_count = 0
    
    # Extraire tous les DB_id de la liste d'entrée
    input_db_ids = [stuff["DB_id"] for stuff in stuff_list]
    
    # Utiliser une transaction pour s'assurer que les opérations sont atomiques
    with engine.begin() as connection:
        try:
            # 1. Identifier et supprimer les stuffs qui ne sont plus présents
            result = connection.execute(
                text("SELECT DB_id FROM Stuff WHERE DB_id NOT IN :ids"),
                {"ids": tuple(input_db_ids) if input_db_ids else (0,)}  # Éviter une liste vide
            ).fetchall()
            
            to_delete_ids = [row[0] for row in result]
            
            for db_id in to_delete_ids:
                # Supprimer d'abord les relations pour respecter les contraintes de clé étrangère
                connection.execute(
                    text("DELETE FROM Stuff_Classe WHERE DB_id = :db_id"),
                    {"db_id": db_id}
                )
                connection.execute(
                    text("DELETE FROM Stuff_Element WHERE DB_id = :db_id"),
                    {"db_id": db_id}
                )
                # Puis supprimer le stuff lui-même
                connection.execute(
                    text("DELETE FROM Stuff WHERE DB_id = :db_id"),
                    {"db_id": db_id}
                )
                deleted_count += 1
            
            # 2. Mettre à jour ou insérer les stuffs de la liste d'entrée
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
                            SET DB_surl = :db_surl, Nom = :nom, PA = :pa, PM = :pm, PO = :po, Invo = :invo, Lvl = :lvl
                            WHERE DB_id = :db_id
                            """),
                            {
                                "db_id": stuff["DB_id"],
                                "db_surl": stuff["DB_surl"],
                                "nom": stuff["Nom"],
                                "pa": stuff["PA"],
                                "pm": stuff["PM"],
                                "po": stuff["PO"],
                                "invo": stuff["Invo"],
                                "lvl" : stuff["Lvl"]
                            }
                        )
                        updated_count += 1
                    else:
                        # Insert new stuff
                        connection.execute(
                            text("""
                            INSERT INTO Stuff (DB_id, DB_surl, Nom, PA, PM, PO, Invo, Lvl)
                            VALUES (:db_id, :db_surl, :nom, :pa, :pm, :po, :invo, :lvl)
                            """),
                            {
                                "db_id": stuff["DB_id"],
                                "db_surl": stuff["DB_surl"],
                                "nom": stuff["Nom"],
                                "pa": stuff["PA"],
                                "pm": stuff["PM"],
                                "po": stuff["PO"],
                                "invo": stuff["Invo"],
                                "lvl" : stuff["Lvl"]
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
        
        except Exception as e:
            print(f"Erreur générale lors de la mise à jour: {e}")
            raise
    
    return {
        "inserted": inserted_count,
        "updated": updated_count,
        "deleted": deleted_count,
        "errors": error_count
    }


# Exemple d'utilisation
if __name__ == "__main__":

    page_maxsize=20
    taille=20
    i=1
    stuff_liste=[]
    print("Début du scraping")
    while taille==page_maxsize:
        resp=req.get(url_builder(page=i)).json()["rows"]
        taille=len(resp)
        for stuff in resp:
            if len(stuff["allowed_classes"])==0:
                stuff["allowed_classes"].append(16)
            temp_dict={
                "DB_id": stuff['id'],
                "DB_surl": get_stuff_base_info(stuff['id'])["DB_surl"],
                "Nom": stuff["name"],
                "PA": get_stuff_base_info(stuff['id'])["PA"],
                "PM": get_stuff_base_info(stuff['id'])["PM"],
                "PO": get_stuff_base_info(stuff['id'])["PO"],
                "Invo": get_stuff_base_info(stuff['id'])["Invo"],
                "Lvl" : get_stuff_base_info(stuff['id'])["Lvl"],
                "classes": stuff["allowed_classes"],
                "elements": [ raw_elt_to_id[elt_raw] for elt_raw in stuff["tags"]]
            }
            stuff_liste.append(temp_dict)
        print("page "+str(i)+" finie")
        i+=1
    
    print("Scraping Terminé")
    # Appeler la fonction avec les données
    print("Mise à jour PanoDB")
    result = upsert_stuff_data(stuff_liste)
    print(f"Résultat: {result['inserted']} insérés, {result['updated']} mis à jour, {result['deleted']} supprimés, {result['errors']} erreurs")