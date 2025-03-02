import os
import asyncio
import random
from twitchio.ext import commands
from twitchio.ext import routines
from dotenv import load_dotenv
from responses import help_response,stuff_response


# Variables d'environnement pour le token et le canal
load_dotenv()

BOT_TOKEN = os.getenv("TMI_TOKEN")  
CHANNEL = os.getenv("CHANNEL")      
CLIENT_ID = os.getenv("CLIENT_ID")      
NICK = os.getenv("BOT_NICK")      
PREFIX = os.getenv("BOT_PREFIX")      

class TwitchBot(commands.Bot):

    def __init__(self):
        super().__init__(   token=BOT_TOKEN,
                            client_id=CLIENT_ID,
                            nick=NICK,
                            prefix=PREFIX,
                            initial_channels=[CHANNEL]
                        )
        self.participants = []
        self.tirage_en_cours = False  # Flag pour vérifier si un tirage est en cours
    
    async def event_ready(self):
        print(f"Bot {self.nick} connecté et prêt sur le canal {CHANNEL}.")
        for channel in self.connected_channels:
            await channel.send(f"Salut à tous ! WarpBot à votre service!")

    async def event_message(self, message):
        if  not message.author or message.author.name.lower() == self.nick.lower(): #si le message.author est noneType ou si l'auteur est le bot lui-même on renvoie rien
            return
        await self.handle_commands(message)

    @commands.command(name="salut")
    async def hello(self, ctx):
        await ctx.send(f"Salut, {ctx.author.name}! Heureux de te voir sur le stream!")

    @commands.command(name="join")
    async def join(self, ctx):
        """Commandes pour participer au tirage"""
        if self.tirage_en_cours:
            if ctx.author.name not in self.participants:
                self.participants.append(ctx.author.name)
                await ctx.send(f"{ctx.author.name} a rejoint le tirage !")
            else:
                await ctx.send(f"{ctx.author.name}, tu es déjà inscrit au tirage.")
        else:
            await ctx.send("Le tirage n'a pas encore commencé. Tapez la commande !start pour démarrer un tirage.")

    @commands.command(name="tirage",)
    async def start(self, ctx, seconds: int = 300):
        """Commandes pour démarrer le tirage"""

        # vérifie que l'auteur a les droits modo
        if not ctx.author.is_mod:  # Vérifie si l'auteur de la commande est un modérateur
            await ctx.send("Tu dois être modérateur pour démarrer un tirage.")
            return


        if not self.tirage_en_cours:
            self.tirage_en_cours = True
            self.participants = []  # Réinitialise les participants
            if seconds%60==0:
                await ctx.send(f"Le tirage commence ! Tapez !join pour participer. Vous avez {str(int(seconds//60))} minutes.")
            else:
                await ctx.send(f"Le tirage commence ! Tapez !join pour participer. Vous avez {str(int(seconds//60))} minutes et {str(int(seconds%60))} secondes.")
            
            # Attendre X secondes avec un message de rappel toutes les minutes
            for i in range(seconds//60):
                await asyncio.sleep(60)
                if seconds%60==0:
                    await ctx.send(f"Tirage en cours ! Tapez !join pour participer. Il vous reste {str(int((seconds-60*i)//60))} minutes.")
                else:
                    await ctx.send(f"Tirage en cours ! Tapez !join pour participer. Il vous reste {str(int((seconds-60*i)//60))} minutes et {str(int(seconds%60))} secondes.")
            await asyncio.sleep(seconds%60)

            # Effectuer le tirage si des participants se sont inscrits
            if len(self.participants)>0:
                winner = random.choice(self.participants)
                await ctx.send(f"Le tirage est terminé ! Le gagnant est {winner} ! Félicitations !")
            else:
                await ctx.send("Aucun participant n'a rejoint le tirage.")
            
            
            # Réinitialiser l'état du tirage
            self.tirage_en_cours = False

        else:
            await ctx.send("Un tirage est déjà en cours. Veuillez attendre qu'il se termine.")

    # @commands.command(name="stuff")
    # async def stuff(self, ctx, element: str, classe: str = "vide"):
    #     """Commande pour obtenir un stuff en fonction d'un élément et d'une classe"""
        
    #     response = stuff_response(element.strip().lower(),classe.strip().lower(),plateforme="twitch")
    #     # Envoi de la réponse dans le chat
    #     await ctx.send(response)

    # @commands.command(name="wbhelp")
    # async def help(self, ctx, commande: str ='vide'):
    #     """Commande pour obtenir une aide sur les commandes du bot"""

    #     response=help_response(commande.strip().lower(),plateforme="twitch")
        
    #     # Envoi de la réponse dans le chat
    #     await ctx.send(response)

# Initialisation et lancement du bot
if __name__ == "__main__":
    bot = TwitchBot()
    bot.run()



# @commands.command(name="enter")
#     async def enter(self, ctx):
#         if ctx.author.name not in self.participants:
#             self.participants.append(ctx.author.name)
#             await ctx.send(f"{ctx.author.name} a été ajouté(e) au tirage au sort!")
#         else:
#             await ctx.send(f"{ctx.author.name}, tu es déjà dans le tirage au sort!")

#     @commands.command(name="pick_winner")
#     async def pick_winner(self, ctx):
#         if ctx.author.is_mod:
#             if self.participants:
#                 winner = random.choice(self.participants)
#                 await ctx.send(f"🎉 Félicitations, {winner} ! Tu as gagné le tirage au sort!")
#                 self.participants.clear()  # Réinitialise les participants après le tirage
#             else:
#                 await ctx.send("Il n'y a pas de participants pour le moment.")
#         else:
#             await ctx.send("Désolé, seule la modération peut tirer un gagnant.")

#     @commands.command(name="participants")
#     async def participants(self, ctx):
#         if self.participants:
#             participants_list = ", ".join(self.participants)
#             await ctx.send(f"Participants au tirage au sort : {participants_list}")
#         else:
#             await ctx.send("Il n'y a pas de participants pour le moment.")



# # load environment variables
# load_dotenv()

# BOT_TOKEN = os.getenv("TMI_TOKEN")  
# CHANNEL = os.getenv("CHANNEL")      
# CLIENT_ID = os.getenv("CLIENT_ID")      
# NICK = os.getenv("BOT_NICK")      
# PREFIX = os.getenv("BOT_PREFIX")      


# # set up the bot
# bot = commands.Bot(
#     token=BOT_TOKEN,
#     client_id=CLIENT_ID,
#     nick=NICK,
#     prefix=PREFIX,
#     initial_channels=[CHANNEL]
# )

# # @bot.event
# async def event_ready():
#     'Called once when the bot goes online.'
#     print(f"{NICK} is online!")
#     ws = bot._ws  # this is only needed to send messages within event_ready
#     await ws.send_privmsg(CHANNEL, f"/me has landed!")

# # @bot.event
# async def event_message(ctx):
#     'Runs every time a message is sent in chat.'

#     # make sure the bot ignores itself and the streamer
#     if ctx.author.name.lower() == NICK.lower():
#         return

#     await bot.handle_commands(ctx)

#     # await ctx.channel.send(ctx.content)

#     if 'hello' in ctx.content.lower():
#         await ctx.channel.send(f"Hi, @{ctx.author.name}!")


# @bot.command(name='test')
# async def test(ctx):
#     await ctx.send('test passed!')


# if __name__ == "__main__":
#     bot.run()

















