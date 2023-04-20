from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.inline.callback_datas import savat_callback, Delivary

# For Karobka inline_buttons
to_karobka_ru = InlineKeyboardMarkup(inline_keyboard=[
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
    InlineKeyboardButton(text="📥 Добавить в корзину",
                         callback_data=Delivary.new(item_name="Delivary",
                                                    which_item='Kоробкa',
                                                    how_many=1,
                                                    how_much_it='250.000'))
  ]
],
                                     row_width=3)

# for each bukets inline_buttons
how_much_choise_ru = []
button_labels_ru = ['101', '201', '301', '401', '501', '601', '701', '1001']
selling_rate_ru = [
  '180.000', '280.000', '380.000', '500.000', '600.000', '700.000', '900.000',
  '1800.000'
]
all_zip_data_ru = dict(zip(button_labels_ru, selling_rate_ru))
for i in all_zip_data_ru:
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
    InlineKeyboardButton(text="📥 Добавить в корзину",
                         callback_data=Delivary.new(
                           item_name="Delivary",
                           which_item=i,
                           how_many=1,
                           how_much_it=all_zip_data_ru[i])))
  how_much_choise_ru.append(keyboard)

confirmation_ru = InlineKeyboardMarkup()
confirmation_ru.add(
  InlineKeyboardButton(text='✅ Подтвердить', callback_data='confirm'),
  InlineKeyboardButton(text='❌ Отмена', callback_data='cancel'))
