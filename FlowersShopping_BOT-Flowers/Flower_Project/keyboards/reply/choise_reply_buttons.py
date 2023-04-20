from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton)
from keyboards.reply.russian_choise_reply_buttons import (
  start_ru, Menu_ru, Karobka_ru, Buket_ru, Buyurtmalar_ru, Xozir_ru, Keyin_ru,
  location_ru, YES_OR_NO_FOR_LOCATION_ru, cancel_ru, Contact_ru, sozlamalar_ru,
  change_language_ru, yes_or_no_ru, Back_for_Ha_ru, Each_ru, b_a_c_k_ru,
  last_agree_ru)

# start keybords, uzb
start: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
tmp_Menu: KeyboardButton = KeyboardButton("🌹 Menyu")
tmp_Location: KeyboardButton = KeyboardButton("✍️ Fikr Bildirish")
tmp_Settings: KeyboardButton = KeyboardButton("⚙️ Sozlamalar")
start.add(tmp_Menu).add(tmp_Location).insert(tmp_Settings)

#location part
location: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
location.add(
  KeyboardButton(text="📍 Geolokatsiyani yuboring", request_location=True))
location.insert(KeyboardButton(text='🗺 Mening manzillarim'))
location.add(KeyboardButton(text='⬅ Ortga vaqtni belgilashga'))

# Menu Keybords
Menu: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
Karobkali: KeyboardButton = KeyboardButton("🥡 Quti ko'rinishida")
Buketli: KeyboardButton = KeyboardButton("💐 Guldasta ko'rinishida")
Back_for_Menu: KeyboardButton = KeyboardButton('⬅ Ortga')
Menu.add(Karobkali).insert(Buketli).add(Back_for_Menu)

# Karobka Keybords
Karobka: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
Back_for_Karobka: KeyboardButton = KeyboardButton('⬅ Menyuga qaytish')
Check_basket_2: KeyboardButton = KeyboardButton('📥 Savat')
Karobka.add(Check_basket_2).add(Back_for_Karobka)

# Buketli keybords
Buket: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
  [[KeyboardButton('101-tali'),
    KeyboardButton('201-tali')],
   [KeyboardButton('301-tali'),
    KeyboardButton('401-tali')],
   [KeyboardButton('501-tali'),
    KeyboardButton('601-tali')],
   [KeyboardButton('701-tali'),
    KeyboardButton('1001-tali')], [KeyboardButton('📥 Savat')],
   [KeyboardButton('⬅ Menyuga qaytish')]],
  resize_keyboard=True)

# Buyurtmalar keybords
Buyurtmalar: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
tmp_Xozir: KeyboardButton = KeyboardButton('📭 Buyurtma xozir kerak')
tmp_Vaqt: KeyboardButton = KeyboardButton('⏱ Buyurtma vaqtini yozish')
Back_Buyurtmalar: KeyboardButton = KeyboardButton("⬅ Menyuga qaytish")
Buyurtmalar.add(tmp_Xozir).insert(tmp_Vaqt).add(Back_Buyurtmalar)

# delivery keybords
Keyin: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
Xozir: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
Back_for_Xozir_Keyin: KeyboardButton = KeyboardButton('⬅ Ortga')
Xozir.add(KeyboardButton(text='📲 Telefon nomer',
                         request_contact=True)).add(Back_for_Xozir_Keyin)
cancel: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True).add(
  KeyboardButton(text='⬅ Ortga'))
Contact: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
Contact.add(KeyboardButton(text='📲 Telefon nomer', request_contact=True)).add(
  KeyboardButton(text='⬅ Geolokatsiya qaytish'))

# Each buket keybords
Each: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
Check_basket: KeyboardButton = KeyboardButton('📥 Savat')
Back_to_buket: KeyboardButton = KeyboardButton('⬅ Buketlarga qaytish')
Each.add(Check_basket).add(Back_to_buket)

# location's yes and no
YES_OR_NO_FOR_LOCATION = ReplyKeyboardMarkup(
  keyboard=[[KeyboardButton(text='✅ Ha'),
             KeyboardButton(text='❌ Yo\'q')],
            [KeyboardButton(text='⬅ Ortga')]],
  resize_keyboard=True)

# yes or no for style_write
yes_or_no: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
yes_or_no.add(KeyboardButton(text='✅ Ha'), KeyboardButton(text='❌ Yo\'q'))

# location's yes of Back
Back_for_Ha: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True)
Back_for_Ha.add(KeyboardButton(text='⬅ Ortga'))

ADMIN_CHANGE_BUTTON: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
  resize_keyboard=True)

