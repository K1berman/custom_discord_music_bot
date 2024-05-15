from discord.ext import commands
from discord import FFmpegPCMAudio
import discord
from config import PATH_TO_FFMPEG
from functions import get_mp3, get_title
import time
import asyncio


@commands.command(brief="Воспроизводит аудио из ссылки")
async def play(ctx, url):
    link = url
    if link is None:
        await ctx.channel.send("Ссылка не найдена!")
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
        if voice_client.is_playing():
            await ctx.channel.send(f"Трек добавлен в очередь!")
            while voice_client.is_playing():
                await asyncio.sleep(1)

    voice_client.stop()

    if not get_mp3.get_mp3_from_youtube(url=link):
        await ctx.channel.send(f"Ссылка указана не верно!")
        return

    time.sleep(2)

    title = get_title.get_mp3_from_youtube(url)
    try:
        audio_source = FFmpegPCMAudio(executable=PATH_TO_FFMPEG, source="exit.mp3")
        await ctx.channel.send(f"Сейчас играет!\n```{title}```")
        voice_client.play(audio_source)

    except Exception as e:
        await ctx.channel.send(f"Произошла ошибка при воспроизведении аудио: {e}")


@commands.command(brief="Ставит на паузу")
async def pause(ctx):
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
    info = "```Доступные команды:\n\t!play (url) - воспроизводит музыку с видео\n\t!skip - пропускает трек\n\t!pause - ставит на паузу трек\n\t!resume - снимает с паузы\n\t!info - список команд\n\t!prostate (track_id | random) - песни легендарного Dj Prostate!\n\t!prostate_list - список песен легендарного Dj Prostate!```"
    await ctx.channel.send(info)