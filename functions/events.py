import asyncio
from .comands_main import guild_nonestop_status, skip
timers = {}

async def is_empty_channel(ctx, member, before, after):
    if not member.bot:
        voice_state = member.guild.voice_client
        if voice_state:
            if after.channel is None:
                if len(voice_state.channel.members) == 1:
                    await skip(ctx)
                    await voice_state.disconnect()




