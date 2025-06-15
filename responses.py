#####################
# VARIABLES
#####################
COLORS=dict()
COLORS["terre"]="815633"
COLORS["feu"]="d13800"
COLORS["eau"]="398a89"
COLORS["air"]="2b6f2d"
COLORS["dopou"]="fa8400"
COLORS["multi"]="f3cf0b"
COLORS["vide"]="773d02"
COLORS["soin"]="ff59e0"
COLORS["cc"]="EE2C20"
COLORS["initiative"]="982DB3"
COLORS["pp"]="229CE1"
COLORS["sagesse"]="8162FF"
COLORS["pods"]="A46D41"
COLORS["repou"]="FC4903"
COLORS["recri"]="FF4233"
COLORS["retrait pa"]="30F8FC"
COLORS["retrait pm"]="83AF3D"
COLORS["esquive pa"]="30F8FC"
COLORS["esquive pm"]="83AF3D"

ELEMENTS=['terre', 'feu', 'eau', 'air', 'dopou', 'feu+terre', 'eau+terre', 
          'air+terre', 'dopou+terre', 'eau+feu', 'air+feu', 'dopou+feu', 
          'air+eau', 'dopou+eau', 'air+dopou', 'air+eau+terre', 'air+eau+feu', 
          'air+feu+terre', 'eau+feu+terre', 'air+dopou+eau', 'air+dopou+terre', 
          'dopou+feu+terre', 'air+dopou+feu', 'dopou+eau+feu', 'dopou+eau+terre', 
          'multi',"vide"]
CLASSES=['cra', 'ecaflip', 'eniripsa', 'enutrof', 'feca', 'iop', 'osamodas', 'pandawa',
         'roublard','sacrieur', 'sadida', 'sram', 'steamer', 'xelor','zobal','vide']
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
IMAGES_LINK["air+eau+feu+terre"]="https://drive.google.com/uc?id="+"1sFla0c4Ze-AkuTM_ubTYjLzviTyu-c2f"#https://drive.google.com/file/d/1sFla0c4Ze-AkuTM_ubTYjLzviTyu-c2f/view?usp=sharing
IMAGES_LINK["multi"]=           "https://drive.google.com/uc?id="+"1sFla0c4Ze-AkuTM_ubTYjLzviTyu-c2f"#https://drive.google.com/file/d/1sFla0c4Ze-AkuTM_ubTYjLzviTyu-c2f/view?usp=sharing
IMAGES_LINK["vide"]=IMAGES_LINK["multi"]
IMAGES_LINK["livre"]=           "https://drive.google.com/uc?id="+"1dgPyJFURlrr79gsMyoWTPFo8NntDkXob"#https://drive.google.com/file/d/1dgPyJFURlrr79gsMyoWTPFo8NntDkXob/view?usp=sharing
IMAGES_LINK["harry"]=           "https://drive.google.com/uc?id="+"1vm8hxVat2uv0zMs7lsa2dF31Fkb_AkFw"#https://drive.google.com/file/d/1vm8hxVat2uv0zMs7lsa2dF31Fkb_AkFw/view?usp=sharing
IMAGES_LINK["youtube"]=           "https://drive.google.com/uc?id="+"17LoeB0RmVWyD4EL3kX8toXzIISW-jlu6"#https://drive.google.com/file/d/17LoeB0RmVWyD4EL3kX8toXzIISW-jlu6/view?usp=sharing
IMAGES_LINK["dofusbook"]=       "https://drive.google.com/uc?id="+"1yDRYdRmBz5zxIfZTWbqzC4W4oDLTvVai"#https://drive.google.com/file/d/1yDRYdRmBz5zxIfZTWbqzC4W4oDLTvVai/view?usp=sharing

