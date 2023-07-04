"""
Reply keyboards
"""
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button_rent = KeyboardButton('😎 Купить')
button_cab = KeyboardButton('👤 Личный Кабинет')
button_info = KeyboardButton('ℹ Информация')
button_rules = KeyboardButton('📕 Правила')
button_id = KeyboardButton('🔍 Узнать ТГ id')

main_kb_markup = ReplyKeyboardMarkup(resize_keyboard=True)
main_kb_markup.add(button_rent)
main_kb_markup.row(button_cab, button_info)
main_kb_markup.row(button_rules, button_id)
