
from random import choice, randint
import re


# idées de dialogues possibles avec le bot:
'''
* WarpBot stuff element classe
    - element : terre/feu/eau/air/dopou
    - classe : logique poto
pourquoi pas rajouter une manière de spécifier docri/12pa 6pm/etc
l'idée est de renvoyer un message avec la présentation des stuff classiques ou spécifiques à chaque classe selon ce que la personne a mis comme info

* WarpBot calcul invo dofusbook
    - invo : dragonnet/momie/bouftou/craqueleur/sanglier/tofu
    - dofusbook : lien d'un stuff dofusbook (ex : https://d-bk.net/fr/t/9nwN )
l'idée est d'envoyer le calcul des dégats des sorts de l'invo en question par le stuff en question

* WarpBot twitch
donne les infos sur les prochains stream que je vais faire
'''


'''
idée présentation stuffs : dict avec tous les elements/modes + toutes les classes
chaque element du dict c'est un dict
quand une classe ne contient pas l'element on dit "j'ai pas de scpécifique mais voici les bases de cet element"
bi elem écris de la maniere suivante "terre+feu" mais rangés par ordre alphabétique, histoire de pouvoir créer facilement la string 
'''

#####################
# VARIABLES
#####################
COLORS=dict()
COLORS["terre"]="815633"
COLORS["feu"]="d13800"
COLORS["eau"]="398a89"
COLORS["air"]="2b6f2d"
COLORS["dopou"]="6f5794"
COLORS["multi"]="f3cf0b"

ELEMENTS=['terre', 'feu', 'eau', 'air', 'dopou', 'feu+terre', 'eau+terre', 
          'air+terre', 'dopou+terre', 'eau+feu', 'air+feu', 'dopou+feu', 
          'air+eau', 'dopou+eau', 'air+dopou', 'air+eau+terre', 'air+eau+feu', 
          'air+feu+terre', 'eau+feu+terre', 'air+dopou+eau', 'air+dopou+terre', 
          'dopou+feu+terre', 'air+dopou+feu', 'dopou+eau+feu', 'dopou+eau+terre', 
          'multi']
CLASSES=['xelor', 'enutrof', 'eniripsa', 'osamodas', 'zobal', 'sadida',
       'steamer', 'sacrieur', 'iop', 'pandawa', 'ecaflip', 'cra', 'feca',
       'sram', 'roublard','vide']
#dans elements et classes je rajoute vide et faux pour prendre en compte les cas où on ne remplis pas l'argument de l'un des deux, ça peut être normal

