from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.inline.callback_datas import savat_callback, Delivary
from keyboards.inline.russian_choise_inline_buttons import to_karobka_ru, how_much_choise_ru, confirmation_ru

# For Karobka inline_buttons
to_karobka = InlineKeyboardMarkup(inline_keyboard=[
  [
    InlineKeyboardButton(text="-",
                         callback_data=savat_callback.new(item_name="minus",
                                                          how_much=0)),
    InlineKeyboardButton(text='1',
                         callback_data=savat_callback.new(item_name='sum',
                                                          how_much=1)),
    InlineKeyboardButton(text="+",
                         callback_data=savat_callback.new(item_name="plus",
                                                          how_much=0))
  ],
  [
    InlineKeyboardButton(text="📥 Buyurtmaga qo'shish",
                         callback_data=Delivary.new(item_name="Delivary",
                                                    which_item='Qutili',
                                                    how_many=1,
                                                    how_much_it='250.000'))
  ]
],
                                  row_width=3)

# for each bukets inline_buttons
how_much_choise = []
button_labels = [
  '101-tali', '201-tali', '301-tali', '401-tali', '501-tali', '601-tali',
  '701-tali', '1001-tali'
]
selling_rate = [
  '180.000', '280.000', '380.000', '500.000', '600.000', '700.000', '900.000',
  '1800.000'
]
all_zip_data = dict(zip(button_labels, selling_rate))
for i in all_zip_data:
  keyboard = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text="-",
                         callback_data=savat_callback.new(item_name="minus",
                                                          how_much=0)),
    InlineKeyboardButton(text='1',
                         callback_data=savat_callback.new(item_name='sum',
                                                          how_much=1)),
    InlineKeyboardButton(text="+",
                         callback_data=savat_callback.new(item_name="plus",
                                                          how_much=0))
  ]],
                                  row_width=3)
  keyboard.add(
    InlineKeyboardButton(text="📥 Buyurtmaga qo'shish",
                         callback_data=Delivary.new(
                           item_name="Delivary",
                           which_item=i,
                           how_many=1,
                           how_much_it=all_zip_data[i])))
  how_much_choise.append(keyboard)

confirmation = InlineKeyboardMarkup()
confirmation.add(
  InlineKeyboardButton(text='✅ Tasdiqlash', callback_data='confirm'),
  InlineKeyboardButton(text='❌ Bekor qilish', callback_data='cancel'))

inline_keyboards = {
  'uzb': {
    'to_karobka': to_karobka,
    'how_much_choise': how_much_choise,
    'confirmation': confirmation
  },
  'rus': {
    'to_karobka': to_karobka_ru,
    'how_much_choise': how_much_choise_ru,
    'confirmation': confirmation_ru
  }
}
