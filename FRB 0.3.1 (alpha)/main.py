import asyncio
import discord

import re
import os
from processing import *

from discord.ext import commands
from discord.ext.tasks import loop

asyncio.set_event_loop(asyncio.new_event_loop())

ffmpeg_options = {
    'options': '-vn'
}


setDJ()
print("oof")
class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
      
    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()

    @commands.command()
    async def play(self, ctx):

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("https://flareradio.radioca.st/stream"))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)


    @commands.command(pass_context=True, no_pm=True)
    async def pause(self, ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()

    @commands.command()
    async def volume(self, ctx, volume: int):
        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send("Changed volume to {}%".format(volume))

    @commands.command()
    async def stop(self, ctx):
        await ctx.voice_client.disconnect()

        
    @commands.command()
    async def setChannel(self, ctx, *, channel):
      channel_id = str(re.findall('\d+', channel)[0])
      f = open(str(ctx.message.guild.id)+".data","w")
      f.write(channel_id)
      f.close()
      
    @commands.command()
    async def setVoice(self, ctx, *, voice):
      voice_id = str(re.findall('\d+', voice)[0])
      f = open(str(ctx.message.guild.id)+"_voice.data","w")
      f.write(voice_id)
      f.close()
      
      
    @play.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

bot = commands.Bot(command_prefix=commands.when_mentioned_or("b!"),
                   description='FLARE RADIO PLAYER')





async def background_task():
    await bot.wait_until_ready()
    while not bot.is_closed():
        activity = discord.Game(name=getStat())
        await bot.change_presence(status=discord.Status.online, activity=activity)
        print(getDJ(), oldDJ())
        if not getDJ() == oldDJ():
          setDJ()
          for guild in bot.guilds:
            g = str(guild.id)
            print(g)
            if os.path.isfile(str(g)+'.data'):
              if not getDJ() == "Flare Radio Stream":
                channel = bot.get_channel(getChannel(g))
                print(channel)
                e=discord.Embed(title=getDJ()+"IS LIVE NOW ", url="http://www.flareradio.net/soon", description="Tune in over at [Flare Radio](http://www.flareradio.net/soon)", color=0xff0404)
                e.set_thumbnail(url="https://images-ext-1.discordapp.net/external/Iwn5QELEcv3bgfPGLzSdwycWikc1B0zyR948lybyf_s/http/flareradio.net/soon/Logo.png")
                e.set_footer(text="FlareBot")
                await channel.send(("@Notified"), embed=e)
        await asyncio.sleep(1)


       
@bot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(bot.user))
    print('------')
    setDJ()
    print("DJ set")
bot.add_cog(Music(bot))
bot.loop.create_task(background_task())
bot.run('NTkzMTcxNTEzNTI4ODExNTIx.XRKEfA.aDM34Xv_9xaQQqoEYkp4dnP8Yb0')