STUFFS=dict()
STUFFS["terre"]={'kolo lunaire roxx': ["<https://d-bk.net/fr/t/8vYb>"],'kolo lunaire res': ["<https://d-bk.net/fr/t/ArAs>"],'kolo lunaire goule': ["<https://d-bk.net/fr/t/ANaF>"],'kolo chasseur ré fixes': ["<https://d-bk.net/fr/t/B0wS>"], 'scaramouchapeau': ["<https://d-bk.net/fr/t/9WxC>"],'plistik wulan': ["<https://d-bk.net/fr/t/BpSq>"], 'cc': [], 'no_cc': []}
STUFFS["feu"]={'bandit lumi': ["<https://d-bk.net/fr/t/A8Zv>"], 'funespadon': ["<https://d-bk.net/fr/t/8yAu>"], 'bandit firefoux': ["<https://d-bk.net/fr/t/7yVX>"], 'no_cc': []}
STUFFS["eau"]={'sanctuaire cryo': ["<https://d-bk.net/fr/t/B7er>"], 'sanctuaire wulan': ["<https://d-bk.net/fr/t/B9MR>"], 'cc': [], 'no_cc': []}
STUFFS["air"]={'no pano, dina usicke': ["<https://d-bk.net/fr/t/9pdy>"], 'no pano, klime sacrif': ["<https://d-bk.net/fr/t/9RJp>"],'ava padgref': ["<https://d-bk.net/fr/t/5qJF>"],'ava allister': ["<https://d-bk.net/fr/t/2EdT>"], 'cc': [], 'no_cc': []}
STUFFS["feu+terre"]={'12/6': [], '11/6': [], 'cc': ["<https://d-bk.net/fr/t/7ESW>"], 'no_cc': ["<https://d-bk.net/fr/t/AwSG>"]}
STUFFS["eau+terre"]={'12/6': [],'11/6': [], 'noctu wulan': ["<https://d-bk.net/fr/t/Azb9>"], 'cc': [], 'no_cc': []}
STUFFS["air+terre"]={'nevark virale': ["<https://d-bk.net/fr/t/Bvq3>"], '11/6': [], 'cc': [], 'no_cc': []}
# STUFFS["dopou+terre"]={'12/6': [], '11/6': [], 'cc': [], 'no_cc': []}
STUFFS["eau+feu"]={'12/6': [], '11/6': [], 'Mazin pnose': ["<https://d-bk.net/fr/t/931X>"], 'cc': [], 'no_cc': []}
STUFFS["air+feu"]={'12/6': [], '11/6': [],'cc': [], 'Padgref strigide': ["<https://d-bk.net/fr/t/7OhS>"], 'no_cc': []}
# STUFFS["dopou+feu"]={'12/6': [], '11/6': [], 'cc': [], 'no_cc': []}
STUFFS["air+eau"]={'12/6': ["<https://d-bk.net/fr/t/8Ql4>"], '11/6': ["<https://d-bk.net/fr/t/BMXD>"], 'cc': ["<https://d-bk.net/fr/t/Br83>"], 'no_cc': []}
STUFFS["dopou+eau"]={'12/6': [], 'full dopou': ["<https://d-bk.net/fr/t/AzPu>"], 'cc': [], 'no_cc': []}
STUFFS["air+dopou"]={'12/6': [], '11/6': [],'ava égarés': ["<https://d-bk.net/fr/t/B150>"], 'full dopou': ["<https://d-bk.net/fr/t/BK5m>"], 'cc': [], 'no_cc': []}
STUFFS["air+eau+terre"]={'12/6': [], '11/6': ["<https://d-bk.net/fr/t/2OhT>"], 'cc': [], 'no_cc': []}
STUFFS["air+eau+feu"]={'12/6': [], '11/6': [], 'cc': ["<https://d-bk.net/fr/t/2OhM>"], 'no_cc': ["<https://d-bk.net/fr/t/BT4t>"]}
STUFFS["air+feu+terre"]={'12/6': [], '11/6': [], 'cc': ["<https://d-bk.net/fr/t/4qgX>"], 'no_cc': ["<https://d-bk.net/fr/t/AP7x>"]}
STUFFS["eau+feu+terre"]={'12/6': [], '11/6': [], 'cc': ["<https://d-bk.net/fr/t/47TD>"], 'no_cc': []}
STUFFS["air+dopou+eau"]={'12/6': ["<https://d-bk.net/fr/t/5kTX>"], '11/6': ["<https://d-bk.net/fr/t/A9Iy>"], 'cc': [], 'no_cc': []}
# STUFFS["air+dopou+terre"]={'12/6': [], '11/6': [], 'cc': [], 'no_cc': []}
# STUFFS["dopou+feu+terre"]={'12/6': [], '11/6': [], 'cc': [], 'no_cc': []}
# STUFFS["air+dopou+feu"]={'12/6': [], '11/6': [], 'cc': [], 'no_cc': []}
STUFFS["dopou+eau+feu"]={'12/6': [], 'full dopou': ["<https://d-bk.net/fr/t/BQQd>"], 'cc': [], 'no_cc': []}
STUFFS["dopou+eau+terre"]={'12/6': [], 'full dopou': ["<https://d-bk.net/fr/t/BQQl>"], 'cc': [], 'no_cc': []}
STUFFS["multi"]={'12/6': [], '11/6': [], 'strigide glours': ["<https://d-bk.net/fr/t/2Ol7>"], 'virale glours wukin': ["<https://d-bk.net/fr/t/Bv6e>"]}
STUFFS["dopou"]={'eau air dopou 11/6' : [STUFFS["air+dopou+eau"]["11/6"][0]]
                ,'eau air dopou 12/6' : [STUFFS["air+dopou+eau"]["12/6"][0]]
                ,'eau dopou' : [STUFFS["dopou+eau"]["full dopou"][0]]
                ,'air dopou' : [STUFFS["air+dopou"]["full dopou"][0]]
                ,'terre eau dopou' : [STUFFS["dopou+eau+terre"]["full dopou"][0]]
                ,'feu eau dopou' : [STUFFS["dopou+eau+feu"]["full dopou"][0]]
                } ### Dopou is always with another element
