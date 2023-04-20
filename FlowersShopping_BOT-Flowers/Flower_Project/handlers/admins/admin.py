from keyboards.reply.choise_reply_buttons import ADMIN_CHANGE_COST, ADMIN_CHANGE_BUTTON, b_a_c_k, markup_admin, ADMIN_ADVERTISEMENT, comments
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, ContentTypes, Message
from handlers.uzb_users.States import Authentication, CHANGE_Karobka, Change_Buket, Change_pic, Advertisement
from keyboards.inline.choice_inline_buttons import how_much_choise, to_karobka
from keyboards.inline.russian_choise_inline_buttons import to_karobka_ru, how_much_choise_ru
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
import pytz
from PIL import Image

load_dotenv()
PASSWORD = os.environ.get('PASSWORD')
ADMIN_ID = os.environ.get('ADMIN_ID')
from loader import dp, bot
from aiogram import types
import sqlite3 as sql
import pandas as pd

db = sql.connect("flower.db")
cursor = db.cursor()


@dp.message_handler(user_id=ADMIN_ID, commands=['admin'])
async def admin_panel(message: Message, state: FSMContext):
  await message.reply('Iltimos adminning parolini kiriting:',
                      reply_markup=ReplyKeyboardRemove())
  await Authentication.password.set()


@dp.message_handler(user_id=ADMIN_ID, text='⬅ Adminga qaytish')
async def back_admin(message: Message, state: FSMContext):
  await message.reply('Admin panel', reply_markup=ADMIN_CHANGE_BUTTON)


@dp.message_handler(user_id=ADMIN_ID, state=Authentication.password)
async def password(message: Message, state: FSMContext):
  if message.text == PASSWORD:
    await message.reply('Sizning kiritgan parolingiz to\'g\'ri',
                        reply_markup=ADMIN_CHANGE_BUTTON)
    await state.finish()
  else:
    await message.reply('Iltimos qayta urinib ko\'ring')


@dp.message_handler(user_id=ADMIN_ID, text='💸 Narxi o\'zgartirish')
async def change_karobka_cost(message: Message):
  await message.reply('Qaysi gul oramini ozgartirasiz',
                      reply_markup=ADMIN_CHANGE_COST)


@dp.message_handler(user_id=ADMIN_ID, text='🆕 Yangi mijozlar')
async def New_customers(message: Message):
  await message.reply('Yangi mijozlar tekshirish qismi',
                      reply_markup=markup_admin)


@dp.message_handler(user_id=ADMIN_ID, text='🥡 Quti narxini')
async def currant_narx(message: Message):
  await message.answer(
    f'Karobkalini narxi: {to_karobka.inline_keyboard[1][0].callback_data.split(":")[-1]} sum\nNarxi ozgartirmoqchi bo\'lsangiz pastga yozing\nIltimos {to_karobka.inline_keyboard[1][0].callback_data.split(":")[-1]} mashunaqa formatda bo\'lsin',
    reply_markup=b_a_c_k)
  await CHANGE_Karobka.narxi_korish.set()


@dp.message_handler(user_id=ADMIN_ID, state=CHANGE_Karobka.narxi_korish)
async def show_karobka_cost(message: Message, state: FSMContext):
  if message.text == '⬅ Ortga':
    await message.reply('Siz ortga qaytingiz', reply_markup=ADMIN_CHANGE_COST)
    await state.finish()
  else:
    xozirgi_narxi_ru = to_karobka_ru.inline_keyboard[1][0].callback_data.split(
      ':')[-1]
    try:
      ozgargan = message.text
      callback = to_karobka.inline_keyboard[1][0].callback_data
      callback_ru = to_karobka_ru.inline_keyboard[1][0].callback_data
      to_karobka.inline_keyboard[1][0].callback_data = ':'.join(
        callback.split(':')[:-1] + [ozgargan])
      to_karobka_ru.inline_keyboard[1][0].callback_data = ':'.join(
        callback_ru.split(':')[:-1] + [ozgargan])
      await message.reply(
        f'Muvaffaqiyatli ozgartirildi !!!\nOzgargan naxr: {to_karobka.inline_keyboard[1][0].callback_data.split(":")[-1]}',
        reply_markup=ADMIN_CHANGE_COST)
      await state.finish()
    except:
      await message.reply(
        f'Xato kiritingiz!!!\nIltimos {xozirgi_narxi_ru} mashunaqa formatda bo\'lsin'
      )


