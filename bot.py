import os
import sys
import asyncio
import logging
from aiogram.types import Message
from aiogram import Bot, Dispatcher, F
from src.welcome import openai_response


# initialize Dispatcher
dp = Dispatcher()


# create a system message handler
@dp.message(F.new_chat_members)
async def somebody_added(message: Message) -> None:
    # handle empty new_chat_members
    chat_members = message.new_chat_members or []
    for user in chat_members:
        # handle empty username
        username = user.username or user.first_name
        await message.answer(await openai_response(username))


async def main() -> None:
    # initialize Bot instance
    bot = Bot(token=os.environ["BOT_TOKEN"])
    # run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
