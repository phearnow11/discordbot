from discord.team import Team
from discord.ext.commands import cog
import discord
from discord.ext import commands
from discord.utils import get

from youtube_dl import YoutubeDL

class music_cog(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

        self.is_playing = False

        self.user_add = []
        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        self.FFMPEG_OPTIONS = {'before_options':'-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        self.vc = ""
    
    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception:
                return False
        
        return {'source': info['formats'][0]['url'], 'title': info['title']}
    
    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing= True

            m_url = self.music_queue[0][0]['source']

            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing= False
    
    async def play_music(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']
        

            if self.vc == "" or not self.vc.is_connected() or self.vc == None:
                self.vc = await self.music_queue[0][1].connect()
            else:
                await self.vc.move_to(self.music_queue[0][1])
            
            print(self.music_queue)
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False
    
    @commands.command(name="play", help="Chơi nhạc")
    async def p(self, ctx, *args):
        query = " ".join(args)
        user = ctx.message.author.mention
        
        
        voice_channel = ctx.author.voice.channel
        if voice_channel is None:
            await ctx.send("**Vào kênh đi cha nội !!**")
        else:
            song = self.search_yt(query)
  
            if type(song) == type(True):
                await ctx.send("**Lỗi không thêm được thử cái khác xem**")
            else:
                await ctx.send(f"**Thêm bài {song} vào queue**")
                self.music_queue.append([song, voice_channel])
                self.user_add.append(user)
                
                if self.is_playing == False:
                    await self.play_music()

    @commands.command(name="queue", help="Hiện queue nhạc")
    async def q(self, ctx):
  
        retval = ""
        for i in range(0, len(self.music_queue)):
            a = i+1
            retval += f"{a}. " + self.music_queue[i][0]['title'] + f" add by \n"
        
        print(retval)
        if retval != "":
            await ctx.send(f"**{retval}**")
        else:
            await ctx.send("**Không có nhạc trong queue**")

    @commands.command(name="skip", help="Skip")
    async def skip(self, ctx):

        if self.vc != "" and self.vc:
            self.vc.stop()
            await self.play_music()
            await ctx.send(f"**Chuyển sang bài tiếp theo**")
        else:
          await ctx.send("**Không còn bài để chuyển nữa**")
    
    @commands.command(name = "resume", help="resume nhạc")
    async def resume(self, ctx):
      voice = get(self.bot.voice_clients, guild=ctx.guild)
      voice.resume()

      user = ctx.message.author.mention
      await ctx.send(f"{user} cho chạy tiếp nhạc")

    @commands.command(name = "pause", help ="pause nhạc")
    async def pause(self, ctx):
      voice = get(self.bot.voice_clients, guild=ctx.guild)
      voice.pause()

      user = ctx.message.author.mention
      await ctx.send(f"{user} pause nhạc")