Buketlar_narxi: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
  [[KeyboardButton('101-tali narxi'),
    KeyboardButton('201-tali narxi')],
   [KeyboardButton('301-tali narxi'),
    KeyboardButton('401-tali narxi')],
   [KeyboardButton('501-tali narxi'),
    KeyboardButton('601-tali narxi')],
   [KeyboardButton('701-tali narxi'),
    KeyboardButton('1001-tali narxi')], [KeyboardButton('⬅ Gularga qaytish')]],
  resize_keyboard=True)


@dp.message_handler(user_id=ADMIN_ID, text='💐 Guldasta narxini')
async def each_buket(message: Message):
  await message.answer('Bu hamma buketlar', reply_markup=Buketlar_narxi)


async def currant_narx1(message: Message, state: FSMContext):
  if message.text == '⬅ Gularga qaytish':
    await message.reply('Siz ortga qaytingiz', reply_markup=ADMIN_CHANGE_COST)
    await state.finish()
  else:
    for i in how_much_choise:
      if i.inline_keyboard[1][0].callback_data.split(
          ":")[-3] == message.text.split(' ')[0]:
        async with state.proxy() as data:
          data['which_item'] = message.text.split(' ')[0]
          data['narxi'] = i.inline_keyboard[1][0].callback_data.split(":")[-1]
        await message.answer(
          f'💐 Guldasta narxi: {i.inline_keyboard[1][0].callback_data.split(":")[-1]} sum\nNarxi ozgartirmoqchi bo\'lsangiz                                    pastga yozing\nIltimos {i.inline_keyboard[1][0].callback_data.split(":")[-1]} mashunaqa formatda bo\'lsin',
          reply_markup=b_a_c_k)
        await Change_Buket.narxi_korish1.set()


button_labels = [
  '101-tali narxi', '201-tali narxi', '301-tali narxi', '401-tali narxi',
  '501-tali narxi', '601-tali narxi', '701-tali narxi', '1001-tali narxi',
  '⬅ Gularga qaytish'
]
for i in button_labels:
  dp.register_message_handler(currant_narx1, Text(i), user_id=ADMIN_ID)


@dp.message_handler(user_id=ADMIN_ID, state=Change_Buket.narxi_korish1)
async def show_buket_cost(message: Message, state: FSMContext):
  if message.text == '⬅ Ortga':
    await message.answer('Qaysi gul oramini ozgartirasiz',
                         reply_markup=ADMIN_CHANGE_COST)
    await state.finish()
  else:
    try:
      ozgargan_narxi = message.text
      async with state.proxy() as data:
        pressed = data['which_item']
        for i in how_much_choise_ru:
          if i.inline_keyboard[1][0].callback_data.split(
              ":")[-3] == pressed.split('-')[0]:
            callback_buket_ru = i.inline_keyboard[1][0].callback_data
            i.inline_keyboard[1][0].callback_data = ':'.join(
              callback_buket_ru.split(':')[:-1] + [ozgargan_narxi])
        for i1 in how_much_choise:
          if i1.inline_keyboard[1][0].callback_data.split(":")[-3] == pressed:
            callback_buket = i1.inline_keyboard[1][0].callback_data
            i1.inline_keyboard[1][0].callback_data = ':'.join(
              callback_buket.split(':')[:-1] + [ozgargan_narxi])
            await message.reply(
              f'Muvaffaqiyatli ozgartirildi !!!\nOzgargan naxr: {i1.inline_keyboard[1][0].callback_data.split(":")[-1]}',
              reply_markup=Buketlar_narxi)
      await state.finish()
    except:
      async with state.proxy() as data:
        pressed_narx = data['narxi']
        await message.reply(
          f'Xato kiritingiz!!!\nIltimos {pressed_narx} mashunaqa formatda bo\'lsin'
        )


