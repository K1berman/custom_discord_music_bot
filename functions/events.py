import asyncio

timers = {}

async def is_empty_channel(member, before, after):
    if not member.bot:
        voice_state = member.guild.voice_client
        if voice_state:
            if after.channel is None:
                if len(voice_state.channel.members) == 1:
                    await voice_state.disconnect()



