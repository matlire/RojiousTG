"""
Commands & messages handler script
"""
from aiogram.types import Message
from aiogram.dispatcher.filters import Command, Text
import asyncio

from main import bot, dp, db, logger

from keyboards.reply_keaboards import *
from keyboards.inline_keaboards import *
from messages.messages import *
import shutil
import os

@dp.message_handler(Command('start'))
async def start_message(message: Message):
    logger.info(f"INFO: Got /start {message.from_user.id}")
    if db.check_if_user_in_db(message.from_user.id) == 0:
        db.add_user(message.from_user.id, message.from_user.full_name, message.from_user.username)
    
    await bot.send_message(message.chat.id, start_msg(message.from_user.full_name), reply_markup=main_kb_markup, parse_mode="HTML")

@dp.message_handler(Command('kill'))
async def kill_message(message: Message):
    logger.info(f"INFO: Got backup from {message.from_user.id}")
    admins = db.get_admins()
    if admins != []:
        if message.from_user.id in admins[0]:
            logger.info("INFO: Stopping bot...")
            await backup_message(message)
            await bot.session.close()
            dp.stop_polling()
            quit()


@dp.message_handler(Command('backup'))
async def backup_message(message: Message):
    logger.info(f"INFO: Got backup from {message.from_user.id}")
    admins = db.get_admins()
    if admins != []:
        if message.from_user.id in admins[0]:
            try:
                shutil.copyfile("db.db", "db-backup.db")
                await bot.send_document(message.from_user.id, open("db-backup.db", 'rb'))
                os.remove("db-backup.db")
            except: pass
            
            try:
                shutil.copyfile("log.log", "log-backup.log")
                await bot.send_document(message.from_user.id, open("log-backup.log", 'rb'))
                os.remove("log-backup.log")
            except: pass

            try:
                shutil.copyfile("log_sql.log", "log_sql-backup.log")
                await bot.send_document(message.from_user.id, open("log_sql-backup.log", 'rb'))
                os.remove("log_sql-backup.log")
            except: pass

@dp.message_handler(content_types=['document'])
async def update_db(message: Message):
    logger.info(f"INFO: Got new db from {message.from_user.id}")
    admins = db.get_admins()
    if admins != []:
        if message.from_user.id in admins[0]:
            if message.document.file_name == "db.db":
                await message.document.download(destination_file="db.db")

@dp.message_handler(regexp=r"^[*]")
async def update_db(message: Message):
    logger.info(f"INFO: Broadcast from {message.from_user.id}")
    admins = db.get_admins()
    if admins != []:
        if message.from_user.id in admins[0]:
            txt = message.text[1:]
            for i in range(0, len(db.get_ids_num())):
                await bot.send_message(db.get_id(i+1), txt, parse_mode="HTML")

@dp.message_handler(Text(equals='🔍 Узнать ТГ id', ignore_case=True))
async def show_id(message: Message):
    logger.info(f"INFO: Check tg_id from {message.from_user.id}")
    await bot.send_message(message.from_user.id, message.from_user.id, parse_mode="HTML")

@dp.message_handler(Text(equals='📕 Правила', ignore_case=True))
async def show_rules(message: Message):
    logger.info(f"INFO: Got rules from {message.from_user.id}")
    await bot.send_message(message.from_user.id, rules_msg, parse_mode="HTML")

@dp.message_handler(Text(equals='ℹ Информация', ignore_case=True))
async def show_info(message: Message):
    logger.info(f"INFO: For info from {message.from_user.id}")
    await bot.send_message(message.from_user.id, about_msg, parse_mode="HTML")

@dp.message_handler(Text(equals='👤 Личный Кабинет', ignore_case=True))
async def show_acc(message: Message):
    logger.info(f"INFO: Got my account from {message.from_user.id}")
    now_user_tg_id = message.from_user.id
    db.update_tg_id(now_user_tg_id, message.from_user.username)

    minecraft_username = db.get_mine_username(now_user_tg_id)
    if minecraft_username != [(None,)]: minecraft_username = minecraft_username[0][0]
    else: minecraft_username = "Вы ещё не добавили"

    discord_username = db.discord_username(now_user_tg_id)
    if discord_username != [(None,)]: discord_username = discord_username[0][0]
    else: discord_username = "Вы ещё не добавили"

    season_available = db.check_season_avail(now_user_tg_id)
    now_season = db.get_now_season()
    if season_available == now_season: season_available = 1
    else: season_available = 0

    private_available = db.check_priv_avail(now_user_tg_id)

    if private_available == now_season: private_available = 1
    else: private_available = 0

    is_admin = db.check_admin(now_user_tg_id)
    if is_admin == [(0,)]: is_admin = 0
    else: is_admin = 1

    user_db_tg_id = db.get_tg_id_by_username(message.from_user.username)
    await bot.send_message(now_user_tg_id, acc_msg(minecraft_username, discord_username, season_available, private_available, now_user_tg_id, user_db_tg_id[0][0], is_admin),reply_markup=acc_kb, parse_mode="HTML")    

@dp.message_handler(Text(equals='😎 Купить', ignore_case=True))
async def buy(message: Message):
    logger.info(f"INFO: Got buy from {message.from_user.id}")
    await bot.send_message(message.from_user.id, buy_msg, reply_markup=buy_kb, parse_mode="HTML")