@dp.message_handler(user_id=ADMIN_ID, text='Bir kunlik mijozlarni tekshirish')
async def check_new_cust1(message: types.Message):
  for_yes = "Yes"
  uz_date = pytz.timezone("Asia/Tashkent")
  day_ago = datetime.now(uz_date) - timedelta(days=7)
  request_day_ago = cursor.execute(
    f"SELECT * FROM shopping WHERE order_time >= '{day_ago}' AND is_fulfilled == '{for_yes}'"
  )
  sorted_data = sorted(request_day_ago.fetchall(), key=lambda x: x[0])
  num_orders = pd.DataFrame({
    "Bugungi buyurtmalar": len(sorted_data)
  },
                            index=[1]).transpose()
  num_orders.columns = [" "]
  for i in range(len(sorted_data)):
    df = pd.DataFrame(
      {
        "ID:                    ": sorted_data[i][0],
        "Yetkazish vaqti:       ": sorted_data[i][10],
        "Guldasta turi:         ": sorted_data[i][4],
        "Nechta donaligi:       ": sorted_data[i][5],
        "Necha pulligi:         ": sorted_data[i][6],
        "Guldasta ustiga yozuvi:": sorted_data[i][7],
        "Ismi:                  ": sorted_data[i][2],
        "Familiyasi:            ": sorted_data[i][3],
        "Nomeri:                ": sorted_data[i][9]
      },
      index=[0]).transpose()
    df.columns = [" "]
    await bot.send_location(chat_id=ADMIN_ID,
                            latitude=sorted_data[i][14],
                            longitude=sorted_data[i][13])
    await message.answer(
      f"ID:\t\t\t{sorted_data[i][0]}\nManzil:\n{sorted_data[i][12]}")
    await message.answer(df)
  await message.answer(num_orders)


@dp.message_handler(user_id=ADMIN_ID, text='Uch kunlik mijozlarni tekshirish')
async def check_new_cust3(message: types.Message):
  for_yes = "Yes"
  uz_date = pytz.timezone("Asia/Tashkent")
  day_ago = datetime.now(uz_date) - timedelta(days=7)
  request_day_ago = cursor.execute(
    f"SELECT * FROM shopping WHERE order_time >= '{day_ago}' AND is_fulfilled == '{for_yes}'"
  )
  sorted_data = sorted(request_day_ago.fetchall(), key=lambda x: x[0])
  num_orders = pd.DataFrame({
    "Bugungi buyurtmalar": len(sorted_data)
  },
                            index=[1]).transpose()
  num_orders.columns = [" "]
  for i in range(len(sorted_data)):
    df = pd.DataFrame(
      {
        "ID:                    ": sorted_data[i][0],
        "Yetkazish vaqti:       ": sorted_data[i][10],
        "Guldasta turi:         ": sorted_data[i][4],
        "Nechta donaligi:       ": sorted_data[i][5],
        "Necha pulligi:         ": sorted_data[i][6],
        "Guldasta ustiga yozuvi:": sorted_data[i][7],
        "Ismi:                  ": sorted_data[i][2],
        "Familiyasi:            ": sorted_data[i][3],
        "Nomeri:                ": sorted_data[i][9]
      },
      index=[0]).transpose()
    df.columns = [" "]
    await bot.send_location(chat_id=ADMIN_ID,
                            latitude=sorted_data[i][14],
                            longitude=sorted_data[i][13])
    await message.answer(
      f"ID:\t\t\t{sorted_data[i][0]}\nManzil:\n{sorted_data[i][12]}")
    await message.answer(df)
  await message.answer(num_orders)


@dp.message_handler(user_id=ADMIN_ID,
                    text='Oxirgi 1 soat mobaynidagi buyurtmalarni tekshirish')
async def check_1_hour(message: types.Message):
  uz_date = pytz.timezone("Asia/Tashkent")
  one_hour = datetime.now(uz_date) - timedelta(days=7)
  request_day_ago = cursor.execute(
    f"SELECT * FROM shopping WHERE order_time >= '{one_hour}' AND is_fulfilled == 'Yes'"
  )
  one_hour_ago = sorted(request_day_ago.fetchall(), key=lambda x: x[0])
  num_orders = pd.DataFrame({
    "Bugungi buyurtmalar": len(one_hour_ago)
  },
                            index=[1]).transpose()
  num_orders.columns = [" "]
  for i in range(len(one_hour_ago)):
    df = pd.DataFrame(
      {
        "ID:                    ": one_hour_ago[i][0],
        "Yetkazish vaqti:       ": one_hour_ago[i][10],
        "Guldasta turi:         ": one_hour_ago[i][4],
        "Nechta donaligi:       ": one_hour_ago[i][5],
        "Necha pulligi:         ": one_hour_ago[i][6],
        "Guldasta ustiga yozuvi:": one_hour_ago[i][7],
        "Ismi:                  ": one_hour_ago[i][2],
        "Familiyasi:            ": one_hour_ago[i][3],
        "Nomeri:                ": one_hour_ago[i][9]
      },
      index=[0]).transpose()
    df.columns = [" "]
    await bot.send_location(chat_id=ADMIN_ID,
                            latitude=one_hour_ago[i][14],
                            longitude=one_hour_ago[i][13])
    await message.answer(
      f"ID:\t\t\t{one_hour_ago[i][0]}\nManzil:\n{one_hour_ago[i][12]}")
    await message.answer(df)
  await message.answer(num_orders)