STUFFS["osamodas"]={'feu' :{'12/6' :["<https://d-bk.net/fr/t/9nwN>"]}
                    ,'eau+feu':{'cher' : ["<https://d-bk.net/fr/t/9UXA>"],'plus abordable' : ["<https://d-bk.net/fr/t/AQSn>"]}
                    ,'air' :{'11/6' :["<https://d-bk.net/fr/t/9Y06>"]}
                    ,'eau' :{'12/6' :["<https://d-bk.net/fr/t/BCMB>"]}                    
                    }
STUFFS["sadida"]={'feu' :{'bandit luminescente' :["<https://d-bk.net/fr/t/9nwN>"]}
                    ,'eau+feu':{'mazin pnose' : ["<https://d-bk.net/fr/t/9UXA>"]}
                    ,'terre' :{'scaramouchapeau lunaire' :["<https://d-bk.net/fr/t/BQpf>"]}
                    # ,'eau+terre' :{'11/6' :["<https://d-bk.net/fr/t/BoWN>"]}                
                    }
STUFFS["iop"]={'dopou' :{'12/6' :["<https://d-bk.net/fr/t/5kTX>"]}              
                    }

IMAGES_LINK=dict()
IMAGES_LINK["twitch"]="https://drive.google.com/uc?id="+"1B7dARplU3Y-0zS77S_JTSqh1gu-tvyIa"#https://drive.google.com/file/d/1B7dARplU3Y-0zS77S_JTSqh1gu-tvyIa/view?usp=sharing
IMAGES_LINK["terre"]="https://drive.google.com/uc?id="+"13rMcJr5wNLaWEOZp7CXrnZkrmh4zvvWr"#"https://drive.google.com/file/d/13rMcJr5wNLaWEOZp7CXrnZkrmh4zvvWr/view?usp=sharing"
IMAGES_LINK["air"]=  "https://drive.google.com/uc?id="+"19PCVHr_1b_bvvgigREB5enX9NNxx4B4-"#"https://drive.google.com/file/d/19PCVHr_1b_bvvgigREB5enX9NNxx4B4-/view?usp=sharing"
IMAGES_LINK["feu"]=  "https://drive.google.com/uc?id="+"1NU5qJ7ETGKPlk2P01L5SXz67z-kZ63RE"#"https://drive.google.com/file/d/1NU5qJ7ETGKPlk2P01L5SXz67z-kZ63RE/view?usp=sharing"
IMAGES_LINK["eau"]=  "https://drive.google.com/uc?id="+"1GorSPzE-Rl7HftV9fj-7kugQQ1ms-WHl"#"https://drive.google.com/file/d/1GorSPzE-Rl7HftV9fj-7kugQQ1ms-WHl/view?usp=sharing"
IMAGES_LINK["dopou"]="https://drive.google.com/uc?id="+"1C0IGM3qztADKcWhx-ElleWSNg0x0-C_D"#"https://drive.google.com/file/d/1C0IGM3qztADKcWhx-ElleWSNg0x0-C_D/view?usp=sharing"
IMAGES_LINK["error"]="https://drive.google.com/uc?id="+"1IXajCU8Qe9Qu2KEmtQf9GZpJZQ0Q1mQc"#"https://drive.google.com/file/d/1IXajCU8Qe9Qu2KEmtQf9GZpJZQ0Q1mQc/view?usp=sharing"
IMAGES_LINK["feu+terre"]=       "https://drive.google.com/uc?id="+"1WBkEeUFqyHl6-TTnN7Hx308sApnrLx4b"#https://drive.google.com/file/d/1WBkEeUFqyHl6-TTnN7Hx308sApnrLx4b/view?usp=sharing
IMAGES_LINK["eau+terre"]=       "https://drive.google.com/uc?id="+"1tpP06if5Jn0Znf9NGx836JonSmuHu5mw"#https://drive.google.com/file/d/1tpP06if5Jn0Znf9NGx836JonSmuHu5mw/view?usp=sharing
IMAGES_LINK["air+terre"]=       "https://drive.google.com/uc?id="+"1GG3Ko9wbAUJ5GAJlL3ZQR33GbznM0Mwa"#https://drive.google.com/file/d/1GG3Ko9wbAUJ5GAJlL3ZQR33GbznM0Mwa/view?usp=sharing
IMAGES_LINK["dopou+terre"]=     "https://drive.google.com/uc?id="+"1MX34nKtjRl7OseIBGiRxPWdjy1n1Mbl3"#https://drive.google.com/file/d/1MX34nKtjRl7OseIBGiRxPWdjy1n1Mbl3/view?usp=sharing
IMAGES_LINK["eau+feu"]=         "https://drive.google.com/uc?id="+"1xfGRTrPA1O-mXzH_p8AFBkbFTc3Rb13x"#https://drive.google.com/file/d/1xfGRTrPA1O-mXzH_p8AFBkbFTc3Rb13x/view?usp=sharing
IMAGES_LINK["air+feu"]=         "https://drive.google.com/uc?id="+"1gL0Vk-HnVV_ExTmbsI-k27VpJ7pH6KRL"#https://drive.google.com/file/d/1gL0Vk-HnVV_ExTmbsI-k27VpJ7pH6KRL/view?usp=sharing
IMAGES_LINK["dopou+feu"]=       "https://drive.google.com/uc?id="+"15ZsxUaFVTW7vGv9CumwaeNQypIzCmcIr"#https://drive.google.com/file/d/15ZsxUaFVTW7vGv9CumwaeNQypIzCmcIr/view?usp=sharing
IMAGES_LINK["air+eau"]=         "https://drive.google.com/uc?id="+"1huDHiTktKhKSYH9HwYnYg1rRPEdwK36n"#https://drive.google.com/file/d/1huDHiTktKhKSYH9HwYnYg1rRPEdwK36n/view?usp=sharing
IMAGES_LINK["dopou+eau"]=       "https://drive.google.com/uc?id="+"1KeEYZZTqsBqnaqa5SbeDQbhjLUie8WoE"#https://drive.google.com/file/d/1KeEYZZTqsBqnaqa5SbeDQbhjLUie8WoE/view?usp=sharing
IMAGES_LINK["air+dopou"]=       "https://drive.google.com/uc?id="+"1BVN5Xgg0DqagzLTcBmLacWMcjOBBhtWX"#https://drive.google.com/file/d/1BVN5Xgg0DqagzLTcBmLacWMcjOBBhtWX/view?usp=sharing
IMAGES_LINK["air+eau+terre"]=   "https://drive.google.com/uc?id="+"1TYzkmD7Zqexg3K_9tyw3eBYBs3FniM9z"#https://drive.google.com/file/d/1TYzkmD7Zqexg3K_9tyw3eBYBs3FniM9z/view?usp=sharing
IMAGES_LINK["air+eau+feu"]=     "https://drive.google.com/uc?id="+"1szOZy3IYBjugqLr1CXk6NpW4KnfZF59g"#https://drive.google.com/file/d/1szOZy3IYBjugqLr1CXk6NpW4KnfZF59g/view?usp=sharing
IMAGES_LINK["air+feu+terre"]=   "https://drive.google.com/uc?id="+"1gMC4SN41sT1g2rTbJHftpqTzuPrS6Jbi"#https://drive.google.com/file/d/1gMC4SN41sT1g2rTbJHftpqTzuPrS6Jbi/view?usp=sharing
IMAGES_LINK["eau+feu+terre"]=   "https://drive.google.com/uc?id="+"1-V9BPis1MR6dT2Zp6yhbD_k1ZW4kOPLQ"#https://drive.google.com/file/d/1-V9BPis1MR6dT2Zp6yhbD_k1ZW4kOPLQ/view?usp=sharing
IMAGES_LINK["air+dopou+eau"]=   "https://drive.google.com/uc?id="+"1jn97glLnA6iR3Wu-D51pvwPtribMmT_p"#https://drive.google.com/file/d/1jn97glLnA6iR3Wu-D51pvwPtribMmT_p/view?usp=sharing
IMAGES_LINK["air+dopou+terre"]= "https://drive.google.com/uc?id="+"15lvhyr2LE4rRVq114tgB241v1q4ebZGA"#https://drive.google.com/file/d/15lvhyr2LE4rRVq114tgB241v1q4ebZGA/view?usp=sharing
IMAGES_LINK["dopou+feu+terre"]= "https://drive.google.com/uc?id="+"1VFuero8gQbfTIZ_0hEBb_9LWNYLeKjfz"#https://drive.google.com/file/d/1VFuero8gQbfTIZ_0hEBb_9LWNYLeKjfz/view?usp=sharing
IMAGES_LINK["air+dopou+feu"]=   "https://drive.google.com/uc?id="+"1H0KF6bFlOxMDPAlb0PxEc6tyTWTuYb9S"#https://drive.google.com/file/d/1H0KF6bFlOxMDPAlb0PxEc6tyTWTuYb9S/view?usp=sharing
IMAGES_LINK["dopou+eau+feu"]=   "https://drive.google.com/uc?id="+"1EfMJiv-ltOpKcR1mZ0b1b_tpCtCQO74u"#https://drive.google.com/file/d/1EfMJiv-ltOpKcR1mZ0b1b_tpCtCQO74u/view?usp=sharing
IMAGES_LINK["dopou+eau+terre"]= "https://drive.google.com/uc?id="+"1pDqCVYu4HXpfcxlLXslC2EpKeuH3epCO"#https://drive.google.com/file/d/1pDqCVYu4HXpfcxlLXslC2EpKeuH3epCO/view?usp=sharing
IMAGES_LINK["multi"]=           "https://drive.google.com/uc?id="+"1sFla0c4Ze-AkuTM_ubTYjLzviTyu-c2f"#https://drive.google.com/file/d/1sFla0c4Ze-AkuTM_ubTYjLzviTyu-c2f/view?usp=sharing
#####################
# MAIN RESPONSE
#####################

