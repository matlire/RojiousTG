from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

acc_kb = InlineKeyboardMarkup().row(InlineKeyboardButton(text="ИЗМЕНИТЬ МАИНКРАФТ НИК 🎲", callback_data="edit_mine_nick")).row(InlineKeyboardButton(text="ИЗМЕНИТЬ ДИСКОРД НИК 🗣", callback_data="edit_dis_nick"))

buy_kb = InlineKeyboardMarkup().row(InlineKeyboardButton(text="МАИНКРАФТ 🏆", callback_data="buy_mine"), InlineKeyboardButton(text="ОБСУЖДЕНИЕ 📧", callback_data="buy_priv"))

def gen_buy_mine_kb(url_):
    buy_mine_kb = InlineKeyboardMarkup().row(InlineKeyboardButton(text="КУПИТЬ 💲", url=url_, callback_data="buy_buy_mine"), InlineKeyboardButton(text="НАЗАД 😐", callback_data="buy_buy_back"))
    buy_mine_kb.add(InlineKeyboardButton(text="Проверить оплату ✔", callback_data="chk_buy_mine"))
    return buy_mine_kb

buy_priv_kb = InlineKeyboardMarkup().row(InlineKeyboardButton(text="НАЗАД 😐", callback_data="buy_buy_back"))
