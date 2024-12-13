from math import e
import discord
from discord.ext import commands
import os
import asyncio
import yt_dlp
import random 
from dotenv import load_dotenv
import urllib.parse, urllib.request, re

# Ajuste para a variável ffmpeg_options (remover a duplicação)
ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn -filter:a "volume=0.25"',
    'executable': r'C:\ffmpeg\bin\ffmpeg.exe'  # Caminho completo para o FFmpeg
}

def run_bot():
    load_dotenv()
    TOKEN = os.getenv('discord_token')
    intents = discord.Intents.default()
    intents.message_content = True
    client = commands.Bot(command_prefix=["zeros ", "z "], intents=intents)

    queues = {}
    voice_clients = {}
    youtube_base_url = 'https://www.youtube.com/'
    youtube_results_url = youtube_base_url + 'results?'
    youtube_watch_url = youtube_base_url + 'watch?v='
    yt_dl_options = {"format": "bestaudio/best"}
    ytdl = yt_dlp.YoutubeDL(yt_dl_options)

    @client.event
    async def on_ready():
        print(f'{client.user} está pronto para tocar músicas!')

    async def play_next(ctx):
        if queues[ctx.guild.id] != []:
            link = queues[ctx.guild.id].pop(0)
            await play(ctx, link=link)

    @client.command(name="play")
    async def play(ctx, *, link):
        try:
            if ctx.voice_client is None:
                voice_client = await ctx.author.voice.channel.connect()
                voice_clients[voice_client.guild.id] = voice_client
            else:
                voice_client = ctx.voice_client

            # Criação da fila caso não exista
            if ctx.guild.id not in queues:
                queues[ctx.guild.id] = []

            # Verifica se a música não está tocando, caso contrário adiciona à fila
            if not voice_client.is_playing():
                if youtube_base_url not in link:
                    query_string = urllib.parse.urlencode({'search_query': link})
                    content = urllib.request.urlopen(youtube_results_url + query_string)
                    search_results = re.findall(r'/watch\?v=(.{11})', content.read().decode())
                    link = youtube_watch_url + search_results[0]

                loop = asyncio.get_event_loop()
                data = await loop.run_in_executor(None, lambda: ytdl.extract_info(link, download=False))

                song_url = data['url']
                song_title = data['title']
                song_duration = data['duration']  # Tempo total em segundos
                song_thumbnail = data['thumbnail']  # URL da miniatura (banner)

                # Criar embed para enviar a miniatura e as informações da música
                embed = discord.Embed(
                    title="Agora tocando",
                    description=song_title,
                    color=discord.Color.blue()
                )
                embed.set_thumbnail(url=song_thumbnail)
                embed.add_field(name="Duração", value=f"{song_duration // 60}:{song_duration % 60:02d}", inline=False)
                await ctx.send(embed=embed)

                # Passando o caminho do FFmpeg corretamente nas opções
                player = discord.FFmpegOpusAudio(song_url, **ffmpeg_options)
                voice_clients[ctx.guild.id].play(player, after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx), client.loop))

            else:
                # Se a música já está tocando, adiciona à fila
                song_title = await add_to_queue(ctx, link)
                await ctx.send(f"A música '{song_title}' foi adicionada à fila, posição {len(queues[ctx.guild.id])}.")

        except Exception as e:
            print(e)

    async def add_to_queue(ctx, link):
        # Adiciona a música à fila
        query_string = urllib.parse.urlencode({'search_query': link})
        content = urllib.request.urlopen(youtube_results_url + query_string)
        search_results = re.findall(r'/watch\?v=(.{11})', content.read().decode())
        link = youtube_watch_url + search_results[0]

        loop = asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(link, download=False))

        song_title = data['title']
        queues[ctx.guild.id].append(link)
        return song_title

    @client.command(name="clear_queue")
    async def clear(ctx):
        try:
            queues[ctx.guild.id].clear()
            await ctx.send("Fila limpa!")
        except Exception as e:
            await ctx.send("Não há nada na fila para limpar.")

    @client.command(name="pause")
    async def pause(ctx):
        try:
            voice_clients[ctx.guild.id].pause()
        except Exception as e:
            print(e)

    @client.command(name="resume")
    async def resume(ctx):
        try:
            voice_clients[ctx.guild.id].resume()
        except Exception as e:
            print(e)

    @client.command(name="stop")
    async def stop(ctx):
        try:
            voice_clients[ctx.guild.id].stop()
            await voice_clients[ctx.guild.id].disconnect()
            del voice_clients[ctx.guild.id]
        except Exception as e:
            print(e)

    @client.command(name="fila")
    async def fila(ctx):
        try:
            queue_list = "\n".join(queues[ctx.guild.id])
            await ctx.send(f"Fila atual:\n{queue_list}")
        except Exception as e:
            await ctx.send("A fila está vazia.")
            
    client.run(TOKEN)
