import handlers
import asyncio
from aiogram import executor
from dispatcher import dp

from handlers.user_actions import send_message_every_10_sec

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(send_message_every_10_sec())
    executor.start_polling(dp, skip_updates=True)  # Don't skip updates, if your bot will process payments or other important stuff