IMAGES_LINK["cra"]=         "https://drive.google.com/uc?id="+"1W0yIPA_r-iX7sHlOUQMyL0CCENAUavzD"# https://drive.google.com/file/d/1W0yIPA_r-iX7sHlOUQMyL0CCENAUavzD/view?usp=sharing
IMAGES_LINK["ecaflip"]=     "https://drive.google.com/uc?id="+"14IWUtmmdPPnIcOwV_IiBisIcGtqr4bNH"#https://drive.google.com/file/d/14IWUtmmdPPnIcOwV_IiBisIcGtqr4bNH/view?usp=sharing
IMAGES_LINK["eniripsa"]=    "https://drive.google.com/uc?id="+"1gmVI9bqu3g67pQbGkOVhDnt0oJlOExH2"#https://drive.google.com/file/d/1gmVI9bqu3g67pQbGkOVhDnt0oJlOExH2/view?usp=sharing
IMAGES_LINK["enutrof"]=     "https://drive.google.com/uc?id="+"1g3Wk0bwnbYuuCklmWgWWA_j2JW7vC0uO"#https://drive.google.com/file/d/1g3Wk0bwnbYuuCklmWgWWA_j2JW7vC0uO/view?usp=sharing
IMAGES_LINK["feca"]=        "https://drive.google.com/uc?id="+"19wy0EztiLpfoX8m05MgmWFneqlGUDStq"#https://drive.google.com/file/d/19wy0EztiLpfoX8m05MgmWFneqlGUDStq/view?usp=sharing
IMAGES_LINK["iop"]=         "https://drive.google.com/uc?id="+"14zqpUXaa6Vvzk-IynOTd27FaG_iocxj-"#https://drive.google.com/file/d/14zqpUXaa6Vvzk-IynOTd27FaG_iocxj-/view?usp=sharing
IMAGES_LINK["osamodas"]=    "https://drive.google.com/uc?id="+"15Jumw7bmFqPE6_ED-6lvsx12rD0nOgFa"#https://drive.google.com/file/d/15Jumw7bmFqPE6_ED-6lvsx12rD0nOgFa/view?usp=sharing
IMAGES_LINK["pandawa"]=     "https://drive.google.com/uc?id="+"1Q3ZtJ3DKJP1yecaKgzNRQ-T1b4RS8VuA"#https://drive.google.com/file/d/1Q3ZtJ3DKJP1yecaKgzNRQ-T1b4RS8VuA/view?usp=sharing
IMAGES_LINK["roublard"]=    "https://drive.google.com/uc?id="+"11yfOyZHbR-Ex0mU1jBx4Hq2RiMvjeN9B"#https://drive.google.com/file/d/11yfOyZHbR-Ex0mU1jBx4Hq2RiMvjeN9B/view?usp=sharing
IMAGES_LINK["sacrieur"]=    "https://drive.google.com/uc?id="+"1ItDn6e0ATFxHFfub0FVQ3wBYi2m03mag"#https://drive.google.com/file/d/1ItDn6e0ATFxHFfub0FVQ3wBYi2m03mag/view?usp=sharing
IMAGES_LINK["sadida"]=      "https://drive.google.com/uc?id="+"1RdbCi1_lNeZFLcJD4eNnHJPY1kIu96uh"#https://drive.google.com/file/d/1RdbCi1_lNeZFLcJD4eNnHJPY1kIu96uh/view?usp=sharing
IMAGES_LINK["sram"]=        "https://drive.google.com/uc?id="+"1TLoJ1Dg-Y31aIrPDj8vg1A6H-hzSr-DP"#https://drive.google.com/file/d/1TLoJ1Dg-Y31aIrPDj8vg1A6H-hzSr-DP/view?usp=sharing
IMAGES_LINK["steamer"]=     "https://drive.google.com/uc?id="+"1IV_-lIEsKEvfmOVOpdTelHAAYBCgWe6h"#https://drive.google.com/file/d/1IV_-lIEsKEvfmOVOpdTelHAAYBCgWe6h/view?usp=sharing
IMAGES_LINK["xelor"]=       "https://drive.google.com/uc?id="+"1p_DCP4it8tL7EEradWE7B0e3bCjPIl21"#https://drive.google.com/file/d/1p_DCP4it8tL7EEradWE7B0e3bCjPIl21/view?usp=sharing
IMAGES_LINK["zobal"]=       "https://drive.google.com/uc?id="+"1Feh1asb3iKvVvB5ABcrAiyDz35VTkiUO"#https://drive.google.com/file/d/1Feh1asb3iKvVvB5ABcrAiyDz35VTkiUO/view?usp=sharing

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
ELEMENTS_PRINCIPAUX=['air','dopou','eau', 'feu','terre']

