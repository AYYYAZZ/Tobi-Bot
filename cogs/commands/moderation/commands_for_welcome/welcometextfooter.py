import discord
from discord.ext import commands
import os
import asyncpg, asyncio
import psycopg2

database = os.environ.get('DATABASE')
user = os.environ.get('USER')
password = os.environ.get('PASSWORD')
host = os.environ.get('HOST')
port = os.environ.get('PORT')

conn = psycopg2.connect(
    database = f"{database}", 
    user = f"{user}", 
    password = f"{password}", 
    host = f"{host}", 
    port = "5432"
)

cursor = conn.cursor()

class WelcomeTextFooter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_guild = True)
    async def wfooter(self, ctx, footer: str = None):

        try:
            
            guild = ctx.message.guild
            
            if footer is not None:
                cursor.execute(f'UPDATE public."Texts_For_Welcome" SET footer = \'{footer}\' WHERE guild_id = \'{guild.id}\';')
                conn.commit()
            else:
                cursor.execute(f'UPDATE public."Texts_For_Welcome" SET footer = Null WHERE guild_id = \'{guild.id}\';')
                conn.commit()
            
            emb = discord.Embed(
                title = 'Успешно!!!',
                description = f'Текст для footer был успешно установлен',
                colour = discord.Color.green(),
                timestamp = ctx.message.created_at
            )
            
            if ctx.guild.system_channel is not None:
                await ctx.guild.system_channel.send(embed = emb)
            elif ctx.guild.system_channel is None:
                await ctx.send(embed = emb)

        except commands.MissingPermissions:
            await ctx.send('Эту команду могут использовать только те у кого в роли есть Управлять сервером')

        except Exception as e:
            print(e)


def setup(bot):
    bot.add_cog(WelcomeTextFooter(bot))