@dp.message_handler(user_id=ADMIN_ID, text="Oxirgi 10ta mijozlarni tekshirish")
async def check_10_last(message: types.Message):
  rows_10 = cursor.execute(
    "SELECT * FROM shopping WHERE is_fulfilled == 'Yes' ORDER BY order_time DESC LIMIT 10"
  )
  row_of_10_data = sorted(rows_10.fetchall(), key=lambda x: x[0])
  num_orders = pd.DataFrame({
    "Bugungi buyurtmalar": len(row_of_10_data)
  },
                            index=[1]).transpose()
  num_orders.columns = [" "]
  for i in range(len(row_of_10_data)):
    df = pd.DataFrame(
      {
        "ID:                    ": row_of_10_data[i][0],
        "Yetkazish vaqti:       ": row_of_10_data[i][10],
        "Guldasta turi:         ": row_of_10_data[i][4],
        "Nechta donaligi:       ": row_of_10_data[i][5],
        "Necha pulligi:         ": row_of_10_data[i][6],
        "Guldasta ustiga yozuvi:": row_of_10_data[i][7],
        "Ismi:                  ": row_of_10_data[i][2],
        "Familiyasi:            ": row_of_10_data[i][3],
        "Nomeri:                ": row_of_10_data[i][9]
      },
      index=[0]).transpose()
    df.columns = [" "]
    await bot.send_location(chat_id=ADMIN_ID,
                            latitude=row_of_10_data[i][14],
                            longitude=row_of_10_data[i][13])
    await message.answer(
      f"ID:\t\t\t{row_of_10_data[i][0]}\nManzil:\n{row_of_10_data[i][12]}")
    await message.answer(df)
  await message.answer(num_orders)


@dp.message_handler(user_id=ADMIN_ID, text="📢 Reklama yuborish")
async def advertsement(message: Message, state: FSMContext):
  await message.answer("Pastga post qoldirib uni tagiga tekstlarni yozing",
                       reply_markup=ADMIN_ADVERTISEMENT)
  await Advertisement.adver.set()


@dp.message_handler(user_id=ADMIN_ID,
                    content_types=types.ContentType.PHOTO,
                    state=Advertisement.adver)
async def post(message: Message, state: FSMContext):
  text_for_photo = message.caption
  if message.content_type == types.ContentType.PHOTO:
    cursor.execute("SELECT user_id FROM translates_from_id")
    yes_users = [*set(cursor.fetchall())]
    for i in yes_users:
      if i[0] != str(ADMIN_ID):
        try:
          photo_file_id = message.photo[-1].file_id
          await bot.send_photo(photo=photo_file_id,
                               chat_id=i[0],
                               caption=text_for_photo)
        except:
          pass
      else:
        pass
    await message.answer('👍 Muvaffaqiyatli yuborildi',
                         reply_markup=ADMIN_CHANGE_BUTTON)
    await state.finish()
  else:
    await message.answer("Nmadur xato ketti qaytadan urinib ko'ring")


@dp.message_handler(user_id=ADMIN_ID,
                    text="⬅ Ortga",
                    state=Advertisement.adver)
async def back_from_adver(message: Message, state: FSMContext):
  await message.reply("Admin panelga Xush kelibsiz",
                      reply_markup=ADMIN_CHANGE_BUTTON)
  await state.finish()


Buket_rasmlar: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
  [[KeyboardButton('101-tali rasmni'),
    KeyboardButton('201-tali rasmni')],
   [KeyboardButton('301-tali rasmni'),
    KeyboardButton('401-tali rasmni')],
   [KeyboardButton('501-tali rasmni'),
    KeyboardButton('601-tali rasmni')],
   [KeyboardButton('701-tali rasmni'),
    KeyboardButton('1001-tali rasmni')], [KeyboardButton('Karobkali rasmni')],
   [KeyboardButton('⬅ Adminga qaytish')]],
  resize_keyboard=True)


