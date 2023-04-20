from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton)

# start keybords, uzb
start_ru: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
tmp_Menu_ru: KeyboardButton = KeyboardButton("🌹 Меню")
tmp_Location_ru: KeyboardButton = KeyboardButton("✍️ Прокомментировать")
tmp_Settings_ru: KeyboardButton = KeyboardButton("⚙️ Настройки")
start_ru.add(tmp_Menu_ru).add(tmp_Location_ru).insert(tmp_Settings_ru)

#location part
location_ru: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
location_ru.add(
  KeyboardButton(text="📍 Отправить геолокацию", request_location=True))
location_ru.insert(KeyboardButton(text='🗺 Мои адреса'))
location_ru.add(KeyboardButton(text='⬅ Назад назначить время'))

# Menu Keybords
Menu_ru: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
Karobkali_ru: KeyboardButton = KeyboardButton("🥡 Букет в коробке")
Buketli_ru: KeyboardButton = KeyboardButton("💐 Цветы в букете")
Back_for_Menu_ru: KeyboardButton = KeyboardButton('⬅ Назад')
Menu_ru.add(Karobkali_ru).insert(Buketli_ru).add(Back_for_Menu_ru)

# Karobka Keybords
Karobka_ru: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
Back_for_Karobka_ru: KeyboardButton = KeyboardButton('⬅ Назад в меню')
Check_basket_2_ru: KeyboardButton = KeyboardButton('📥 Корзина')
Karobka_ru.add(Check_basket_2_ru).add(Back_for_Karobka_ru)

# Buketli keybords
Buket_ru: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
  [[KeyboardButton('101'), KeyboardButton('201')],
   [KeyboardButton('301'), KeyboardButton('401')],
   [KeyboardButton('501'), KeyboardButton('601')],
   [KeyboardButton('701'), KeyboardButton('1001')],
   [KeyboardButton('📥 Корзина')], [KeyboardButton('⬅ Назад в меню')]],
  resize_keyboard=True)

# Buyurtmalar keybords
Buyurtmalar_ru: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
tmp_Xozir_ru: KeyboardButton = KeyboardButton('📭 Доставка нужна сейчас')
tmp_Vaqt_ru: KeyboardButton = KeyboardButton('⏱ Назначить время доставки')
Back_Buyurtmalar_ru: KeyboardButton = KeyboardButton("⬅ Назад в меню")
Buyurtmalar_ru.add(tmp_Xozir_ru).insert(tmp_Vaqt_ru).add(Back_Buyurtmalar_ru)

# delivery keybords
Keyin_ru: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
Xozir_ru: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
Back_for_Xozir_Keyin_ru: KeyboardButton = KeyboardButton('⬅ Назад')
Xozir_ru.add(KeyboardButton(text='📲 Контакт номер',
                            request_contact=True)).add(Back_for_Xozir_Keyin_ru)
cancel_ru: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True).add(
  KeyboardButton(text='⬅ Назад'))
Contact_ru: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
Contact_ru.add(KeyboardButton(text='📲 Контакт номер',
                              request_contact=True)).add(
                                KeyboardButton(text='⬅ Назад в геолокацию'))

# Each buket keybords
Each_ru: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
Check_basket_ru: KeyboardButton = KeyboardButton('📥 Корзина')
Back_to_buket_ru: KeyboardButton = KeyboardButton('⬅ Вернуться к букетам')
Each_ru.add(Check_basket_ru).add(Back_to_buket_ru)

# location's yes and no
YES_OR_NO_FOR_LOCATION_ru = ReplyKeyboardMarkup(
  keyboard=[[KeyboardButton(text='✅ Да'),
             KeyboardButton(text='❌ Нет')], [KeyboardButton(text='⬅ Назад')]],
  resize_keyboard=True)

# yes or no for style_write
yes_or_no_ru: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
yes_or_no_ru.add(KeyboardButton(text='✅ Да'), KeyboardButton(text='❌ Нет'))

# location's yes of Back
Back_for_Ha_ru: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
Back_for_Ha_ru.add(KeyboardButton(text='⬅ Назад'))

sozlamalar_ru = ReplyKeyboardMarkup(resize_keyboard=True)
sozlamalar_ru.add("Изменить язык")
sozlamalar_ru.add("⬅ Назад")
b_a_c_k_ru: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
  resize_keyboard=True).add(KeyboardButton(text='⬅ Назад'))

change_language_ru = ReplyKeyboardMarkup(keyboard=[[
  KeyboardButton(text='🇷🇺 Русский'),
  KeyboardButton(text='🇺🇿 O\'zbekcha')
], [KeyboardButton(text='⬅ Назад')]],
                                         resize_keyboard=True)

last_agree_ru = ReplyKeyboardMarkup(
  keyboard=[[KeyboardButton(text="✅ Да"),
             KeyboardButton(text="❌ Нет")]],
  resize_keyboard=True)
