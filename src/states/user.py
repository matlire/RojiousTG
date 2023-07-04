"""
States script
"""
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message
from handlers.user import *

from main import bot, dp, db, logger

# States for changing minecraft and discord nicknames
class Form_mine_nick(StatesGroup):
    mine_nick = State()

class Form_diss_nick(StatesGroup):
    diss_nick = State()

# Cancel handler
@dp.message_handler(state='*', commands='отмена')
@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.reply('Отменено')
    await show_acc(message)
    logger.info(f"INFO: {message.from_user.id}/{message.from_user.full_name} - Canceled changing minecraft nick")

# Change minecraft nickname handler
@dp.message_handler(state=Form_mine_nick.mine_nick)
async def process_edit_mine_nick(message: Message, state: FSMContext):
    db.update_mine_nick(message.text, message.from_user.id)
    await state.finish()
    await bot.send_message(message.from_user.id, edit_nick_suc, parse_mode="HTML")
    await show_acc(message)
    logger.info(f"INFO: {message.from_user.id}/{message.from_user.full_name} - Minecraft nick updated")

# Change discord nickname handler
@dp.message_handler(state=Form_diss_nick.diss_nick)
async def process_edit_diss_nick(message: Message, state: FSMContext):
    db.update_diss_nick(message.text, message.from_user.id)
    await state.finish()
    await bot.send_message(message.from_user.id, edit_nick_suc, parse_mode="HTML")
    await show_acc(message)
    logger.info(f"INFO: {message.from_user.id}/{message.from_user.full_name} - Discord nick updated")