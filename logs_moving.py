import re
import asyncio
from datetime import datetime, timezone
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import create_engine, Column, Integer, BigInteger, String, TIMESTAMP, JSON, text
from sqlalchemy.ext.declarative import declarative_base
import discord
from discord.ext import commands

from dotenv import load_dotenv
import os
from PanoDB_link import CONNECTION_STRING
from typing import Final

# ----------------------------
# CONFIGURATION
# ----------------------------

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
from typing import Final

LOG_CHANNEL_ID = 1335368709157421056  # ID du channel où tes logs sont postés
# CONNECTION_STRING = "mysql+mysqlconnector://user:password@localhost:3306/ma_base"


# ----------------------------
# SETUP SQLALCHEMY
# ----------------------------

engine = create_engine(CONNECTION_STRING, echo=False)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class CommandLog(Base):
    __tablename__ = 'command_logs'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    executed_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    user_id = Column(BigInteger, nullable=True)
    user_name = Column(String(100), nullable=False)
    guild_id = Column(BigInteger, nullable=True)
    guild_name = Column(String(100), nullable=False)
    channel_id = Column(BigInteger, nullable=True)
    channel_name = Column(String(100), nullable=False)
    command = Column(String(50), nullable=False)
    arguments = Column(JSON)

Base.metadata.create_all(engine)

# ----------------------------
# FONCTION DE LOG
# ----------------------------

def command_log(user_name, user_id, server_name, server_id, channel_name, channel_id, command_name, arguments, date=None):
    session = Session()
    
    try:
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
        if date:
            log_kwargs["executed_at"] = date

        log_entry = CommandLog(**log_kwargs)
        session.add(log_entry)
        session.commit()
        print(f"[LOG] Commande '{command_name}' exécutée par {user_name} enregistrée.")
    
    except SQLAlchemyError as e:
        session.rollback()
        print(f"[ERREUR LOG] Impossible d’enregistrer la commande '{command_name}': {e}")
    
    finally:
        session.close()

# ----------------------------
# BOT DISCORD
# ----------------------------

intents = discord.Intents.default()
intents.members = True  # pour récupérer les membres
bot = commands.Bot(command_prefix="!", intents=intents)

# Regex pour parser les messages avec ou sans arguments
pattern = re.compile(
    r"(?P<user_name>.+) used /(?P<command>\S+)(?: with args: (?P<args>.+?))? in server (?P<guild>.+) channel (?P<channel>.+)"
)

@bot.event
async def on_ready():
    print(f"Bot connecté comme {bot.user}")
    
    channel = bot.get_channel(LOG_CHANNEL_ID)
    if channel is None:
        print("Channel non trouvé.")
        return

    print("Récupération des messages historiques...")
    
    async for message in channel.history(limit=None, oldest_first=True):
        match = pattern.match(message.content)
        if not match:
            continue
        
        user_name = match.group("user_name")
        command_name = match.group("command")
        guild_name = match.group("guild")
        channel_name = match.group("channel")
        executed_at = message.created_at.replace(tzinfo=timezone.utc)
        
        # Arguments en dict
        args_dict = {}
        args_str = match.group("args")
        if args_str:
            for pair in args_str.split(" | "):
                if ": " in pair:
                    key, value = pair.split(": ", 1)
                    args_dict[key] = value
        
        # IDs Discord
        guild_id = None
        user_id = None
        channel_id = None

        guild_obj = discord.utils.get(bot.guilds, name=guild_name)
        if guild_obj:
            guild_id = guild_obj.id
            member_obj = discord.utils.get(guild_obj.members, name=user_name)
            if member_obj:
                user_id = member_obj.id
            channel_obj = discord.utils.get(guild_obj.channels, name=channel_name)
            if channel_obj:
                channel_id = channel_obj.id
        
        # Log dans la DB
        command_log(
            user_name=user_name,
            user_id=user_id,
            server_name=guild_name,
            server_id=guild_id,
            channel_name=channel_name,
            channel_id=channel_id,
            command_name=command_name,
            arguments=args_dict,
            date=executed_at
        )

    print("Import des logs terminé.")
    await bot.close()  # fermer le bot une fois terminé

# ----------------------------
# LANCEMENT DU BOT
# ----------------------------

bot.run(TOKEN)