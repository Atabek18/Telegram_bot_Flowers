from keyboards.inline.russian_choise_inline_buttons import how_much_choise_ru
from keyboards.reply.russian_choise_reply_buttons import Each_ru, Menu_ru
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import pandas as pd
import sqlite3
from handlers.uzb_users.for_run_inline1 import DL


def number_to_emoji(number):
  emoji_digits = [
    '0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣'
  ]
  return ''.join(emoji_digits[int(digit)] for digit in str(number))


@dp.message_handler(lambda message: message.text == "📥 Корзина")
async def check_is_buy(message: types.Message):
  conn = sqlite3.connect('flower.db')
  cursor = conn.cursor()
  cursor.execute(
    "SELECT how_many, buket, how_much_it FROM shopping WHERE is_fulfilled = ? and user_id = ?",
    ('No', message.chat.id))
  query = cursor.fetchall()

  conn1, cursor1 = DL.qui_sql()
  cursor1.execute(
    "SELECT buket FROM shopping WHERE user_id=? AND is_fulfilled=?",
    (message.chat.id, 'No'))
  select = cursor1.fetchall()
  set_select = set([i[0] for i in select])
  uzb = [
    '101-tali', '201-tali', '301-tali', '401-tali', '501-tali', '601-tali',
    '701-tali', '1001-tali', 'Qutili'
  ]
  rus = ['101', '201', '301', '401', '501', '601', '701', '1001', 'Kоробкa']
  get_it = dict(zip(uzb, rus))
  key = [
    types.InlineKeyboardButton(text='❌' + get_it[i],
                               callback_data='del{}'.format(i))
    for i in set_select
  ]
  new_but1 = InlineKeyboardMarkup(
    inline_keyboard=[[
      InlineKeyboardButton(
        text='🚖 Заказать', callback_data='open_delivery', cache_time=1)
    ],
                     [
                       InlineKeyboardButton(text='⬅ Назад',
                                            callback_data='close'),
                       InlineKeyboardButton(text='🗑 Очистить корзину',
                                            callback_data='clear_to_')
                     ]]).add(*key)
  if query:
    df = pd.DataFrame(query, columns=['nechta', 'buket', 'narxi'])
    df['buket'] = df['buket'].str.replace('Qutili', 'Kоробкa')
    df['buket'] = df['buket'].str.replace('-tali', '')
    df['narxi'] = [int("".join(i.split('.'))) for i in df['narxi']]
    df = df.sort_values(by='narxi', ascending=True)
    df['narxi'] = df['nechta'] * df['narxi']
    group = df.groupby('buket').sum()
    group.insert(1, 'buket_name', group.index.values)
    total_narx = group['narxi'].sum()
    group['narxi'] = group['narxi'].astype(str)
    group['narxi'] = [
      i[:-6] + '.' + i[-6:-3] + '.' + i[-3:] if i[:-6] else i[:-3] + '.' +
      i[-3:] for i in group['narxi']
    ]
    group['nechta'] = [
      number_to_emoji(group['nechta'][i]) for i in range(len(group['nechta']))
    ]
    group.insert(1, 'X', ['✖️' for i in range(len(group))])
    group.insert(3, 'teng', ['🟰' for i in range(len(group))])
    yol_haqqi = '30.000 сумов'
    total_temp = str(total_narx + 30000)
    total = total_temp[:-6] + '.' + total_temp[-6:-3] + '.' + total_temp[
      -3:] if total_temp[:-6] != '' else total_temp[-6:-3] + '.' + total_temp[
        -3:]
    total_narx_ = str(total_narx)[:-6] + '.' + str(
      total_narx)[-6:-3] + '.' + str(total_narx)[-3:] if str(
        total_narx
      )[:-6] != '' else str(total_narx)[-6:-3] + '.' + str(total_narx)[-3:]
    await message.answer(
      f'📥 Внутри корзины имеется:\n{group.to_string(index=False, header=False)}\nЗа товары: {str(total_narx_)} сумма\nЗа доставку: {yol_haqqi}\nОбщая сумма: {total} суммов',
      reply_markup=new_but1)
  else:
    await message.reply('📥 Ваша корзина пуста')


button_labels = [
  '101', '201', '301', '401', '501', '601', '701', '1001', '⬅ Назад в меню'
]


async def button_handler(message: types.Message, state: FSMContext):
  if message.text == '⬅ Назад в меню':
    await message.answer("Выберите одну из следующих:", reply_markup=Menu_ru)
  else:
    button_label = message.text
    await message.answer('Выберите количество букета:', reply_markup=Each_ru)

    sp = button_label.split('-')[0]
    for i in how_much_choise_ru:
      if i.inline_keyboard[1][0].callback_data.split(':')[2].split(
          '-')[0] == sp:
        with open(f'imgs/{sp}tali.jpg', 'rb') as photo_:
          await bot.send_photo(
            chat_id=message.chat.id,
            photo=photo_,
            caption=
            f'Букет которого вы выбрали: {sp}\nЦена: {i.inline_keyboard[1][0].callback_data.split(":")[-1]} суммов',
            reply_markup=i)


for label in button_labels:
  dp.register_message_handler(button_handler, Text(label))
