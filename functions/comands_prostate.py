import random

from discord import FFmpegPCMAudio
from config import PATH_TO_FFMPEG
from discord.ext import commands
import asyncio
import discord
from random import randint
from os import sep,listdir,remove
from .comands_main import is_connected_to_channel, guild_nonestop_status, play_audio

def get_prostate_list():
    pupuki_list = {}
    files = listdir(f"music{sep}prostate{sep}")
    id = 1
    for file in files:
        pupuki_list[str(id)] = file
        id += 1
    return pupuki_list


@commands.command(brief="Воспроизводит аудио из !prostate_list")
async def prostate(ctx, *args):

    track_list = get_prostate_list()

    input_data: list = list(args)
    nonestop: str = None

    guild_nonestop_status[ctx.guild.id] = "play"

    if not is_connected_to_channel(ctx):
        await ctx.channel.send("Вы должны быть в голосовом канале.")
        return

    if "nonestop" in input_data:
        nonestop = "nonestop"
        input_data.remove("nonestop")

    if "random" in input_data:
        url = str(randint(1, len(track_list)))
        input_data.remove("random")
    else:
        url = " ".join(input_data)

    try:
        id = int(url)

    except ValueError:
        await ctx.channel.send("Неверно указан id, используй !prostate_list")
        return

    if (int(id) < 1 or int(id) > len(track_list)):
        await ctx.channel.send("Неверно указан id, используй !prostate_list")
        return

    id = str(id)

    voice_channel = ctx.author.voice.channel
    if voice_channel is None:
        await ctx.channel.send("Вы должны быть в голосовом канале.")
        return

    file_name = f"music{sep}prostate{sep}{track_list.get(id)}"

    await play_audio(ctx, file_name, nonestop)

@commands.command(brief="prostate_list")
async def prostate_list(ctx):
    track_list = get_prostate_list()
    list = []
    for i in range(1, len(track_list)+ 1):
        data = f"{i} - {track_list.get(str(i))}"
        list.append(data)
    prostate_list = "\n".join(list)
    await ctx.channel.send(f"```{prostate_list}```")


@commands.command(brief="prostate_list")
async def add_prostate(ctx):

    data = ctx.message.attachments
    if not data:
        await ctx.channel.send(f"Файл не прикреплен!")
        return

    for attach in data:
        if not ".mp3" in attach.filename:
            await ctx.channel.send(f"Неверный формат файла - {attach.filename}")
            continue
        await attach.save(f"music{sep}prostate{sep}{attach.filename}")
        await ctx.channel.send(f"Добавлен файл - {attach}\nid треков поменялись!")


@commands.command(brief="prostate_list")
async def del_prostate(ctx, id = None):
    if id is None:
        await ctx.channel.send("Неверно указан id, используй !prostate_list")
        return

    track_list = get_prostate_list()

    if (int(id) < 1 or int(id) > len(track_list)):
        await ctx.channel.send("Неверно указан id, используй !prostate_list")
        return

    file = f"{track_list.get(id)}.mp3"
    remove(f"music{sep}prostate{sep}{file}")
    await ctx.channel.send("Трек удален!")


@commands.command(brief="prostate_list")
async def gun(ctx):
    lenth = random.randint(0, 22)
    await ctx.channel.send(f"У {ctx.author.mention} ствол {lenth} см")
    return