def no_secondary_elt(elt_list): #renvoie true si la liste est composée uniquement d'éléments principaux
    for e in elt_list:
        if not e in ELEMENTS_PRINCIPAUX:
            return False
    return True

def no_main_elt(elt_list): #renvoie true si la liste est composée uniquement d'éléments secondaires
    for e in elt_list:
        if e in ELEMENTS_PRINCIPAUX:
            return False
    return True

def filter_sort_main_elts(elt_list):
    filt_sort=[e for e in ELEMENTS_PRINCIPAUX if e in elt_list]
    return filt_sort

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
`{prefixe}stuff` : 
- Sans arguments derrière la commande le bot t'envoie une interface à travers laquelle tu donne tes critères pour le stuff que tu veux.
- Si tu connais déjà le fonctionnement du bot tu peux directement spécifier tes critères dans la commande en remplissant les arguments pour gagner du temps. Exemple : `/stuff element:terre eau classe:enutrof`
- Liste des éléments valides : air, eau, feu, terre, dopou, cc, initiative, soin, retrait pa, retrait pm, esquive pa, esquive pm, repou, recri, tank, pp, sagesse, pods, pvp, pvm
"""    
    elif command=="twitch": #/wbhelp twitch
        resp= f"""
`{prefixe}twitch` Renvoie les informations relative à la chaîne Twitch.
"""
    elif command=="youtube": #/wbhelp twitch
        resp= f"""
`{prefixe}youtube` Renvoie les informations relative à la chaîne Youtube.
"""
    else: #/wbhelp
        resp= f"""
Actuellement les commandes disponibles sont les suivantes :
- </stuff:1290488859909423174> : Pour recevoir des recommandations de stuff selon des critères au choix
- </help:1350823984421273652> : Pour une aide sur l'utilisation du bot
- </twitch:1290500457659371563> : Pour les dernières news sur la chaîne Twitch
- </youtube:1350823984421273653> : Pour les dernières news de la chaîne Youtube
- </dofusbook:1351208176120238110> : Pour avoir le lien de la bibliothèque de stuff
- </bibliotheques:1372970032837165059> : Pour savoir quelles sont les bibliothèques utilisées dans ce serveur
- </change_bibliotheque_canal:1383835695046721659> : Pour changer la bibliothèque de stuff source du canal
- </change_bibliotheque_serveur:1383835695046721660> : Pour changer la bibliothèque de stuff source par défaut du serveur
- </supprime_bibliotheque_canal:1383835695046721661> : Pour supprimer la bibliothèque de stuff source du canal
- </supprime_bibliotheque_serveur:1383835695046721662> : Pour supprimer la bibliothèque de stuff source par défaut du serveur

Pour plus d'informations sur l'utilisation de ces commandes, tu peux taper `/help <commande>` ou aller voir la documentation sur [Dofus Touls](https://discord.gg/TcrNrRE5QV).
"""
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
        if elt=="vide": #sans élément précisé
            if classe in STUFFS.keys(): #si on a au moins un stuff spécifique à la classe
                resp=f"""
Pour l'élément {elt.replace("+","/")} de la classe {classe} je te recommande :\n"""
                for c_elt in STUFFS[classe].keys():
                    for mode in STUFFS[classe][c_elt].keys():
                        if len(STUFFS[classe][c_elt][mode])>0:
                            resp+=f"- {c_elt.replace('+','/')} | {mode} : {STUFFS[classe][c_elt][mode][0]}\n"
                # resp+="N'hésite pas à tag Warp pour plus de détails sur ces stuffs."
                    
            if resp=='pas trouvé':
                resp=f"""
    Je n'ai pas de stuff {elt.replace("+","/")} spécifiques pour la classe {classe}, tu trouveras probablement ton bonheur dans les stuffs classiques de l'élément:\n"""
                for mode in STUFFS[elt].keys():
                    if len(STUFFS[elt][mode])>0:
                        resp+=f"- {mode} : {STUFFS[elt][mode][0]}\n"
                # resp+="N'hésite pas à tag Warp pour plus de détails sur ces stuffs."
            return resp,error
        else: #avec un élément
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
    
    colors_list=[COLORS[k]for k in COLORS.keys() if k in elements]
    if len(colors_list)==0:
        return 0x000000
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