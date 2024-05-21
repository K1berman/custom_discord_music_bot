from discord.ext import commands
from discord import FFmpegPCMAudio
import discord
from config import PATH_TO_FFMPEG
from functions import get_mp3, get_title
import asyncio
from os import remove,sep


queue = []
queue_prostate = []

async def del_after_play(voice_client, path:str):
    while voice_client.is_playing():
        await asyncio.sleep(1)
    remove(path)


async def play_next_track(ctx):
    if len(queue) > 0:
        next_track = queue.pop(0)
        try:
            audio_source = discord.FFmpegPCMAudio(executable=PATH_TO_FFMPEG, source=f"{next_track}")
            voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
            voice_client.play(audio_source, after=lambda e: asyncio.run_coroutine_threadsafe(play_next_track(ctx), ctx.bot.loop))
            await ctx.channel.send(f"Сейчас играет!\n```{next_track}```")
            await del_after_play(voice_client, f"{next_track}")
        except Exception as e:
            await ctx.channel.send(f"Произошла ошибка при воспроизведении аудио: {e}")
    elif len(queue_prostate) > 0:
        next_track = queue_prostate.pop(0)
        try:
            audio_source = discord.FFmpegPCMAudio(executable=PATH_TO_FFMPEG, source=f"music{sep}prostate{sep}{next_track}.mp3")
            voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
            voice_client.play(audio_source, after=lambda e: asyncio.run_coroutine_threadsafe(play_next_track(ctx), ctx.bot.loop))
            await ctx.channel.send(f"Сейчас играет!\n```{next_track}```")
        except Exception as e:
            await ctx.channel.send(f"Произошла ошибка при воспроизведении аудио: {e}")
    else:
        voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        voice_client.stop()



@commands.command(brief="Воспроизводит аудио из ссылки")
async def play(ctx, url = None):

    if ctx.author.voice is None:
        await ctx.channel.send("Вы должны быть в голосовом канале.")
        return

    link = url

    if link is None:
        await ctx.channel.send("Ссылка не найдена!")
        return

    voice_channel = ctx.author.voice.channel
    if voice_channel is None:
        await ctx.channel.send("Вы должны быть в голосовом канале.")
        return

    voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)

    title = get_title.get_mp3_from_youtube(url=url)
    file_name = f"{title}.mp3"
    if not get_mp3.get_mp3_from_youtube(url=link, full_file_name=file_name):
        await ctx.channel.send(f"Ссылка указана не верно!")
        return


    if voice_client is None:
        voice_client = await voice_channel.connect()
    else:
        await voice_client.move_to(voice_channel)
        if voice_client.is_playing():
            await ctx.channel.send(f"Трек добавлен в очередь!")
            queue.append(title)
            return

    voice_client.stop()

    try:
        audio_source = FFmpegPCMAudio(executable=PATH_TO_FFMPEG, source=file_name)
        await ctx.channel.send(f"Сейчас играет!\n```{title}```")
        voice_client.play(audio_source)
        await del_after_play(voice_client, file_name)

    except Exception as e:
        await ctx.channel.send(f"Произошла ошибка при воспроизведении аудио: {e}")

    if not voice_client.is_playing():
        await play_next_track(ctx)

@commands.command(brief="prostate_list")
async def play_file(ctx):
    if ctx.author.voice is None:
        await ctx.channel.send("Вы должны быть в голосовом канале.")
        return

    data = ctx.message.attachments
    if not data:
        await ctx.channel.send("Файл не прикреплен!")
        return

    voice_channel = ctx.author.voice.channel
    if voice_channel is None:
        await ctx.channel.send("Вы должны быть в голосовом канале.")
        return

    voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    if voice_client is None:
        voice_client = await voice_channel.connect()
    else:
        await voice_client.move_to(voice_channel)


    for attach in data:
        if not attach.filename.endswith(".mp3") and not attach.filename.endswith(".ogg") and not attach.filename.endswith(".wav"):
            await ctx.channel.send(f"Неверный формат файла - {attach.filename}")
            continue

        try:
            file_path = f"{attach.filename}"
            await attach.save(file_path)
            if voice_client.is_playing():
                await ctx.channel.send("Трек добавлен в очередь!")
                queue.append(attach.filename)
                continue
            else:
                audio_source = discord.FFmpegPCMAudio(executable=PATH_TO_FFMPEG, source=file_path)
                await ctx.channel.send(f"Сейчас играет!\n```{attach.filename}```")
                voice_client.play(audio_source)

                await del_after_play(voice_client, file_path)


        except Exception as e:
            await ctx.channel.send(f"Произошла ошибка при воспроизведении аудио: {e}")

    if not voice_client.is_playing():
        await play_next_track(ctx)

@commands.command(brief="Ставит на паузу")
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


@commands.command(brief="Убирает с паузы")
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


@commands.command(brief="Пропускает аудио")
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
    voice_client.stop()


@commands.command(brief="Доступные команды")
async def info(ctx):
    info = "```Доступные команды:\n\t!play (url) - воспроизводит музыку с видео\n\t!play_file + прикрепленный трек - воспроизводит файл\n\t!skip - пропускает трек\n\t!pause - ставит на паузу трек\n\t!resume - снимает с паузы\n\t!prostate (track_id | random) - песни легендарного Dj Prostate!\n\t!prostate_list - список песен легендарного Dj Prostate!\
    \n\t!add_prostate + прикрепленный трек mp3 формата - добавляет файл в !prostate_list\n\t!del_prostate (track_id) - удаляет трек по id из !prostate_list\n\t!info - список команд```"
    await ctx.channel.send(info)