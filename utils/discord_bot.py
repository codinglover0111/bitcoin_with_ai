import asyncio
import os
import threading
import discord
from dotenv import load_dotenv
from discord.ext import commands

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path)

class DiscordBot:
    def __init__(self, loop):
        self.loop = loop  # 이벤트 루프를 저장합니다.
        intents = discord.Intents.all()
        # bot 생성 시 loop를 지정 (discord.py의 버전에 따라 loop 인자 사용 여부가 달라질 수 있음)
        self.bot = commands.Bot(command_prefix='!', intents=intents)
        self.bot.event(self.on_ready)
    
    async def on_ready(self):
        print(f'{self.bot.user.name}으로 로그인했습니다.')
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                if channel.permissions_for(guild.me).send_messages:
                    await channel.send('안녕하세요! 제가 입장했습니다.')
                    break

    async def _send_message_async(self, message: str):
        """비동기로 메시지를 보내는 내부 함수"""
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                if channel.permissions_for(guild.me).send_messages:
                    await channel.send(message)
                    return  # 한 채널에만 전송

    def send_message(self, message: str):
        """
        동기 코드에서도 호출할 수 있도록, 이벤트 루프에 비동기 작업을 등록합니다.
        """
        # _send_message_async 코루틴을 현재 저장된 이벤트 루프에 안전하게 제출합니다.
        asyncio.run_coroutine_threadsafe(self._send_message_async(message), self.loop)

def start_bot(loop, bot_instance, token):
    """봇을 실행하는 코루틴을 이벤트 루프에서 실행"""
    asyncio.set_event_loop(loop)
    loop.run_until_complete(bot_instance.bot.start(token))

if __name__ == "__main__":
    token = os.getenv('DISCORD_TOKEN')
    
    # 별도의 이벤트 루프를 생성합니다.
    loop = asyncio.new_event_loop()
    
    # DiscordBot 인스턴스 생성 시 이벤트 루프를 전달합니다.
    bot_instance = DiscordBot(loop)
    
    # 봇을 별도의 스레드에서 실행합니다.
    bot_thread = threading.Thread(target=start_bot, args=(loop, bot_instance, token), daemon=True)
    bot_thread.start()
    
    # 레거시 동기 코드에서 send_message를 호출하는 예시
    import time
    time.sleep(5)  # 봇이 완전히 시작될 때까지 잠시 대기
    
    # 동기 코드에서 메시지 전송
    bot_instance.send_message("테스트 메시지입니다.")
    
    try:
        bot_thread.join()
    except KeyboardInterrupt:
        print("종료 중...")
        for task in asyncio.all_tasks(loop):
            task.cancel()
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
        print("종료 완료")