# def get_response(user_input: str, user_name : str, channel : str):
#     lowered: str = user_input.lower()

#     if lowered == '':
#         return 'Ok tu arrive à envoyer des messages vides?? Sorcier!'
#     elif lowered =='salut warpbot' :
#         return f'Salut {user_name}!'    
#     elif lowered =='!warpbot lance un dé' or lowered =='!wb lance un dé':
#         return f'Tu as eu: {randint(1, 6)}'
#     elif command :=re.match(r"(?P<botname>!\w+)\s?(?P<function>\w*)\s?(?P<arg1>[+\w]*)\s?(?P<arg2>[a-z0-9\/\.\-:]*)", lowered):
#         print(command.group('botname'),command.group('function'),command.group('arg1'),command.group('arg2'))
#         if command.group('botname')!= '!warpbot' and command.group('botname')!= '!wb':
#             return -1
        
#         if command.group('function')=="stuff": #stuff
#             element = command.group('arg1')
#             classe = command.group('arg2')
#             # print(element,classe)
#             return stuff_response(element=element,classe=classe)
        
#         # elif command.group('function')=="calcul": #calcul
#         #     return calcul_response(command)
        
#         elif command.group('function')=="twitch": #twitch
#             resp= f"""
# Je stream la majorité des tournois pvp sur dofus touch, sauf quand je participe bien sur !
# Au programme :
# - 27/28/29 septembre : stream tournois du serveur Oshimo
# - 4/5/6 octobre : je participe au tournois sur herdegrize
# """
#             return resp
        
