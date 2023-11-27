from aiogram import types

from model import *


db = DatabaseManager()


async def parse_data(message: types.Message) -> tuple:
    """
    Parse data message
    """
    user_name = str(message.from_user.first_name)
    chat_id = int(message.chat.id)
    message_text = str(message.text)

    all_info = (chat_id, user_name, message_text)
    return all_info


async def filter_tickets(all_info: tuple) -> asyncpg.Record:
    """
    Filter tickets to existing
    """
    async with db:
        ticket = await db.filter_in_ticket(all_info[0])
    return ticket


async def create_ticket(ticket: asyncpg.Record, all_info: tuple) -> bool:
    """
    Сreate ticket
    """
    if ticket == []:
        async with db:
            await db.create_ticket(all_info[0], all_info[1], all_info[2])
        return True
    else:
        return False