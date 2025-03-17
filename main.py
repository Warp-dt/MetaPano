from typing import Final
import os
import signal
from dotenv import load_dotenv
import discord
from discord import Intents, Interaction, InteractionType, Embed, app_commands
from discord.ext import commands
import signal
import asyncio
import sys
import aiohttp

from responses import help_response,color_mix,IMAGES_LINK,image_response,CLASSES, filter_sort_main_elts,ELEMENTS_PRINCIPAUX, no_secondary_elt,no_main_elt
from PanoDB_link import find_stuff


# STEP 0: LOAD OUR TOKEN FROM SOMEWHERE SAFE
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# STEP 1: BOT SETUP
intents: Intents = Intents.default()
intents.message_content = True 
bot = commands.Bot(command_prefix='!', intents=intents)

# STEP 2: HANDLING THE STARTUP FOR OUR BOT
@bot.event
async def on_ready() -> None:
    print(f'{bot.user} is now running!')
    # Sync the slash commands once the bot is ready
    try:
        await bot.tree.sync()
        print("Slash commands have been synced successfully!")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

    ### récupération des emoji
    # Initialiser une session HTTP si elle n'existe pas déjà
    if not hasattr(bot, 'http_session'):
        bot.http_session = aiohttp.ClientSession()
    # Récupérer les informations de l'application
    application = await bot.application_info()    
    # Récupérer les emojis d'application via l'API HTTP
    await fetch_application_emojis(application.id)
    
    ### display des serveurs sur lequel le bot est installé
    channel = bot.get_channel(1308510294506606623)
    if channel is not None:
        try:
            await channel.send("Hello World!")
            # liste des serveurs dans lesquels le bot est présent
            for guild in bot.guilds:
                print(f"Server: {guild.name} | Members count: {guild.member_count}")
                # print(guild.icon)
                # print(guild.owner)
                # print(guild.banner)
                # print(guild.members)
                # print(guild.preferred_locale)
                # for member in guild.members:
                #     print(member) # prints all members names one by one
                print('_________')
            print("Activation message sent successfully.")
            
        except Exception as e:
            print(f"Failed to send activation message: {e}")

# Commands logging
@bot.event
async def on_interaction(interaction):
        # Vérifie si l'interaction est une commande
    if interaction.type == InteractionType.application_command and not interaction.response.is_done():
        channel = bot.get_channel(1335368709157421056)
        server = interaction.guild.name
        user = interaction.user
        command = interaction.command.name
        cmd_channel = interaction.channel
        
        # Récupération des arguments
        options = []
        if interaction.data.get('options'):
            for option in interaction.data['options']:
                option_name = option['name']
                option_value = option['value']
                options.append(f"{option_name}: {option_value}")
        
        # Création du message avec les arguments si présents
        if options:
            args_str = ' | '.join(options)
            log_message = f'{user} used /{command} with args: {args_str} in server {server} channel {cmd_channel}'
        else:
            log_message = f'{user} used /{command} in server {server} channel {cmd_channel}'
        
        # print(log_message)
        await channel.send(log_message)

############################################################################################
# @bot.event
# async def on_disconnect():
#     print("My battery is low and it's getting dark.")

# ## STEP 2.1 : HANDLING THE SHUTDOWN
# async def shutdown_handler():
#     """Sends a message to the target channel before shutting down."""
#     channel = bot.get_channel(1308510294506606623)
#     if channel is not None:
#         try:
#             await channel.send("My battery is low and it's getting dark.")
#             print("Shutdown message sent successfully.")
#         except Exception as e:
#             print(f"Failed to send shutdown message: {e}")

# def handle_exit(signum, frame):
#     """Capture termination signals and shut down gracefully."""
#     print("Shutting down bot...")
#     loop = bot.loop
#     if loop.is_running():
#         loop.create_task(shutdown_handler())
#     loop.stop()

# # Register signals (e.g., SIGINT for Ctrl+C)
# signal.signal(signal.SIGINT, handle_exit)
# signal.signal(signal.SIGTERM, handle_exit)
############################################################################################
# Flag global pour suivre si le message a été envoyé
shutdown_message_sent = False

class GracefulExit(SystemExit):
    pass

async def shutdown_handler():
    """Sends a message to the target channel before shutting down."""
    global shutdown_message_sent
    print("Initiating shutdown sequence...")
    
    if not shutdown_message_sent:
        channel = bot.get_channel(1308510294506606623)
        if channel is not None:
            try:
                await channel.send("My battery is low and it's getting dark.")
                shutdown_message_sent = True
                print("Shutdown message sent successfully.")
            except Exception as e:
                print(f"Failed to send shutdown message: {e}")
    
    try:
        await bot.close()
        print("Bot connection closed successfully.")
    except Exception as e:
        print(f"Error during bot shutdown: {e}")
    
    raise GracefulExit()

def signal_handler(signum, frame):
    """Handle termination signals."""
    print(f"Received signal {signum}")
    if asyncio.get_event_loop().is_running():
        asyncio.create_task(shutdown_handler())
    else:
        sys.exit(0)

