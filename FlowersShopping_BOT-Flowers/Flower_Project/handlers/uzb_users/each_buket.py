from keyboards.inline.choice_inline_buttons import how_much_choise
from keyboards.reply.choise_reply_buttons import Each, Menu
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import pandas as pd
import sqlite3


def get_data(data):
  df = pd.DataFrame(data, columns=['nechta', 'buket', 'narxi'])
  df['narxi'] = [int(''.join(i.split('.'))) for i in df['narxi']]
  df = df.sort_values(by='narxi', ascending=False)
  df['narxi'] = df['nechta'] * df['narxi']
  group = df.groupby('buket').sum()
  group.insert(1, 'buket_name', group.index.values)
  total_narx = group['narxi'].sum()
  group['narxi'] = group['narxi'].astype(str)
  group['narxi'] = [
    i[:-6] + '.' + i[-6:-3] + '.' + i[-3:] if i[:-6] else i[:-3] + '.' + i[-3:]
    for i in group['narxi']
  ]
  group['nechta'] = [
    number_to_emoji(group['nechta'][i]) for i in range(len(group['nechta']))
  ]
  group.insert(1, 'X', ['✖️' for i in range(len(group))])
  group.insert(3, 'teng', ['🟰' for i in range(len(group))])
  yol_haqqi = '30.000 so\'m'
  total_temp = str(total_narx + 30000)
  total = total_temp[:-6] + '.' + total_temp[-6:-3] + '.' + total_temp[
    -3:] if total_temp[:-6] != '' else total_temp[-6:-3] + '.' + total_temp[-3:]
  total_narx_ = str(total_narx)[:-6] + '.' + str(total_narx)[
    -6:-3] + '.' + str(total_narx)[-3:] if str(total_narx)[:-6] != '' else str(
      total_narx)[-6:-3] + '.' + str(total_narx)[-3:]
  return group, total_narx_, yol_haqqi, total


def number_to_emoji(number):
  emoji_digits = [
    '0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣'
  ]
  return ''.join(emoji_digits[int(digit)] for digit in str(number))


@dp.message_handler(text=["📥 Savat"])
async def check_is_buy(message: types.Message):
  conn1 = sqlite3.connect('flower.db')
  cursor1 = conn1.cursor()
  cursor1.execute(
    "SELECT buket FROM shopping WHERE user_id=? AND is_fulfilled=?",
    (message.chat.id, 'No'))
  set_select = set([i[0] for i in cursor1.fetchall()])
  key = [
    types.InlineKeyboardButton(text='❌' + i, callback_data='del{}'.format(i))
    for i in set_select
  ]
  new_but = InlineKeyboardMarkup(
    inline_keyboard=[[
      InlineKeyboardButton(
        text='🚖 Buyurtma Berish', callback_data='open_delivery', cache_time=1)
    ],
                     [
                       InlineKeyboardButton(text='⬅ Ortga',
                                            callback_data='close'),
                       InlineKeyboardButton(text='🗑 Savatni tozalash',
                                            callback_data='clear_to_')
                     ]]).add(*key)
  conn = sqlite3.connect('flower.db')
  cursor = conn.cursor()
  cursor.execute(
    "SELECT how_many, buket, how_much_it FROM shopping WHERE is_fulfilled = ? and user_id = ?",
    ('No', message.chat.id))
  query = cursor.fetchall()
  if query:
    group, total_narx_, yol_haqqi, total = get_data(query)

    await message.answer(
      f'📥 Savat ichida:\n{group.to_string(index=False, header=False)}\nTovarlar: {str(total_narx_)} so\'m\nYo\'l haqqi: {yol_haqqi}\nJami: {total} so\'m',
      reply_markup=new_but)
  else:
    await message.reply('📥 Savatingiz xozircha bo\'sh')


button_labels = [
  '101-tali', '201-tali', '301-tali', '401-tali', '501-tali', '601-tali',
  '701-tali', '1001-tali', '⬅ Menyuga qaytish'
]


async def button_handler(message: types.Message, state: FSMContext):
  if message.text == '⬅ Menyuga qaytish':
    await message.answer("Quyidagilardan birini tanlang", reply_markup=Menu)
  else:
    button_label = message.text
    await message.answer('Buyurtma miqdorini tanlang:', reply_markup=Each)

    sp = button_label.split('-')[0]
    for i in how_much_choise:
      if i.inline_keyboard[1][0].callback_data.split(':')[2].split(
          '-')[0] == sp:
        with open(f'imgs/{sp}tali.jpg', 'rb') as photo_:
          await bot.send_photo(
            message.chat.id,
            photo=photo_,
            caption=
            f'Siz tanlagan guldasta: {sp}-tali\nNarxi: {i.inline_keyboard[1][0].callback_data.split(":")[-1]} so\'m',
            reply_markup=i)


for label in button_labels:
  dp.register_message_handler(button_handler, Text(label))
