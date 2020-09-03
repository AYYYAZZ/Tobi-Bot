import discord
from discord.ext import commands
import youtube_dl
import ctypes
import ctypes.util
import os
import asyncio

ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}   


class Test(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        
    @commands.command()
    @commands.is_owner()
    async def test(self, ctx, url: str):
        
        def endSong(self, guild, path):
            os.remove(path)
         #link to your song on YouTube
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            file = ydl.extract_info(url, download=True)
            guild = "743761540758503444" #id of your server which you can get by right clicking on server name and clicking "Copy ID" (developer mode must be on)
            path = str(file['title']) + "-" + str(file['id'] + ".mp3")
        
        await ctx.message.author.voice.channel.connect(reconnect=True)                                     
        
        voice_client.play(discord.FFmpegPCMAudio(path), after=lambda x: endSong(guild, path))
        voice_client.source = discord.PCMVolumeTransformer(voice_client.source, 1)
        
        while voice_client.is_playing(): #waits until song ends
            await asyncio.sleep(1)
        else:
            await voice_client.disconnect() #and disconnects
            print("Disconnected")
    
def setup(bot):
    bot.add_cog(Test(bot))