#         elif command.group('function')=="help": #help
#             return help_response(command)
        
#         else: #mauvaise fonction
#             resp= f"""
# Argument `{command.group('function')} ` inconnu, les fonctions utilisables sont:
# - help   : pour recevoir de l'aide sur l'utilisation du bot 
# - stuff  : pour recevoir des recommandations de stuff
# - twitch : pour avoir des infos sur les prochains stream de warp
# Tu peux utiliser `!WarpBot help xxx` pour avoir des informations sur comment formuler les requetes avec chacune des 2 fonctions stuff/twitch.
# """
# # - calcul : pour avoir des estimations de dommage d'invocations ou dopou
#             return resp
#     return -1



#####################
# FONCTIONS UTILES
#####################

#prend une liste d'éléments et la met sous la forme elt1+elt2+elt3...
def from_elts_to_multi(elt_list):
    sorted_list=sorted(elt_list)
    return '+'.join(sorted_list)

#prends les éléments sous le format elt1+elt2+elt3... et les remet dans le bon ordre
def lecture_elt(elts):
    elt_spl=[e.strip() for e in elts.replace("/","+").split(r"+")]
    # print(elts,elt_spl)
    if len(elt_spl)==1:
        elt_spl=[e.strip() for e in elts.split(r" ")]
        # print(elts,elt_spl)

    return from_elts_to_multi(elt_spl)