# Register signal handlers
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

@bot.event
async def on_disconnect():
    global shutdown_message_sent
    print("Bot disconnected from Discord.")
    
    if not shutdown_message_sent:
        channel = bot.get_channel(1308510294506606623)
        if channel is not None and bot.is_ready():
            try:
                await channel.send("My battery is low and it's getting dark.")
                shutdown_message_sent = True
                print("Disconnection message sent successfully.")
            except Exception as e:
                print(f"Failed to send disconnection message: {e}")
############################################################################################
# STEP 3: SLASH COMMAND IMPLEMENTATION

CRITERES=["Élément","Classe","PA","PM","PO","Invo","Lvl"]
ELEMENTS_DB=['air','dopou', 'eau','feu','terre','cc','initiative','soin','retrait pa', 'retrait pm', 'esquive pa', 'esquive pm', 'repou', 'recri', 'tank', 'pp', 'sagesse','pods','pvp', 'pvm']
LVL_TRANCHES=["200","199","198-195"]+[str(195-k*5-1)+'-'+str(190-k*5) for k in range(21)]+["<90"]


class LvlSelect(discord.ui.Select):
    def __init__(self,criteres_restants,criteres_val):
        
        self.criteres_restants=criteres_restants[1:]
        self.criteres_val=criteres_val
        options = [
            discord.SelectOption(label=choice, value=choice)
            for choice in LVL_TRANCHES
        ]
        super().__init__(
            placeholder="Tranche de lvl",
            min_values=1,
            max_values=25,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        self.criteres_val["Lvl"]=self.values
        self.view.clear_items()
        await interaction.response.defer()
        await interaction.followup.send(
            embed=resultat_embed(self.criteres_val),  
            view=self.view,
            ephemeral=False)

class InvoSelect(discord.ui.Select):
    def __init__(self,criteres_restants,criteres_val):
        
        self.criteres_restants=criteres_restants[1:]
        self.criteres_val=criteres_val
        options = [
            discord.SelectOption(label=choice, value=choice)
            for choice in list(range(6,0,-1))
        ]
        super().__init__(
            placeholder="Nombre d'invo minimum",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        self.criteres_val["Invo"]=self.values[0]
        self.view.clear_items()
        if len(self.criteres_restants)>0:
            if self.criteres_restants[0]=="Lvl":
                self.view.add_item(LvlSelect(criteres_restants=self.criteres_restants,criteres_val=self.criteres_val))
            else:
                print("probleme dans les criteres on n'est pas censé arriver là!")

            await interaction.response.send_message(
                embed=next_critere_embed(self.criteres_restants), 
                view=self.view,
                ephemeral=True)
        else:
            await interaction.response.defer()
            await interaction.followup.send(
                embed=resultat_embed(self.criteres_val),  
                view=self.view,
                ephemeral=False)

class POSelect(discord.ui.Select):
    def __init__(self,criteres_restants,criteres_val):
        
        self.criteres_restants=criteres_restants[1:]
        self.criteres_val=criteres_val
        options = [
            discord.SelectOption(label=choice, value=choice)
            for choice in list(range(6,0,-1))
        ]
        super().__init__(
            placeholder="PO minimum",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        self.criteres_val["PO"]=self.values[0]
        self.view.clear_items()
        if len(self.criteres_restants)>0:
            if self.criteres_restants[0]=="Invo":
                self.view.add_item(InvoSelect(criteres_restants=self.criteres_restants,criteres_val=self.criteres_val))
            elif self.criteres_restants[0]=="Lvl":
                self.view.add_item(LvlSelect(criteres_restants=self.criteres_restants,criteres_val=self.criteres_val))
            else:
                print("probleme dans les criteres on n'est pas censé arriver là!")

            await interaction.response.send_message(
                embed=next_critere_embed(self.criteres_restants), 
                view=self.view,
                ephemeral=True)
        else:
            await interaction.response.defer()
            await interaction.followup.send(
                embed=resultat_embed(self.criteres_val),  
                view=self.view,
                ephemeral=False)
            
class PM6Button(discord.ui.Button):
    def __init__(self,criteres_restants,criteres_val):
        
        self.criteres_restants=criteres_restants[1:]
        self.criteres_val=criteres_val
        super().__init__(label="6", style=discord.ButtonStyle.primary)
    
    async def callback(self, interaction: discord.Interaction):
        self.view.clear_items()
        self.criteres_val["PM"]='6'
        if len(self.criteres_restants)>0:
            if self.criteres_restants[0]=="PO":
                self.view.add_item(POSelect(criteres_restants=self.criteres_restants,criteres_val=self.criteres_val))
            elif self.criteres_restants[0]=="Invo":
                self.view.add_item(InvoSelect(criteres_restants=self.criteres_restants,criteres_val=self.criteres_val))
            elif self.criteres_restants[0]=="Lvl":
                self.view.add_item(LvlSelect(criteres_restants=self.criteres_restants,criteres_val=self.criteres_val))
            else:
                print("probleme dans les criteres on n'est pas censé arriver là!")
                
            await interaction.response.send_message(
                embed=next_critere_embed(self.criteres_restants), 
                view=self.view,
                ephemeral=True)
        else:
            await interaction.response.defer()
            await interaction.followup.send(
                embed=resultat_embed(self.criteres_val),  
                view=self.view,
                ephemeral=False)
            
class PM5Button(discord.ui.Button):
    def __init__(self,criteres_restants,criteres_val):
        
        self.criteres_restants=criteres_restants[1:]
        self.criteres_val=criteres_val
        super().__init__(label="5", style=discord.ButtonStyle.primary)
    
    async def callback(self, interaction: discord.Interaction):
        self.view.clear_items()
        self.criteres_val["PM"]='5'
        if len(self.criteres_restants)>0:
            if self.criteres_restants[0]=="PO":
                self.view.add_item(POSelect(criteres_restants=self.criteres_restants,criteres_val=self.criteres_val))
            elif self.criteres_restants[0]=="Invo":
                self.view.add_item(InvoSelect(criteres_restants=self.criteres_restants,criteres_val=self.criteres_val))
            elif self.criteres_restants[0]=="Lvl":
                self.view.add_item(LvlSelect(criteres_restants=self.criteres_restants,criteres_val=self.criteres_val))
            else:
                print("probleme dans les criteres on n'est pas censé arriver là!")
                
            await interaction.response.send_message(
                embed=next_critere_embed(self.criteres_restants), 
                view=self.view,
                ephemeral=True)
        else:
            await interaction.response.defer()
            await interaction.followup.send(
                embed=resultat_embed(self.criteres_val),  
                view=self.view,
                ephemeral=False)
        
class PA11Button(discord.ui.Button):
    def __init__(self,criteres_restants,criteres_val):
        
        self.criteres_restants=criteres_restants[1:]
        self.criteres_val=criteres_val
        super().__init__(label="11", style=discord.ButtonStyle.primary)
    
    async def callback(self, interaction: discord.Interaction):
        self.view.clear_items()
        self.criteres_val["PA"]='11'
        if len(self.criteres_restants)>0:
            if self.criteres_restants[0]=="PM":###
                self.view.add_item(PM6Button(criteres_restants=self.criteres_restants,criteres_val=self.criteres_val))
                self.view.add_item(PM5Button(criteres_restants=self.criteres_restants,criteres_val=self.criteres_val))
            elif self.criteres_restants[0]=="PO":###
                self.view.add_item(POSelect(criteres_restants=self.criteres_restants,criteres_val=self.criteres_val))
            elif self.criteres_restants[0]=="Invo":
                self.view.add_item(InvoSelect(criteres_restants=self.criteres_restants,criteres_val=self.criteres_val))
            elif self.criteres_restants[0]=="Lvl":
                self.view.add_item(LvlSelect(criteres_restants=self.criteres_restants,criteres_val=self.criteres_val))
            else:
                print("probleme dans les criteres on n'est pas censé arriver là!")
                
            await interaction.response.send_message(
                embed=next_critere_embed(self.criteres_restants), 
                view=self.view,
                ephemeral=True)
        else:
            await interaction.response.defer()
            await interaction.followup.send(
                embed=resultat_embed(self.criteres_val),  
                view=self.view,
                ephemeral=False)
            
class PA12Button(discord.ui.Button):
    def __init__(self,criteres_restants,criteres_val):
        
        self.criteres_restants=criteres_restants[1:]
        self.criteres_val=criteres_val
        super().__init__(label="12", style=discord.ButtonStyle.primary)
    
    async def callback(self, interaction: discord.Interaction):
        self.view.clear_items()
        self.criteres_val["PA"]='12'

        if len(self.criteres_restants)>0:
            if self.criteres_restants[0]=="PM":###
                self.view.add_item(PM6Button(criteres_restants=self.criteres_restants,criteres_val=self.criteres_val))
                self.view.add_item(PM5Button(criteres_restants=self.criteres_restants,criteres_val=self.criteres_val))
            elif self.criteres_restants[0]=="PO":###
                self.view.add_item(POSelect(criteres_restants=self.criteres_restants,criteres_val=self.criteres_val))
            elif self.criteres_restants[0]=="Invo":
                self.view.add_item(InvoSelect(criteres_restants=self.criteres_restants,criteres_val=self.criteres_val))
            elif self.criteres_restants[0]=="Lvl":
                self.view.add_item(LvlSelect(criteres_restants=self.criteres_restants,criteres_val=self.criteres_val))
            else:
                print("probleme dans les criteres on n'est pas censé arriver là!")
                
            await interaction.response.send_message(
                embed=next_critere_embed(self.criteres_restants), 
                view=self.view,
                ephemeral=True)
        else:
            await interaction.response.defer()
            await interaction.followup.send(
                embed=resultat_embed(self.criteres_val),  
                view=self.view,
                ephemeral=False)

class ClasseSelect(discord.ui.Select):
    def __init__(self,criteres_restants,criteres_val):
        
        self.criteres_restants=criteres_restants[1:]
        self.criteres_val=criteres_val
        options = [
            discord.SelectOption(label=choice, value=choice)
            for choice in CLASSES
        ]
        super().__init__(
            placeholder="Classe désirée",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        self.criteres_val["Classe"]=self.values[0]
        self.view.clear_items()
        if len(self.criteres_restants)>0:
            if self.criteres_restants[0]=="Lvl":
                self.view.add_item(LvlSelect(criteres_restants=self.criteres_restants,criteres_val=self.criteres_val))
            elif self.criteres_restants[0]=="PA":
                self.view.add_item(PA12Button(criteres_restants=self.criteres_restants,criteres_val=self.criteres_val))
                self.view.add_item(PA11Button(criteres_restants=self.criteres_restants,criteres_val=self.criteres_val))
            elif self.criteres_restants[0]=="PM":###
                self.view.add_item(PM6Button(criteres_restants=self.criteres_restants,criteres_val=self.criteres_val))
                self.view.add_item(PM5Button(criteres_restants=self.criteres_restants,criteres_val=self.criteres_val))
            elif self.criteres_restants[0]=="PO":###
                self.view.add_item(POSelect(criteres_restants=self.criteres_restants,criteres_val=self.criteres_val))
            elif self.criteres_restants[0]=="Invo":
                self.view.add_item(InvoSelect(criteres_restants=self.criteres_restants,criteres_val=self.criteres_val))
            else:
                print("probleme dans les criteres on n'est pas censé arriver là!")
                
            await interaction.response.send_message(
                embed=next_critere_embed(self.criteres_restants),  
                view=self.view,
                ephemeral=True)
        else:
            await interaction.response.defer()
            await interaction.followup.send(
                embed=resultat_embed(self.criteres_val),  
                view=self.view,
                ephemeral=False)


class ElementSelect(discord.ui.Select):
    def __init__(self,criteres_restants,criteres_val):
        
        self.criteres_restants=criteres_restants[1:]
        self.criteres_val=criteres_val
        options = [
            discord.SelectOption(label=choice, value=choice)
            for choice in ELEMENTS_DB
        ]
        super().__init__(
            placeholder="Élément(s) voulu(s)",
            min_values=1,
            max_values=19,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        self.criteres_val["Élément"]=self.values
        self.view.clear_items()
        if len(self.criteres_restants)>0:
            if self.criteres_restants[0]=="Classe":
                self.view.add_item(ClasseSelect(criteres_restants=self.criteres_restants,criteres_val=self.criteres_val))
            elif self.criteres_restants[0]=="PA":
                self.view.add_item(PA12Button(criteres_restants=self.criteres_restants,criteres_val=self.criteres_val))
                self.view.add_item(PA11Button(criteres_restants=self.criteres_restants,criteres_val=self.criteres_val))
            elif self.criteres_restants[0]=="PM":
                self.view.add_item(PM6Button(criteres_restants=self.criteres_restants,criteres_val=self.criteres_val))
                self.view.add_item(PM5Button(criteres_restants=self.criteres_restants,criteres_val=self.criteres_val))
            elif self.criteres_restants[0]=="PO":
                self.view.add_item(POSelect(criteres_restants=self.criteres_restants,criteres_val=self.criteres_val))
            elif self.criteres_restants[0]=="Invo":
                self.view.add_item(InvoSelect(criteres_restants=self.criteres_restants,criteres_val=self.criteres_val))
            elif self.criteres_restants[0]=="Lvl":
                self.view.add_item(LvlSelect(criteres_restants=self.criteres_restants,criteres_val=self.criteres_val))
            else:
                print("probleme dans les criteres on n'est pas censé arriver là!")
                
            await interaction.response.send_message(
                embed=next_critere_embed(self.criteres_restants),  
                view=self.view,
                ephemeral=True)
        else:
            await interaction.response.defer()
            await interaction.followup.send(
                embed=resultat_embed(self.criteres_val),  
                view=self.view,
                ephemeral=False)

class CriteresSelect(discord.ui.Select):
    def __init__(self):
        self.criteres_val=dict()
        options = [
            discord.SelectOption(label=crit, value=crit)
            for crit in CRITERES
        ]
        super().__init__(
            placeholder="Choisissez les critères de sélection pour votre stuff",
            min_values=1,
            max_values=7,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        self.view.clear_items()
        sorted_criteres_restants=[item for item in CRITERES if item in self.values]
        if sorted_criteres_restants[0]=="Élément":
            self.view.add_item(ElementSelect(criteres_restants=sorted_criteres_restants,criteres_val=self.criteres_val))
        elif sorted_criteres_restants[0]=="Classe":
            self.view.add_item(ClasseSelect(criteres_restants=sorted_criteres_restants,criteres_val=self.criteres_val))
        elif sorted_criteres_restants[0]=="PA":
            self.view.add_item(PA12Button(criteres_restants=sorted_criteres_restants,criteres_val=self.criteres_val))
            self.view.add_item(PA11Button(criteres_restants=sorted_criteres_restants,criteres_val=self.criteres_val))
        elif sorted_criteres_restants[0]=="PM":
            self.view.add_item(PM6Button(criteres_restants=sorted_criteres_restants,criteres_val=self.criteres_val))
            self.view.add_item(PM5Button(criteres_restants=sorted_criteres_restants,criteres_val=self.criteres_val))
        elif sorted_criteres_restants[0]=="PO":
            self.view.add_item(POSelect(criteres_restants=sorted_criteres_restants,criteres_val=self.criteres_val))
        elif sorted_criteres_restants[0]=="Invo":
            self.view.add_item(InvoSelect(criteres_restants=sorted_criteres_restants,criteres_val=self.criteres_val))
        elif sorted_criteres_restants[0]=="Lvl":
            self.view.add_item(LvlSelect(criteres_restants=sorted_criteres_restants,criteres_val=self.criteres_val))
        else:
            print("probleme dans les criteres on n'est pas censé arriver là!")


        await interaction.response.send_message(
            embed=next_critere_embed(sorted_criteres_restants), 
            view=self.view,
            ephemeral=True)

def resultat_embed(criteres : dict,assouplissement=None):
    if assouplissement is None:
        assouplissement = []

    stuff_list=find_stuff(criteres)

    if len(stuff_list)>0:
        # lors du renvoi de tous les stuff d'une classe, séparer par éléments primordiaux et mettre indication des éléments secondaires
        if "Élément" in criteres.keys():
            color=color_mix(criteres["Élément"])
            titre=f'Stuffs {" ".join(criteres["Élément"])}'
            if "Classe" in criteres.keys():
                titre+=' '+criteres["Classe"]
        else:
            color=color_mix(["vide"])
            if "Classe" in criteres.keys():
                titre=f'Stuffs {criteres["Classe"]}'
        embed = Embed(
            title=titre,
            color=color #0x773d02#607d83
        )
        try:
            illustration=IMAGES_LINK['+'.join(filter_sort_main_elts(criteres["Élément"]))]
        except:
            try:
                illustration=IMAGES_LINK[criteres["Classe"]]
            except:
                illustration=IMAGES_LINK["harry"]
        
        embed.set_thumbnail(url=illustration)  # URL d'une image pour l'illustration

        #field criteres
        content_criteres=''
        for crit in criteres.keys():
            if crit=="Élément":
                content_criteres+=f"- {crit} : "
                for c in criteres[crit]:
                    content_criteres+=f"<:{c.replace(' ','')}:{bot.application_emojis[c.replace(' ','')]}>"
                content_criteres+="\n"
            elif crit=="Classe":
                content_criteres+=f"- {crit} : <:{criteres[crit].replace(' ','')}:{bot.application_emojis[criteres[crit].replace(' ','')]}>\n"
            elif crit in ["PA",'PM','PO','Invo']:
                content_criteres+=f"- <:{crit.replace(' ','')}:{bot.application_emojis[crit.replace(' ','')]}> : {criteres[crit]}\n"
            else:
                content_criteres+=f"""- {crit} : {str(criteres[crit]).replace("[","").replace("]","").replace("'","")}\n"""

        if len(assouplissement)>0:
            content_criteres+="Je n'ai pas trouvé de stuff répondant à tous les critères demandés, j'ai du retirer:\n"
            assou_dopou=True
            for c_assou,v_assou in assouplissement:
                if c_assou=="Élément_dopou":
                    content_criteres+=f"- {'Élément'} :"
                    all_elts_crit=v_assou
                    for cd,vd in assouplissement:
                        if cd=="Élément":
                            all_elts_crit=vd
                    for elt_retitré in set(criteres["Élément"])^set(all_elts_crit):
                        content_criteres+=f"<:{elt_retitré.replace(' ','')}:{bot.application_emojis[elt_retitré.replace(' ','')]}>"
                    content_criteres+="\n"
                    assou_dopou=False
                elif c_assou=="Élément" and assou_dopou:
                    content_criteres+=f"- {c_assou} :"
                    for elt_retitré in set(v_assou)^set(criteres["Élément"]):
                        content_criteres+=f"<:{elt_retitré.replace(' ','')}:{bot.application_emojis[elt_retitré.replace(' ','')]}>"
                    content_criteres+="\n"
                else :
                    content_criteres+=f"- {c_assou}\n"
        embed.add_field(name="Critères", value=content_criteres, inline=True)

        #field(s) stuffs    
        if (not "Élément" in criteres.keys()) and "Classe" in criteres.keys():
            content_dict=dict()
            for stuff in stuff_list:
                elt=" ".join(filter_sort_main_elts(stuff['Elements'].split(",")))
                # print("stuff['Elements']",stuff['Elements'],"elt",elt)
                if elt in content_dict.keys():
                    content_dict[elt]+=f"- [**{stuff['Nom']}**](https://d-bk.net/fr/t/{stuff['DB_surl']})\n"
                else:
                    content_dict[elt]=f"- [**{stuff['Nom']}**](https://d-bk.net/fr/t/{stuff['DB_surl']})\n"

            for elt_princi in content_dict:
                # print("elt_princi",elt_princi)
                if ' ' in elt_princi:
                    emoji_elt=''.join([f'<:{e.replace(" ","")}:{bot.application_emojis[e.replace(" ","")]}>' for e in elt_princi.split(' ')])
                else:
                    emoji_elt=f'<:{elt_princi.replace(" ","")}:{bot.application_emojis[elt_princi.replace(" ","")]}>'
                embed.add_field(name=f"{elt_princi}{emoji_elt}", value=content_dict[elt_princi], inline=True)

        else:
            content_dblink=''
            for stuff in stuff_list:
                content_dblink+=f"- [**{stuff['Nom']}**](https://d-bk.net/fr/t/{stuff['DB_surl']})\n"
                if len(content_dblink)>800:
                    content_dblink+="D'autres stuffs existent mais je n'ai pas assez de place ici pour tous les lister, précise ta recherche."
                    break
            embed.add_field(name="Liens dofusbook", value=content_dblink, inline=True)
        embed.set_footer(text="Si tu as une question n'hésite pas à la poser à Warp ou sur le discord Dofus Touls.")
        return embed
    
    else: #on a pas trouvé de stuff, on va donc assouplir les critères pour essayer de trouver quelque chose de proche
        criteres_altérés=criteres.copy()
        if "PO" in criteres:
            # print("PO")
            criteres_altérés.pop('PO')
            assouplissement.insert(0,('PO',criteres["PO"]))
        elif "Invo" in criteres:
            # print("Invo")
            criteres_altérés.pop('Invo')
            assouplissement.insert(0,('Invo',criteres["Invo"]))
        elif "Élément" in criteres and not no_secondary_elt(criteres["Élément"]) and not no_main_elt(criteres["Élément"]): #si on a filtré sur les éléments et si il y a un élément non principal dans la liste, j'avoue la formulation est bizarre mais ça marche tkt
            criteres_altérés["Élément"]=filter_sort_main_elts(criteres_altérés["Élément"])
            assouplissement.insert(0,("Élément",criteres["Élément"]))
            # print("Élément")
        elif "Élément" in criteres and "dopou" in criteres["Élément"] and len(criteres["Élément"])>1: #si on a filtré sur les éléments et si il y a dopou dans les éléments et qu'il y a plus d'un élément (principaux seulement car les non principaux ont été enlevés à la condition précédente)
            criteres_altérés["Élément"]=["dopou"]
            assouplissement.insert(0,("Élément_dopou",criteres["Élément"]))
            # print("Élément dopou")
        elif "Classe" in criteres:
            # print("Classe")
            criteres_altérés.pop('Classe')
            assouplissement.insert(0,('Classe',criteres["Classe"]))
        elif "PM" in criteres:
            # print("PM")
            criteres_altérés.pop('PM')
            assouplissement.insert(0,('PM',criteres["PM"]))
        elif "PA" in criteres:
            # print("PA")
            criteres_altérés.pop('PA')
            assouplissement.insert(0,('PA',criteres["PA"]))
        else:
            #vraiment t'as forcé fréro c'est quoi cette combinaison d'éléments du démon que tu nous a cook
            if "Élément" in criteres.keys():
                color=color_mix(criteres["Élément"])
            else:
                color=color_mix(["vide"])
            embed = Embed(
                title="Oups",
                color=color#0xff0000 #0x773d02#607d83
            )
            try:
                illustration=IMAGES_LINK['+'.join(filter_sort_main_elts(criteres["Élément"]))]
            except:
                illustration=IMAGES_LINK["error"]
            embed.set_thumbnail(url=IMAGES_LINK["error"]) 
            embed.add_field(name=f'Élément {" ".join(criteres["Élément"])} vide',value="Je n'ai pas de stuff dans ma base pour cet élément ou cette combinaison d'éléments.")
            embed.set_footer(text="Si tu as une question n'hésite pas à la poser à Warp ou sur le discord Dofus Touls.")    
            return embed
        
        # print(criteres_altérés,assouplissement)
        return resultat_embed(criteres_altérés,assouplissement)



def next_critere_embed(criteres_restants : list):
    crit=criteres_restants[0]
    embed = Embed(
        title=crit,
        color=0x773d02#607d83
    )
    embed.set_thumbnail(url=IMAGES_LINK["harry"])  # URL d'une image pour l'illustration

    content=""
    if crit=="Élément":
        content="Sélectionne l'élément ou la combinaison d'éléments de ton choix."
    elif crit=="Classe":
        content="Sélectionne la classe de ton choix."
    elif crit=="Lvl":
        content="Sélectionne la ou les tranches de niveaux de ton choix."
    elif crit in ["PA","PM","PO"]:
        content=f"Sélectionne le nombre minimal de {crit} que tu veux."
    elif crit == 'Invo':
        content="Sélectionne le nombre minimal d'invocations que tu veux."

    embed.add_field(name=content, value="", inline=False)
    return embed

#choix proposés 
@app_commands.choices(classe=[app_commands.Choice(name=cl, value=cl) for cl in CLASSES])
# @app_commands.choices(element=[app_commands.Choice(name=elt, value=elt) for elt in ELEMENTS_DB]) #on ne peut pas l'utiliser car y'a possibilité de combinaisons 

# Stuff command
@bot.tree.command(name="stuff", description="Pour trouver le stuff de tes rêves.")
async def stuff(interaction: Interaction, 
                element: str="vide", 
                classe: str="vide", 
                pa_min: app_commands.Range[int, 0, 12]=0, 
                pm_min: app_commands.Range[int, 0, 6]=0, 
                po_min: app_commands.Range[int, -10, 6]=0, 
                invo_min: app_commands.Range[int, -10, 6]=0,
                lvl_max: app_commands.Range[int, 0, 200] = 0):
    if element=="vide" and classe=="vide" and lvl_max==0 and pa_min==0 and pm_min==0 and po_min==0 and invo_min==0: #sans arg
        embed = Embed(
            title=f"Conseils de stuff",
            color=0x773d02#607d83
        )
        embed.set_thumbnail(url=IMAGES_LINK["harry"])  # URL d'une image pour l'illustration
        
        content="""
- Élément
- Classe
- PA, PM, PO, Invo minimums
- Tranche de lvl souhaitée (par défaut 200)
"""
        embed.add_field(name="Critères de sélection disponibles : ", value=content, inline=False)
        view = discord.ui.View(timeout=600.0)
        view.add_item(CriteresSelect())
        await interaction.response.send_message(
            embed=embed,
            view=view,
            ephemeral=True)
        
    else : #avec au moins un arg
        criteres=dict()
        elt_error=[]
        if element!="vide":
            element_list=element.strip().lower().replace("/","+").replace(" ","+").split("+")
            criteres['Élément']=[]
            for elt in element_list:
                if elt in ELEMENTS_DB:
                    criteres['Élément'].append(elt)
                else : 
                    elt_error.append(elt)
        if lvl_max!=0 and lvl_max!=200:
            if lvl_max>50:
                criteres["Lvl"]=[f"{lvl_max}-{lvl_max-20}"]
            else:
                criteres["Lvl"]=[f"{lvl_max}-{0}"]        
        if classe!="vide":
            criteres["Classe"]=classe
        if pa_min!=0:
            criteres["PA"]=str(pa_min)
        if pm_min!=0:
            criteres["PM"]=str(pm_min) 
        if po_min!=0:
            criteres["PO"]=str(po_min) 
        if invo_min!=0:
            criteres["Invo"]=str(invo_min) 
        
        if len(elt_error)==0: #si il n'y a pas eu d'erreur
            # print("crit", criteres)
            resp=resultat_embed(criteres)
            await interaction.response.send_message(
                embed=resp, 
                ephemeral=False)
        else: #erreur dans les éléménts
            embed = Embed(
                title=f"Erreur dans les éléménts",
                color=0x000000#607d83
            )
            embed.set_thumbnail(url=IMAGES_LINK["error"])  # URL d'une image pour l'illustration
            err_resp=""
            for err in elt_error:
                err_resp+=f"Element `{err}` non reconnu.\n"
            err_resp+="""\nListe des éléments valides :
- air, eau, feu, terre, dopou, cc, initiative, soin, retrait pa, retrait pm, esquive pa, esquive pm, repou, recri, tank, pp, sagesse, pods, pvp, pvm
Et toute combinaison de ces éléments."""
            # print("err_resp",err_resp)
            embed.add_field(name='Liste des erreurs :', value=err_resp)
            await interaction.response.send_message(
                embed=embed, 
                ephemeral=True)


# # context command
# @bot.tree.context_menu(name="test_contexte")
# async def test_contexte(interaction: Interaction, member : discord.Member):
#     await interaction.response.send_message(f"member joined at : {member.joined_at}")

# help command
@bot.tree.command(name="help", description="Besoin d'aide sur l'utilisation du bot?")
async def help(interaction: Interaction, commande: str ='vide'):
    resp=help_response(commande.strip().lower())
    embed = Embed(
        title=f"Aide",
        color=0xff0000  
    )

    embed.set_thumbnail(url=IMAGES_LINK["error"])  # URL d'une image pour l'illustration
    embed.add_field(name="Comment utiliser WarpBot?", value=(resp), inline=False)
    await interaction.response.send_message(embed=embed)

# twitch command
@bot.tree.command(name="twitch", description="Pour avoir des infos sur les prochains streams de Warp.")
async def twitch(interaction: Interaction):
    embed = Embed(
        title=f"Twitch",
        color=0x6441a5  # Couleur twitch
    )

    embed.set_thumbnail(url=IMAGES_LINK["twitch"])  # URL d'une image pour l'illustration
    embed.add_field(name="Lien de la chaîne :",value=("[**warp_is_fine**](https://www.twitch.tv/warp_is_fine)"), inline=False)
    embed.add_field(name="Planning :", value=(f"""
Je stream la majorité des tournois pvp sur dofus touch, sauf quand je participe bien sur !
Au programme :
- Pas de tournois en ce moment mais quasi tous les soirs je stream des 3v3 kamas!
"""), inline=False)
    embed.set_footer(text="N'hésite pas à follow pour être au courant quand je lance un stream.")
    await interaction.response.send_message(embed=embed)

# Youtube command
@bot.tree.command(name="youtube", description="Pour avoir des infos sur la chaine Youtube de Warp.")
async def twitch(interaction: Interaction):
    embed = Embed(
        title=f"Youtube",
        color=0xFF0000 # Couleur twitch
    )
    embed.set_thumbnail(url=IMAGES_LINK["youtube"])  # URL d'une image pour l'illustration
    embed.add_field(name="Lien de la chaîne :",value=("[**Warp-dt**](https://www.youtube.com/channel/UCVMa-curO2R2fJNQALwB2tQ)"), inline=False)
    embed.add_field(name="Contenu :", value=(f"""
Sur ma chaîne youtube je poste la majorité des rediff des matchs que je stream, mais aussi des vidéos exclusives !"""), inline=False)
    embed.set_footer(text="N'hésite pas à t'abonner pour être au courant quand je sors une nouvelle vidéo.")
    await interaction.response.send_message(embed=embed)

# Dofusbook command
@bot.tree.command(name="dofusbook", description="Le lien de la bibliothèque de stuff sur dofusbook/")
async def twitch(interaction: Interaction):
    embed = Embed(
        title=f"Dofusbook",
        color=0x1b3a57 # Couleur twitch
    )
    embed.set_thumbnail(url=IMAGES_LINK["dofusbook"])  # URL d'une image pour l'illustration
    embed.add_field(name="Bibliothèque de stuffs :",value=("[**MetaPano**](https://d-bk.net/fr/tl/4BAS)"), inline=False)
    embed.add_field(name="Contenu :", value=(f"""
Tous les stuffs que le bot va recommander sont présents dans ce compte dofusbook, c'est en quelques sorte la base de connaissance du bot."""), inline=False)
    embed.set_footer(text="Si tu as une question n'hésite pas à la poser à Warp ou sur le discord Dofus Touls.")
    await interaction.response.send_message(embed=embed)

#################################################################################### emojis

async def fetch_application_emojis(application_id):
    # L'URL de l'API pour les emojis d'application
    url = f"https://discord.com/api/v10/applications/{application_id}/emojis"
    
    # Les headers nécessaires, incluant le token du bot
    headers = {
        "Authorization": f"Bot {bot.http.token}",
        "Content-Type": "application/json"
    }
    
    try:
        async with bot.http_session.get(url, headers=headers) as response:
            if response.status == 200:
                emojis_data = await response.json()
                
                # structurer les informations utiles
                emojis_dict=dict()
                for emo in emojis_data["items"]:
                    emojis_dict[emo["name"]]=emo["id"]

                # Stocker les données pour utilisation ultérieure
                bot.application_emojis = emojis_dict
                print(f"Emojis récupérés!")
                return emojis_dict
            else:
                error_text = await response.text()
                print(f"Erreur API récupération emojis: {response.status}, {error_text}")
                return None
    except Exception as e:
        print(f"Erreur lors de la requête: {e}")
        return None

# @bot.tree.command()
# async def app_emojis(interaction: Interaction):
#     if hasattr(bot, 'application_emojis') and bot.application_emojis:
#         # Formatter et afficher les emojis
#         emoji_info = "\n".join([f"Nom: {emoji}, ID: {bot.application_emojis[emoji]}, <:{emoji}:{bot.application_emojis[emoji]}>" for emoji in bot.application_emojis])
#         await interaction.response.send_message(f"Emojis de l'application:\n{emoji_info[:1900]}")
        
#         # # Exemple d'utilisation d'un emoji si disponible
#         # if bot.application_emojis:
#         #     emoji = bot.application_emojis[0]
#         #     emoji_id = emoji['id']
#         #     emoji_name = emoji['name']
#         #     await interaction.response.send_message(f"Exemple d'emoji: <:{emoji_name}:{emoji_id}>")
#     else:
#         await interaction.response.send_message("Aucun emoji d'application trouvé ou non encore chargé.")

# @bot.tree.command()
# async def reload_emojis(interaction: Interaction):
#     application = await bot.application_info()
#     emojis = await fetch_application_emojis(application.id)
#     if emojis:
#         await interaction.response.send_message(f"Rechargement réussi, {len(emojis)} emojis trouvés.")
#     else:
#         await interaction.response.send_message("Échec du rechargement des emojis.")

# N'oubliez pas de fermer la session HTTP lors de la fermeture du bot
@bot.event
async def on_shutdown():
    if hasattr(bot, 'http_session'):
        await bot.http_session.close()



























# STEP 4: MAIN ENTRY POINT
def main() -> None:
    bot.run(TOKEN)


if __name__ == '__main__':
    main()
