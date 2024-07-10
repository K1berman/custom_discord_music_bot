from discord.ext import commands
from discord import FFmpegPCMAudio
import discord
from config import PATH_TO_FFMPEG
from functions import get_mp3, get_title, finder
import asyncio
from os import remove,sep
import re
import datetime

guild_queue = {}
guild_nonestop_status = {}

def is_connected_to_channel(ctx) -> bool:

    if ctx.author.voice is None:
        return False

    if ctx.author.voice.channel is None:
        return False

    return True

async def del_after_play(voice_client, path:str):
    while voice_client.is_playing():
        await asyncio.sleep(1)
    remove(path)


async def play_next_track(ctx):
    if guild_queue.get(ctx.guild.id) and len(guild_queue.get(ctx.guild.id)) > 0:
        next_track = guild_queue.get(ctx.guild.id).pop(0)
        await play_audio(ctx, next_track)
    else:
        voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        voice_client.stop()


async def player(ctx, voice_client: str, file_name: str):
    try:
        audio_source = FFmpegPCMAudio(executable=PATH_TO_FFMPEG, source=file_name)
        voice_client.play(audio_source)

    except Exception as e:
        await ctx.channel.send(f"Произошла ошибка при воспроизведении аудио: {e}")


async def play_audio(ctx, file_name: str, nonestop: str = None) -> None:

    voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)

    if voice_client is None:
        voice_client = await ctx.author.voice.channel.connect()
    else:
        await voice_client.move_to(ctx.author.voice.channel)
        if voice_client.is_playing():
            await ctx.channel.send(f"Трек добавлен в очередь!")

            if not guild_queue.get(ctx.guild.id):
                guild_queue[ctx.guild.id] = []

            guild_queue.get(ctx.guild.id).append(file_name)

            return

    voice_client.stop()

    await ctx.channel.send(f"Сейчас играет!\n```{file_name[5:-4]}\n```")

    if nonestop == "nonestop":
        while guild_nonestop_status.get(ctx.guild.id) == "play":
            await player(ctx, voice_client, file_name)
            while voice_client.is_playing():
                await asyncio.sleep(1)
    else:
        await player(ctx, voice_client, file_name)

    await del_after_play(voice_client, file_name)

    if not voice_client.is_playing():
        await play_next_track(ctx)



@commands.command(brief="Воспроизводит аудио из ссылки")
async def play(ctx, *args):

    input_data: list = list(args)
    nonestop: str = None

    guild_nonestop_status[ctx.guild.id] = "play"

    if not is_connected_to_channel(ctx):
        await ctx.channel.send("Вы должны быть в голосовом канале.")
        return

    if "nonestop" in input_data:
        nonestop = "nonestop"
        input_data.remove("nonestop")

    files = ctx.message.attachments

    url = " ".join(input_data)


    if files:
        for attach in files:
            if not attach.filename.endswith((".mp3", ".ogg", ".wav", ".mp4")):
                await ctx.channel.send(f"Неверный формат файла - {attach.filename}")
                return

            file_name: str = attach.filename

            if file_name.endswith(".mp4"):
                file_name.replace(".mp4", ".mp3")

            file_name = f"%s%s" % (datetime.datetime.now().strftime("%M_%S"), file_name)
            print(file_name)
            await attach.save(file_name)
            break

    elif url:
        if "https://www.youtube.com/watch?v=" in url:
            pass
        else:
            url = finder.get_link_by_trackname(url)

        title = get_title.get_mp3_from_youtube(url=url)
        print(title)
        file_name = f"{datetime.datetime.now().strftime("%M_%S")}{title}.mp3"
        print(url)
        if not get_mp3.get_mp3_from_youtube(url=url, full_file_name=file_name):
            await ctx.channel.send(f"Трек не найден!")
            return

    else:
        await ctx.channel.send(f"Укажите ссылку или прикрепите файл!")
        return

    await play_audio(ctx, file_name, nonestop)


@commands.command(brief="Воспроизводит приклепленный файл")
async def play_file(ctx):
    await ctx.channel.send(f"Теперь !play так же работает с файлами")
    await play(ctx)


@commands.command(brief="Ставит трек на паузу")
async def pause(ctx):

    if ctx.author.voice is None:
        await ctx.channel.send("Вы должны быть в голосовом канале.")
        return

    voice_channel = ctx.author.voice.channel
    if voice_channel is None:
        await ctx.channel.send("Вы должны быть в голосовом канале, чтобы управлять ботом!")
        return

    voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    if voice_client is None:
        await ctx.channel.send("Бот ничего не воспроизводит!")
        return

    if not voice_client.is_playing():
        await ctx.channel.send("Бот ничего не воспроизводит!")
        return

    voice_client.pause()


@commands.command(brief="Убирает трек с паузы")
async def resume(ctx):
    voice_channel = ctx.author.voice.channel
    if voice_channel is None:
        await ctx.channel.send("Вы должны быть в голосовом канале, чтобы управлять ботом!")
        return

    voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    if voice_client is None:
        await ctx.channel.send("Бот ничего не воспроизводит!")
        return

    if voice_client.is_playing():
        await ctx.channel.send("Бот уже воспроизводит аудио!")
        return

    voice_client.resume()


@commands.command(brief="Пропускает трек")
async def skip(ctx):
    voice_channel = ctx.author.voice.channel
    if voice_channel is None:
        await ctx.channel.send("Вы должны быть в голосовом канале, чтобы управлять ботом!")
        return

    voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    if voice_client is None:
        await ctx.channel.send("Бот ничего не воспроизводит!")
        return

    if not voice_client.is_playing():
        await ctx.channel.send("Бот ничего не воспроизводит!")
        return

    await ctx.channel.send("Пропускаю трек!")
    guild_nonestop_status[ctx.guild.id] = "stop"
    voice_client.stop()


@commands.command(brief="Доступные команды")
async def info(ctx):
    info = "```Доступные команды:\n\t!play (url) - воспроизводит музыку с видео\n\t!play_file + прикрепленный трек - воспроизводит файл\n\t!skip - пропускает трек\n\t!pause - ставит на паузу трек\n\t!resume - снимает с паузы\n\t!prostate (track_id | random) - песни легендарного Dj Prostate!\n\t!prostate_list - список песен легендарного Dj Prostate!\
    \n\t!add_prostate + прикрепленный трек mp3 формата - добавляет файл в !prostate_list\n\t!del_prostate (track_id) - удаляет трек по id из !prostate_list\n\t!info - список команд```"
    await ctx.channel.send(info)