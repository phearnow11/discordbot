import discord 
from discord.ext import commands
from music import music_cog


Bot = commands.Bot(command_prefix='>')

Bot.add_cog(music_cog(Bot))




Bot.run("ODg0MTU0NzgzMTkwMDkzODY1.YTUXTw.JzRYZE0IhxhT-TXFWM84c1-3prQ")