@dp.message_handler(user_id=ADMIN_ID, text='🖼️ Rasmlarni o\'zgartirish')
async def Forward_to_change(message: Message):
  await message.answer(text='Quydagilardan birini tanglang',
                       reply_markup=Buket_rasmlar)


async def show_pictures(message: Message, state: FSMContext):
  if message.text == '⬅ Adminga qaytish':
    await message.answer('Quydagilardan birini tanglang',
                         reply_markup=ADMIN_CHANGE_BUTTON)
    await state.finish()
  else:
    file_path = message.text.split(
      '-')[0] + 'tali' if 'Karobkali' not in message.text else 'Kоробкa'
    with open(f'imgs/{file_path}.jpg', 'rb') as img:
      await bot.send_photo(
        chat_id=ADMIN_ID,
        photo=img,
        caption="O'zgartirmoqchi bo'lgan rasimingizni tashang",
        reply_markup=b_a_c_k)
      async with state.proxy() as data:
        data['file_path'] = f'imgs/{file_path}.jpg'
    await Change_pic.change_picture.set()


pictues_labels = [
  '101-tali rasmni', '201-tali rasmni', '301-tali rasmni', '401-tali rasmni',
  '501-tali rasmni', '601-tali rasmni', '701-tali rasmni', '1001-tali rasmni',
  'Karobkali rasmni', '⬅ Ortga'
]
for pictures in pictues_labels:
  dp.register_message_handler(show_pictures, Text(pictures), user_id=ADMIN_ID)


async def replace_image(old_image, new_image: str) -> bytes:
  os.remove(old_image)
  with Image.open(new_image) as new_img:
    new_img.save(old_image)


@dp.message_handler(user_id=ADMIN_ID,
                    content_types=ContentTypes.PHOTO,
                    state=Change_pic.change_picture)
async def Change_it(message: Message, state: FSMContext):
  photo_file_id = message.photo[-1].file_id
  file_path = await bot.download_file_by_id(photo_file_id)
  async with state.proxy() as data:
    await replace_image(data['file_path'], file_path)
  await message.answer('Muvaffaqiyatli o\'zgartirildi! 👍',
                       reply_markup=ADMIN_CHANGE_BUTTON)
  await state.finish()


@dp.message_handler(user_id=ADMIN_ID,
                    text='⬅ Ortga',
                    state=Change_pic.change_picture)
async def back_only_pic(message: Message, state: FSMContext):
  await message.answer('Quydagilardan birini tanglang',
                       reply_markup=Buket_rasmlar)
  await state.finish()\


@dp.message_handler(user_id=ADMIN_ID, text="✍️ Kommentariyalarni ko'rish")
async def check_comments(message: Message):
  await message.reply("Quyidagilardan birini tanlang:", reply_markup=comments)


@dp.message_handler(user_id=ADMIN_ID, text="1 haftalik kommentlarni o'qish")
async def check_one_week_comments(message: Message):
  uz_date = pytz.timezone("Asia/Tashkent")
  one_week = datetime.now(uz_date) - timedelta(days=7)
  request_week_ago = cursor.execute(
    f"SELECT * FROM comment WHERE yozgan_vaqti >= '{one_week}'")
  request_week_data = sorted(request_week_ago.fetchall(), key=lambda x: x[0])
  for i in request_week_data:
    df_for_week_comments = pd.DataFrame(
      {
        "ID: ": i[0],
        "User_id: ": i[1],
        "Comment yozgan vaqti: ": i[3]
      },
      index=[0]).transpose()
    df_for_week_comments.columns = [" "]
    comment_week = i[2]
    await message.answer(df_for_week_comments)
    await message.answer(comment_week)


@dp.message_handler(user_id=ADMIN_ID, text="1 kunlik kommentlarni ko'rish")
async def check_one_day_comments(message: Message):
  uzb_date = pytz.timezone("Asia/Tashkent")
  one_day = datetime.now(uzb_date) - timedelta(days=1)
  request_one_day = cursor.execute(
    f"SELECT * FROM comment WHERE yozgan_vaqti >= '{one_day}'")
  request_one_data = sorted(request_one_day.fetchall(), key=lambda x: x[0])
  for i in request_one_data:
    df_for_day_comments = pd.DataFrame(
      {
        "ID: ": i[0],
        "User_id: ": i[1],
        "Comment yozgan vaqti: ": i[3]
      },
      index=[0]).transpose()
    df_for_day_comments.columns = [" "]
    comment_day = i[2]
    await message.answer(df_for_day_comments)
    await message.answer(comment_day)