def help_response(command,plateforme="discord"):

    if plateforme=="discord":
        prefixe='/'
    elif plateforme=="twitch":
        prefixe="!"
    else :
        prefixe='/'

    if command=="stuff": #/wbhelp stuff
        resp= f"""
Pour recevoir des recommandations de stuff il faut utiliser la commande `{prefixe}stuff élément classe`
- **élément** : terre/feu/eau/air/dopou/multi ou toute combinaison d'éléments différents (excepté multi) séparés d'un '+', ex: élément+élément+... avec 3 éléments maximum
Exemple de requete valide : `{prefixe}stuff air+eau`
- OPTIONNEL **classe** : une des classes du jeu écrite avec le nom complet, pour recevoir des stuff spécifiques à la classe donnée s'il y en a dans la bibliothèque.
Ce qui nous fait une requete de la forme : `{prefixe}stuff eau+feu osamodas`
"""
#     elif command.group('arg1')=="calcul": #/wbhelp calcul
#         resp= f"""
# TODO : pas de fonction donc pas d'explication pour le moment
# """
    elif command=="twitch": #/wbhelp twitch
        resp= f"""
`{prefixe}twitch` Répond avec les infos sur les prochains stream de prévus (si il n'y a pas de tournois de prévus probablement qu'il n'y aura pas de stream).
"""
    else: #/wbhelp
        resp= f"""
Il y a deux commandes :
- Stuff  : pour recevoir des recommandations de stuff. `{prefixe}wbhelp stuff` pour plus de détails.
- Twitch : pour avoir des infos sur les prochains stream de warp. Pas d'argument à rajouter, `{prefixe}twitch` vous renverra les informations nécessaires.
"""
# - Calcul : pour avoir des estimations de dommage d'invocations ou dopou . `/wbhelp calcul` pour plus de détails.
# - calcul : pour la formulation des calculs de dommage d'invocations ou dopou
    return resp
        
def stuff_response(element,classe,plateforme="discord"):

    elt=lecture_elt(element)
    error=4 #0=ok, 1=element inconnu, 2= classe inconnue, 3=element&classe inconnue,4=erreurs autres
    if plateforme=="discord":
        prefixe='/'
    elif plateforme=="twitch":
        prefixe="!"
    else :
        prefixe='/'
        

    # vérification que les arguments soient corrects
    if not classe in CLASSES and not elt in ELEMENTS: #classe+element non reconnus
        resp=f"""
Je ne reconnais pas les arguments **{elt}** et **{classe}** fournis.
Pour recevoir de l'aide sur l'utilisation de la fonction stuff, taper `{prefixe}wbhelp stuff`.
Elements valides: terre/feu/eau/air/dopou/multi ou toute combinaison d'éléments différents (excepté multi) séparés d'un '+', d'un '/' ou d'un espace.
Pour les classes il faut écrire le nom en entier.
Exemple de requete valide : `{prefixe}stuff eau+feu osamodas`.
"""     
        error=3
        return resp,error
    elif not elt in ELEMENTS: #élément non reconnu
        resp=f"""
Je ne reconnais pas l'élément **{elt}** désolé, pour recevoir de l'aide sur l'utilisation de la fonction stuff, taper `{prefixe}wbhelp stuff`.
Elements valides: terre/feu/eau/air/dopou/multi ou toute combinaison d'éléments différents (excepté multi) séparés d'un '+'.
Exemple de requete valide : `{prefixe}stuff air+eau`.
"""     
        error=1
        return resp,error
    elif not classe in CLASSES: #classe non reconnue
        resp=f"""
Je ne reconnais pas la classe **{classe}** désolé, pour recevoir de l'aide sur l'utilisation de la fonction stuff, taper `{prefixe}wbhelp stuff`.
Il faut écrire le nom de classe en entier.
Exemple de requete valide : `{prefixe}stuff eau+feu osamodas`.
"""     
        error=2
        return resp,error
    
    if classe=='vide': # pas de classe spécifiée
        if elt=="dopou":
            error=0
            resp= f"""
Les dopou ne se jouent pas spécialement tous seuls, meme si ils sont prédominants il y a toujours un élément avec, mes recommandations sont donc les suivantes : 
- eau air dopou : 11/6 {STUFFS["air+dopou+eau"]["11/6"][0]} ou 12/6 {STUFFS["air+dopou+eau"]["12/6"][0]}
- eau dopou : {STUFFS["dopou+eau"]["full dopou"][0]}
- air dopou : {STUFFS["air+dopou"]["full dopou"][0]}
- terre eau dopou : {STUFFS["dopou+eau+terre"]["full dopou"][0]} (fonctionne pour terre dopou)
- feu eau dopou : {STUFFS["dopou+eau+feu"]["full dopou"][0]} (fonctionne pour feu dopou)"""
            return resp,error        
        else:
            if elt in STUFFS.keys():
                error=0
                resp= f"""
Pour un stuff {elt.replace("+","/")} je recommande :\n"""
                for mode in STUFFS[elt].keys():
                    if len(STUFFS[elt][mode])>0:
                        resp+=f"- {mode} : {STUFFS[elt][mode][0]}\n"
                # resp+="N'hésite pas à tag Warp pour plus de détails sur ces stuffs."
                return resp,error

            else: #élément non présent dans la biblio
                error=0
                resp=f"""
Je n'ai pas de stuff dans ma bibliothèque qui corresponde au combo {elt.replace("+","/")}, tu peux tag Warp pour savoir pourquoi et peut-être qu'il aura quelque chose à te proposer."""
                return resp,error
                
    else: #avec une classe précisée
        error=0
        resp='pas trouvé'
        if classe in STUFFS.keys():
            if elt in STUFFS[classe].keys():
                resp=f"""
Pour l'élément {elt.replace("+","/")} de la classe {classe} je te recommande :\n"""
                for mode in STUFFS[classe][elt].keys():
                    if len(STUFFS[classe][elt][mode])>0:
                        resp+=f"- {mode} : {STUFFS[classe][elt][mode][0]}\n"
                # resp+="N'hésite pas à tag Warp pour plus de détails sur ces stuffs."
                
        if resp=='pas trouvé':
            resp=f"""
Je n'ai pas de stuff {elt.replace("+","/")} spécifiques pour la classe {classe}, tu trouveras probablement ton bonheur dans les stuffs classiques de l'élément:\n"""
            for mode in STUFFS[elt].keys():
                if len(STUFFS[elt][mode])>0:
                    resp+=f"- {mode} : {STUFFS[elt][mode][0]}\n"
            # resp+="N'hésite pas à tag Warp pour plus de détails sur ces stuffs."
        return resp,error
    error=4
    resp="Vraisemblablement il y a une erreur dans le code : tu ne devrais pas arriver ici, tag Warp pour qu'il répare le bug stp <3"
    return resp,error