ADMIN_CHANGE_BUTTON.add(
  KeyboardButton(text='🆕 Yangi mijozlar'),
  KeyboardButton(text='📢 Reklama yuborish')).add(
    KeyboardButton(text='💸 Narxi o\'zgartirish'),
    KeyboardButton(text='🖼️ Rasmlarni o\'zgartirish')).add(
      KeyboardButton(text='✍️ Kommentariyalarni ko\'rish'))

ADMIN_ADVERTISEMENT = ReplyKeyboardMarkup(resize_keyboard=True)
ADMIN_ADVERTISEMENT.add(KeyboardButton(text="⬅ Ortga"))

ADMIN_CHANGE_COST: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
  resize_keyboard=True)
ADMIN_CHANGE_COST.add(KeyboardButton(text='🥡 Quti narxini'),
                      KeyboardButton("💐 Guldasta narxini")).add(
                        KeyboardButton(text='⬅ Adminga qaytish'))
b_a_c_k: ReplyKeyboardMarkup = ReplyKeyboardMarkup(resize_keyboard=True).add(
  KeyboardButton(text='⬅ Ortga'))

markup_admin = ReplyKeyboardMarkup(resize_keyboard=True)
markup_admin.add(KeyboardButton(text="Bir kunlik mijozlarni tekshirish"))
markup_admin.add(
  KeyboardButton(text="Oxirgi 1 soat mobaynidagi buyurtmalarni tekshirish"))
markup_admin.add(KeyboardButton(text='Uch kunlik mijozlarni tekshirish'))
markup_admin.add(KeyboardButton(text="Oxirgi 10ta mijozlarni tekshirish")).add(
  KeyboardButton(text='⬅ Adminga qaytish'))

sozlamalar = ReplyKeyboardMarkup(resize_keyboard=True)
sozlamalar.add("Tilni o'zgartirish")
sozlamalar.add("⬅ Ortga")

change_language = ReplyKeyboardMarkup(keyboard=[[
  KeyboardButton(text='🇷🇺 Русский'),
  KeyboardButton(text='🇺🇿 O\'zbekcha')
], [KeyboardButton(text='⬅ Ortga')]],
                                      resize_keyboard=True)

change_language_begin = ReplyKeyboardMarkup(keyboard=[[
  KeyboardButton(text='🇷🇺 Русский'),
  KeyboardButton(text='🇺🇿 O\'zbekcha')
]],
                                            resize_keyboard=True)

last_agree = ReplyKeyboardMarkup(
  keyboard=[[KeyboardButton(text="✅ Ha"),
             KeyboardButton(text="❌ Yo'q")]],
  resize_keyboard=True)

comments = ReplyKeyboardMarkup(keyboard=[[
  KeyboardButton(text="1 haftalik kommentlarni o'qish"),
  KeyboardButton(text="1 kunlik kommentlarni ko'rish")
], [KeyboardButton(text="⬅ Adminga qaytish")]],
                               resize_keyboard=True)

keyboards_reply = {
  'uzb': {
    'start': start,
    'location': location,
    'Menu': Menu,
    'Karobka': Karobka,
    'Buket': Buket,
    'Buyurtmalar': Buyurtmalar,
    'Keyin': Keyin,
    'Xozir': Xozir,
    'cancel': cancel,
    'Contact': Contact,
    'Each': Each,
    'YES_OR_NO_FOR_LOCATION': YES_OR_NO_FOR_LOCATION,
    'yes_or_no': yes_or_no,
    'Back_for_Ha': Back_for_Ha,
    'ADMIN_CHANGE_BUTTON': ADMIN_CHANGE_BUTTON,
    "ADMIN_ADVERTISEMENT": ADMIN_ADVERTISEMENT,
    'b_a_c_k': b_a_c_k,
    'ADMIN_CHANGE_COST': ADMIN_CHANGE_COST,
    'markup_admin': markup_admin,
    'sozlamalar': sozlamalar,
    'change_language': change_language,
    'last_agree': last_agree,
    'change_language_begin': change_language_begin
  },
  'rus': {
    'start': start_ru,
    'location': location_ru,
    'Menu': Menu_ru,
    'Karobka': Karobka_ru,
    'Buket': Buket_ru,
    'Buyurtmalar': Buyurtmalar_ru,
    'Keyin': Keyin_ru,
    'Xozir': Xozir_ru,
    'cancel': cancel_ru,
    'Contact': Contact_ru,
    'Each': Each_ru,
    'YES_OR_NO_FOR_LOCATION': YES_OR_NO_FOR_LOCATION_ru,
    'yes_or_no': yes_or_no_ru,
    'Back_for_Ha': Back_for_Ha_ru,
    'b_a_c_k': b_a_c_k_ru,
    'sozlamalar': sozlamalar_ru,
    'change_language': change_language_ru,
    "last_agree": last_agree_ru,
    'change_language_begin': change_language_begin
  }
}
