from discord import FFmpegPCMAudio
from config import PATH_TO_FFMPEG
from discord.ext import commands
import asyncio
import discord
from random import randint
from os import sep

track_list = {"1": "Александр Пупукин - Пиписька Негра",
              "2": "Brazil Pupuki - Pipiska Negra(extended)",
              "3": "Medieval Puki - King of the puki",
              "4": "Chinese Ballads - Vlad's story",
              "5": "Mary Dick - Pipiska Negra(soul)",
              "6": "DJ Prostate - Puki Pupuki"
              }

@commands.command(brief="Воспроизводит аудио из !prostate_list")
async def prostate(ctx, id, mode = None):

    if id == "random":
        id = str(randint(1, len(track_list)))

    try:
        id = int(id)

    except ValueError:
        await ctx.channel.send("Неверно указан id, используй !prostate_list")
        return

    if (int(id) < 1 or int(id) > len(track_list)):
        await ctx.channel.send("Неверно указан id, используй !prostate_list")
        return

    id = str(id)

    if mode == "nonestop":
        pass

    voice_channel = ctx.author.voice.channel
    if voice_channel is None:
        await ctx.channel.send("Вы должны быть в голосовом канале.")
        return

    voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)

    if voice_client is None:
        voice_client = await voice_channel.connect()
    else:
        await voice_client.move_to(voice_channel)
        if voice_client.is_playing():
            await ctx.channel.send(f"Трек добавлен в очередь!")
            while voice_client.is_playing():
                await asyncio.sleep(1)

    voice_client.stop()

    try:
        audio_source = FFmpegPCMAudio(executable=PATH_TO_FFMPEG, source=f"music{sep}prostate{sep}{track_list.get(id)}.mp3")
        await ctx.channel.send(f"Сейчас играет!\n```{track_list.get(id)}```")
        voice_client.play(audio_source)

    except Exception as e:
        await ctx.channel.send(f"Произошла ошибка при воспроизведении аудио: {e}")\


@commands.command(brief="Воспроизводит аудио из !prostate_list")
async def prostate_list(ctx):
    list = []
    for i in range(1, len(track_list)+ 1):
        data = f"{i} - {track_list.get(str(i))}"
        list.append(data)
    prostate_list = "\n".join(list)
    await ctx.channel.send(f"```{prostate_list}```")