def color_mix(elements):
    try:
        colors_list=[COLORS[k]for k in lecture_elt(elements).split('+')]
    except: #erreur dans les éléments
        return int("000000",16)
    tot_weight = len(colors_list)
    red = int(sum([int(k[:2], 16) for k in colors_list])/tot_weight)
    green = int(sum([int(k[2:4], 16) for k in colors_list])/tot_weight)
    blue = int(sum([int(k[4:6], 16) for k in colors_list])/tot_weight)
    zpad = lambda x: x if len(x)==2 else '0' + x
    
    return int(zpad(hex(red)[2:]) + zpad(hex(green)[2:]) + zpad(hex(blue)[2:]), 16)

def image_response(element):
    elt=lecture_elt(element)
    try:
        image=IMAGES_LINK[elt]
    except:
        image=IMAGES_LINK['error']
    return image
    
def calcul_response(command,plateforme="discord"):

    if plateforme=="discord":
        prefixe='/'
    elif plateforme=="twitch":
        prefixe="!"
    else :
        prefixe='/'
    if command.group('arg1')=="dopou": #/calcul dopou

        resp= f"""
Pour recevoir des recommandations de stuff il faut utiliser la fonction `{prefixe}stuff élément classe`
- **élément** : terre/feu/eau/air/dopou/multi ou toute combinaison de ces éléments (excepté multi) séparés d'un '+', ex: élément+élément+... avec 3 éléments maximum
Exemple de requete valide : `/stuff air+eau`
- **classe** : une des classes du jeu écrite avec le nom complet, pour recevoir des stuff spécifiques à la classe donnée s'il y en a dans la bibliothèque.
Ce qui nous fait une requete de la forme : `{prefixe}stuff eau+feu osamodas`
"""
    
    elif command.group('arg1')=='': #/calcul 
        resp= f"""

"""
    else: #/calcul dqzdzqd , arg1 erroné
        resp= f"""

"""
    return resp