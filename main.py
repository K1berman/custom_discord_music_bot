from discord.ext import commands
import discord
from config import DISCORD_TOKEN
from functions import comands_main, comands_prostate, events


intents = discord.Intents.all()
intents.messages = True
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_voice_state_update(member, before, after):
    await events.is_empty_channel(member, before, after)


bot.add_command(comands_main.play)
bot.add_command(comands_main.skip)
bot.add_command(comands_main.pause)
bot.add_command(comands_main.resume)
bot.add_command(comands_main.info)
bot.add_command(comands_prostate.prostate)
bot.add_command(comands_prostate.prostate_list)
bot.add_command(comands_prostate.add_prostate)
bot.add_command(comands_prostate.del_prostate)
bot.add_command(comands_main.play_file)


bot.run(token=DISCORD_TOKEN)

