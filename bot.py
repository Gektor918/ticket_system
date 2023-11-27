import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from services_bot import *

bot = Bot("Your token", parse_mode=ParseMode.HTML)
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f"Привет, терперь ты можешь создать тикет!")


@dp.message()
async def create_ticket_dp(message: types.Message) -> None:
    """
    Create ticket
    """
    try:
        resp_data = await parse_data(message)
        ticket = await filter_tickets(resp_data)
        rezult = await create_ticket(ticket, resp_data)
        if rezult:
            await message.answer('Тикет успешно создан.')
        else:
            await message.answer('У вас уже есть открытый тикет.')
    except TypeError:
        await message.answer("Nice try!")


async def main() -> None:
    await dp.start_polling(bot)


async def message(chat_id: int, text: str) -> types.Message:
    try:
        message = await bot.send_message(chat_id, text)
        return message
    except Exception as e:
        error_message = f"Failed to send message: {e}"
        return {"error_message": error_message}


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())