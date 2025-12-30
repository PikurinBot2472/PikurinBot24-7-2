from keep_alive import keep_alive
import discord
import asyncio
import logging

audio_url = "https://www.dropbox.com/scl/fi/ggkumfroq21oua2rjs8hu/2025-2026-J-POP-26-J-ROCK-bgm-djmix-bgm.mp3?rlkey=pom06f67ozsz05s24nllxqgss&st=rqsgeq4c&dl=1"
TOKEN = 'MTI3NzE0Mjc5MjA3MzY0MjEwNA.GWEbX9.OZHmiEtul19btoFd6s7CqIqwclkYogrl-ZNSzw'

channel_id = 1277188290121961586

intents = discord.Intents.all()
intents.typing = False
client = discord.Client(intents=intents)

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


async def ensure_voice(channel):
    vc = channel.guild.voice_client

    if vc is None:
        await channel.connect(self_deaf=True)
        return

    if not vc.is_connected():
        await vc.disconnect(force=True)
        await channel.connect(self_deaf=True)


async def play_loop(channel):
    while True:
        try:
            await ensure_voice(channel)
            vc = channel.guild.voice_client

            # VCがまだ無い・切断中なら待つ
            if vc is None or not vc.is_connected():
                await asyncio.sleep(2)
                continue

            # 再生中なら待機
            if vc.is_playing():
                await asyncio.sleep(5)
                continue

            source = discord.FFmpegPCMAudio(
                audio_url,
                before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
            )

            vc.play(source)

            # 再生終了まで待つ
            while vc.is_playing():
                await asyncio.sleep(1)

        except Exception as e:
            log.exception("play_loop error")
            await asyncio.sleep(5)  # 落ち着かせて再試行


@client.event
async def on_ready():
    print('ログインしました')
    await client.change_presence(
        activity=discord.Game(name='Pikurinサーバー専用BOT')
    )

    channel = client.get_channel(channel_id)
    client.loop.create_task(play_loop(channel))


keep_alive()
client.run(TOKEN)
