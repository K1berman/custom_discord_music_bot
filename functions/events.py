from .comands_main import guild_nonestop_status, guild_queue
timers = {}

async def is_empty_channel(member, before, after):
    voice_state = member.guild.voice_client
    if not member.bot:
        if voice_state:
            if after.channel is None:
                if len(voice_state.channel.members) == 1:
                    guild_nonestop_status[member.guild.id] = "stop"
                    guild_queue[member.guild.id] = None
                    if voice_state.is_playing():
                        await voice_state.stop()
                    await voice_state.disconnect()
    else:
        if before.channel is not None and after.channel is None:
            guild_nonestop_status[member.guild.id] = "stop"
            guild_queue[member.guild.id] = None
            if voice_state.is_playing():
                await voice_state.stop()
            await voice_state.disconnect()




