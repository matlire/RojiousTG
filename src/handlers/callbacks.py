from main import bot, dp, db, logger

from aiogram.types import CallbackQuery
import string
import random
from yoomoney import Quickpay, Client

from keyboards.reply_keaboards import *
from keyboards.inline_keaboards import *
from messages.messages import *
from states import Form_mine_nick, Form_diss_nick
from handlers.user import *
from config import Config

@dp.callback_query_handler(lambda c: c.data == 'edit_mine_nick')
async def process_callback_edit_mine_nick_handler(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    logger.info(f"INFO: Starting editing minecraft nick on {callback_query.from_user.id}")
    await Form_mine_nick.mine_nick.set()
    await bot.send_message(callback_query.from_user.id, edit_mine_nick, parse_mode="HTML")

@dp.callback_query_handler(lambda c: c.data == 'edit_dis_nick')
async def process_callback_edit_diss_nick_handler(callback_query: CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    logger.info(f"INFO: Starting editing discord nick on {callback_query.from_user.id}")
    await Form_diss_nick.diss_nick.set()
    await bot.send_message(callback_query.from_user.id, edit_diss_nick, parse_mode="HTML")

@dp.callback_query_handler(lambda c: c.data == 'buy_mine')
async def process_callback_buy_mine_handler(callback_query: CallbackQuery):
    logger.info(f"INFO: Started buying minecraft bypass on {callback_query.from_user.id}")
    await bot.answer_callback_query(callback_query.id)

    logger.info(f"INFO: Check & Confirm buying minecraft bypass on {callback_query.from_user.id}")
    season_available = db.check_season_avail(callback_query.from_user.id)
    now_season = db.get_now_season()
    if season_available == now_season: bought = 1
    else: bought = 0

    if bought:
        await bot.send_message(callback_query.from_user.id, succ_pay, parse_mode='html')
        return

    letters_and_digits = string.ascii_lowercase + string.digits
    rand_str = "".join(random.sample(letters_and_digits, 10))
    quick_pay = Quickpay(
        receiver="4100117103211788",
        quickpay_form="shop",
        targets="Rojious проходка",
        paymentType="SB",
        sum=db.get_season_price()[0][0],
        label=rand_str,
    )

    db.update_label(rand_str, callback_query.from_user.id)

    await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id, text=f'{buy_spoiler_msg(db.get_season_descr())} {buy_mine_msg(db.get_season_price())}', parse_mode='html')
    await bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id, reply_markup=gen_buy_mine_kb(quick_pay.redirected_url))

@dp.callback_query_handler(lambda c: c.data == 'chk_buy_mine')
async def process_callback_check_payment_handler(callback_query: CallbackQuery):
    logger.info(f"INFO: Check & Confirm buying minecraft bypass on {callback_query.from_user.id}")
    await bot.answer_callback_query(callback_query.id)

    data = db.get_payment_status(callback_query.from_user.id)
    bought = data[0][0]
    label = data[0][1]

    season_available = db.check_season_avail(callback_query.from_user.id)
    now_season = db.get_now_season()
    if season_available == now_season: bought = 1
    else: bought = 0

    if bought == 0:
        client = Client(Config.access_token)
        history = client.operation_history(label=label)
        try:
            operation = history.operations[-1]
            if operation.status == 'success':
                db.update_payment_status(operation.status, callback_query.message.from_user.id)
                db.update_season_avail(callback_query.from_user.id)
                admins = db.get_admins()
                if admins != []:
                    for i in db.get_admins():
                        await bot.send_message(i[0], buy_data_msg(callback_query.from_user.id, callback_query.from_user.username, callback_query.from_user.full_name, db.get_mine_username(callback_query.from_user.id)[0][0]), parse_mode='html')
                await bot.send_message(callback_query.from_user.id, succ_pay, parse_mode='html')
        except:
            await bot.send_message(callback_query.from_user.id, wait_msg, parse_mode='html')
    else:
        await bot.send_message(callback_query.from_user.id, succ_pay, parse_mode='html')

@dp.callback_query_handler(lambda c: c.data == 'buy_priv')
async def process_callback_buy_priv_handler(callback_query: CallbackQuery):
    logger.info(f"INFO: Started buying private bypass on {callback_query.from_user.id}")
    await bot.answer_callback_query(callback_query.id)
    
    await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id, text=buy_priv_msg, parse_mode='html')
    await bot.edit_message_reply_markup(callback_query.from_user.id, callback_query.message.message_id, reply_markup=buy_priv_kb)

@dp.callback_query_handler(lambda c: c.data == 'buy_buy_priv')
async def process_callback_buy_buy_priv_handler(callback_query: CallbackQuery):
    logger.info(f"INFO: Got private buy message on {callback_query.from_user.id}")
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, buy_priv_msg, parse_mode='html')

@dp.callback_query_handler(lambda c: c.data == 'buy_buy_back')
async def process_callback_buy_back_handler(callback_query: CallbackQuery):
    logger.info(f"INFO: Backed buying on {callback_query.from_user.id}")
    await bot.answer_callback_query(callback_query.id)
    await bot.delete_message(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id)
    await buy(callback_query)
