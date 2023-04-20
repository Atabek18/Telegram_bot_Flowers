from keyboards.reply.choise_reply_buttons import keyboards_reply
from keyboards.inline.choice_inline_buttons import inline_keyboards
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.markdown import text, italic, code
from handlers.uzb_users.for_run_inline1 import DL
from database.sqlite_db_user import CREATE_DB
from aiogram.dispatcher.filters import Text
from deep_translator import GoogleTranslator
from aiogram.dispatcher import FSMContext
from handlers.uzb_users import States
from datetime import datetime
from geopy import Nominatim
from loader import dp, bot
from aiogram import types
import sqlite3
import pytz
import pandas as pd

uzb_tz = pytz.timezone('Asia/Tashkent')
utc_now = datetime.utcnow()
uzb_now = utc_now.astimezone(uzb_tz)
current_time_tash = uzb_now.strftime('%Y-%m-%d %H:%M')

####################DB_CREATE_PLACE###################################
LOCATION_DB = CREATE_DB(db_file_name='flower.db', tabel_name='location_ident')
LOCATION_DB.ST_DB(
  values="""(id INTEGER PRIMARY KEY AUTOINCREMENT,user_id TEXT NOT NULL,
                            location_name TEXT NOT NULL, location_latitude TEXT NOT NULL,
                            location_longitude TEXT NOT NULL)""")

TRANSLATE_USER_LANG = CREATE_DB(db_file_name='flower.db',
                                tabel_name='translates_from_id')
TRANSLATE_USER_LANG.ST_DB(
  values="""(user_id INTEGER PRIMARY KEY,language TEXT NOT NULL)""")


@dp.message_handler(text='🇺🇿 O\'zbekcha')
async def to_Uzb(message: types.Message):
  conn, cursor = TRANSLATE_USER_LANG.qui_sql()
  cursor.execute(
    "UPDATE translates_from_id SET language = ? WHERE user_id = ?",
    ('uzb', int(message.chat.id)))
  conn.commit()
  dict_f = {'uzb': 'Bizning gul do\'konimizga xush kelibsiz'}
  cursor.execute(
    f"SELECT language FROM translates_from_id WHERE user_id = {message.chat.id}"
  )
  select = cursor.fetchall()
  await message.answer(dict_f[select[0][0]],
                       reply_markup=keyboards_reply[select[0][0]]['start'])


@dp.message_handler(text="🇷🇺 Русский")
async def func_ru(message: types.Message):
  conn, cursor = TRANSLATE_USER_LANG.qui_sql()
  cursor.execute(
    "UPDATE translates_from_id SET language = ? WHERE user_id = ?",
    ('rus', int(message.chat.id)))
  conn.commit()
  dict_f = {'rus': 'Приветствуем вас на нашем цветочном магазине'}
  cursor.execute(
    f"SELECT language FROM translates_from_id WHERE user_id = {message.chat.id}"
  )
  select = cursor.fetchall()
  await message.answer(dict_f[select[0][0]],
                       reply_markup=keyboards_reply[select[0][0]]['start'])


async def HELP_COMMEND():
  a = {
    'uzb': '/start Bosh menyuga o\'tish uchun deb yozing',
    'rus': 'Введите /start, чтобы перейти в главное меню'
  }
  return a


@dp.message_handler(content_types=[
  types.ContentType.STICKER, types.ContentType.AUDIO,
  types.ContentType.STICKER, types.ContentType.UNKNOWN
])
async def unknown_message(msg: types.Message):
  try:
    conn, cursor = TRANSLATE_USER_LANG.qui_sql()

    cursor.execute(
      f"SELECT language FROM translates_from_id WHERE user_id = {msg.chat.id}")
    select = cursor.fetchall()

    message_text = text("Kechirasiz bot sizni tushunmadi," + '\U0001F914',
                        italic('\neslatib o\'tamiz,'), code('/help'),
                        'botni tushunishga yordam beradi')
    message_text1 = text("Я не знаю, что с этим делать" + '\U0001F914',
                         italic('\nЯ просто напомню,'), 'что есть',
                         code('команда'), '/help')
    dict_f = {'rus': message_text1, 'uzb': message_text}
    await msg.reply(dict_f[select[0][0]], parse_mode=types.ParseMode.MARKDOWN)
  except:
    await msg.reply(
      "🇺🇿 Botimiz yangilangaligi tufayli /start buyruqi orqali ishga tushuring\n\n🇷🇺 В связи с обновлением бота перезапустите бот коммандой /start"
    )


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
  conn, cursor = TRANSLATE_USER_LANG.qui_sql()
  try:
    cursor.execute(
      "INSERT INTO translates_from_id (user_id, language) VALUES (?,?)",
      (int(message.chat.id), 'uzb'))
  except:
    cursor.execute(
      "UPDATE translates_from_id SET language = ? WHERE user_id = ?",
      ('uzb', int(message.chat.id)))
  conn.commit()
  dict_f = {'uzb': '🇺🇿 Tilni tanlang:\n🇷🇺 Выберите язык:'}
  cursor.execute(
    f"SELECT language FROM translates_from_id WHERE user_id = {message.chat.id}"
  )
  select = cursor.fetchall()
  await message.answer(
    dict_f[select[0][0]],
    reply_markup=keyboards_reply[select[0][0]]['change_language_begin'])


@dp.message_handler(text=['🌹 Menyu', '🌹 Меню'])
async def MENU(message: types.Message):
  try:
    conn, cursor = TRANSLATE_USER_LANG.qui_sql()
    dict_f = {
      'uzb': 'Guldasta turini tanlang:',
      'rus': 'Выберите подходящую вам вид букета'
    }
    conn, cursor = TRANSLATE_USER_LANG.qui_sql()
    cursor.execute(
      f"SELECT language FROM translates_from_id WHERE user_id = {message.chat.id}"
    )
    select = cursor.fetchall()
    await message.answer(dict_f[select[0][0]],
                         reply_markup=keyboards_reply[select[0][0]]['Menu'])
  except:
    await message.reply(
      "🇺🇿 Botimiz yangilangaligi tufayli /start buyruqi orqali ishga tushuring\n\n🇷🇺 В связи с обновлением бота перезапустите бот коммандой /start"
    )


@dp.message_handler(
  Text([
    "🥡 Quti ko'rinishida", "💐 Guldasta ko'rinishida", '🥡 Букет в коробке',
    '💐 Цветы в букете'
  ]))
async def Type_flowers(message_karobka_buket: types.Message,
                       state: FSMContext):
  try:
    conn, cursor = TRANSLATE_USER_LANG.qui_sql()
    dict_f = {
      'uzb': 'Buyurtma miqdorini tanlang:',
      'rus': 'Выберите количество букетов:'
    }
    narx = inline_keyboards['uzb']['to_karobka'].inline_keyboard[1][
      0].callback_data.split(':')[-1]
    dict_f1 = {
      'uzb': f'Siz tanlagan gul: 🥡 Quti ko\'rinishida\nNarxi: {narx} so\'m',
      'rus':
      f'Букет который вы выбрали:🥡 Букет в коробке\n\nЦена: {narx} суммов'
    }
    dict_f2 = {
      'uzb': 'Quydagilardan birini tanlang:',
      'rus': 'Выберите одну из следующих:'
    }
    cursor.execute(
      f"SELECT language FROM translates_from_id WHERE user_id = {message_karobka_buket.chat.id}"
    )
    select = cursor.fetchall()

    if message_karobka_buket.text == '🥡 Quti ko\'rinishida' or message_karobka_buket.text == '🥡 Букет в коробке':
      await message_karobka_buket.answer(dict_f[select[0][0]],
                                         reply_markup=keyboards_reply)
      with open('imgs/Kоробкa.jpg', 'rb') as photo_:
        await bot.send_photo(
          message_karobka_buket.chat.id,
          photo=photo_,
          caption=f'{dict_f1[select[0][0]]}',
          reply_markup=inline_keyboards[select[0][0]]['to_karobka'])

    elif message_karobka_buket.text == "💐 Guldasta ko'rinishida" or message_karobka_buket.text == "💐 Цветы в букете":
      await message_karobka_buket.answer(
        dict_f2[select[0][0]],
        reply_markup=keyboards_reply[select[0][0]]['Buket'])
  except:
    await message_karobka_buket.reply(
      "🇺🇿 Botimiz yangilangaligi tufayli /start buyruqi orqali ishga tushuring\n\n🇷🇺 В связи с обновлением бота перезапустите бот коммандой /start"
    )


@dp.message_handler(text=['📭 Buyurtma xozir kerak', '📭 Доставка нужна сейчас'])
async def xozir(message_xozir: types.Message):
  try:
    conn, cursor = TRANSLATE_USER_LANG.qui_sql()
    dict_f = {
      'uzb':
      '90 daqiqa ichida yetkazib beriladi\nYetkazib berish uchun geolokatsiyangizni ulashing',
      'rus':
      'Доставка в течение 90 минут\nПоделитесь своей геолокацией для доставки'
    }
    cursor.execute(
      f"SELECT language FROM translates_from_id WHERE user_id = {message_xozir.chat.id}"
    )
    select = cursor.fetchall()
    await message_xozir.answer(
      dict_f[select[0][0]],
      reply_markup=keyboards_reply[select[0][0]]['location'])

    conn1 = sqlite3.connect('flower.db')
    cursor1 = conn1.cursor()
    cursor1.execute(
      "UPDATE shopping SET zakaz_qilingan_vaqti = ? WHERE user_id = ? AND is_fulfilled = ?",
      ('xozir', message_xozir.chat.id, 'No'))
    conn1.commit()
  except:
    await message_xozir.reply(
      "🇺🇿 Botimiz yangilangaligi tufayli /start buyruqi orqali ishga tushuring\n\n🇷🇺 В связи с обновлением бота перезапустите бот коммандой /start"
    )


need = str(datetime.now()).split('-')
current_time = uzb_now.strftime('%m.%d.%H')


@dp.message_handler(
  text=['⏱ Buyurtma vaqtini yozish', '⏱ Назначить время доставки'])
async def Buyurtma_vaqti(message_keying: types.Message, state: FSMContext):
  try:
    conn, cursor = TRANSLATE_USER_LANG.qui_sql()
    dict_f = {
      'uzb':
      f'Buyurtmangizni yetkazma vaqtini quyidagi formatda yozing: Oy-Sana-Soat: {current_time}',
      'rus':
      f'Введите время доставки вашего заказа в следующем формате: Месяц-Дата-Час: {current_time}'
    }
    cursor.execute(
      f"SELECT language FROM translates_from_id WHERE user_id = {message_keying.chat.id}"
    )
    select = cursor.fetchall()
    await message_keying.answer(
      dict_f[select[0][0]],
      reply_markup=keyboards_reply[select[0][0]]['cancel'])
    await States.Buyurtma_vaqt_state.start_vaqt.set()
  except:
    await message_keying.reply(
      "🇺🇿 Botimiz yangilangaligi tufayli /start buyruqi orqali ishga tushuring\n\n🇷🇺 В связи с обновлением бота перезапустите бот коммандой /start"
    )


@dp.message_handler(state=States.Buyurtma_vaqt_state.start_vaqt)
async def start_typing_time(message: types.Message, state: FSMContext):
  try:
    conn, cursor = TRANSLATE_USER_LANG.qui_sql()
    dict_f = {
      'uzb': 'Buyurtmani qabul qilish uchun sizga mos vaqtni tanlang',
      'rus': 'Выберите подходящее вам время для получения заказа'
    }
    dict_f1 = {
      'uzb':
      'Guldastaga buyurtma berish uchun bizga geolokatsiyangizni yuboring',
      'rus': 'Чтобы заказать букет отправьте нам вашу геолокацию'
    }
    dict_f2 = {
      'uzb':
      f'Siz kiritgan vaqt to\'g\'ri emas\n\nIltimos yetkazib bermoqchi bo\'lgan vaqtingizni\nQuyidagi formatda kiriting: Oy.Sana.Soat:{current_time}',
      'rus':
      f'Время которое вы ввели было неправильно введено\n\nПожалуйста введите времю для доставки\nПримено в таком формате: месяц.день.время: {current_time}'
    }
    cursor.execute(
      f"SELECT language FROM translates_from_id WHERE user_id = {message.chat.id}"
    )
    select = cursor.fetchall()

    if message.text == '⬅ Ortga' or message.text == '⬅ Назад':
      await message.answer(
        dict_f[select[0][0]],
        reply_markup=keyboards_reply[select[0][0]]['Buyurtmalar'])
      await state.finish()
    else:
      check_it_time = message.text.split('.')
      date_format = '%Y-%m-%d-%H'
      try:
        date_time_obj = datetime.strptime(
          str(datetime.now().year) + '-' + "-".join(message.text.split('.')),
          date_format)
        if len(check_it_time) == 3:
          await message.answer(
            dict_f1[select[0][0]],
            reply_markup=keyboards_reply[select[0][0]]['location'])
          base = sqlite3.connect('flower.db')
          curr = base.cursor()
          curr.execute(
            "UPDATE shopping SET zakaz_qilingan_vaqti = ? WHERE user_id = ? AND is_fulfilled = ?",
            (date_time_obj, message.chat.id, 'No'))
          base.commit()
          await state.finish()
        else:
          await message.answer(dict_f2[select[0][0]])
      except:
        await message.answer(dict_f2[select[0][0]])
  except:
    await message.reply(
      "🇺🇿 Botimiz yangilangaligi tufayli /start buyruqi orqali ishga tushuring\n\n🇷🇺 В связи с обновлением бота перезапустите бот коммандой /start"
    )


@dp.message_handler(commands=["help"])
async def healper_func(message: types.Message):
  try:
    conn, cursor = TRANSLATE_USER_LANG.qui_sql()
    cursor.execute(
      f"SELECT language FROM translates_from_id WHERE user_id = {message.chat.id}"
    )
    select = cursor.fetchall()
    await message.answer(text=HELP_COMMEND()[select[0][0]], parse_mode='HTML')
  except:
    await message.reply('Iltimos, botni qaytadan boshlang /start')


@dp.message_handler(text=['🗺 Mening manzillarim', '🗺 Мои адреса'])
async def Sended_Locations(message: types.Message, state: FSMContext):
  try:
    conn, cursor = TRANSLATE_USER_LANG.qui_sql()
    dict_f = {
      'uzb': "Bizda mavjud bo'lgan sizning manzillaringiz",
      'rus': 'Ваши адреса, которые у нас есть'
    }
    dict_f1 = {
      'uzb':
      'Xozircha bizda manzilingiz mavjud emas, geolokatsiyangizni ulashing',
      'rus':
      'В данный момент у вас не существует локаций, отправьте нам свою локацию'
    }
    dict_back = {'uzb': '⬅ Ortga', 'rus': '⬅ Назад'}
    cursor.execute(
      f"SELECT language FROM translates_from_id WHERE user_id = {message.chat.id}"
    )
    select = cursor.fetchall()

    conn1 = sqlite3.connect('flower.db')
    cursor1 = conn1.cursor()
    cursor1.execute(
      f"""SELECT location_name FROM location_ident WHERE user_id=={message.chat.id}"""
    )
    query = cursor1.fetchall()
    if query:
      my_loc = ReplyKeyboardMarkup(resize_keyboard=True)
      for i in set(query):
        my_loc.add(KeyboardButton(text=i[0]))
      my_loc.add(KeyboardButton(text=dict_back[select[0][0]]))
      try:
        await bot.edit_message_reply_markup(chat_id=message.chat.id,
                                            message_id=message.message_id,
                                            reply_markup=my_loc)
      except:
        await message.answer(dict_f[select[0][0]], reply_markup=my_loc)
      await States.State_Loc.your_loc.set()
    else:
      await message.answer(dict_f1[select[0][0]])
  except:
    await message.reply(
      "🇺🇿 Botimiz yangilangaligi tufayli /start buyruqi orqali ishga tushuring\n\n🇷🇺 В связи с обновлением бота перезапустите бот коммандой /start"
    )


@dp.message_handler(state=States.State_Loc.your_loc)
async def my_loc(message: types.Message, state: FSMContext):
  try:
    conn, cursor = TRANSLATE_USER_LANG.qui_sql()
    cursor.execute(
      f"SELECT language FROM translates_from_id WHERE user_id = {message.chat.id}"
    )
    select = cursor.fetchall()
    dict_f = {
      'uzb': 'Balki qayta urinib ko\'rarsiz',
      'rus': 'Может быть попробуете еще?'
    }
    dict_f1 = {
      'uzb': 'Aloqa uchun telefon raqamingizni ulashing',
      'rus': 'Поделитесь своим контактным телефоном'
    }
    dict_f2 = {
      'uzb': 'Bot sizni tushunmadi',
      'rus': 'Бот не совсем вас понял вас'
    }

    conn1 = sqlite3.connect('flower.db')
    cursor1 = conn1.cursor()
    cursor1.execute(
      f"""SELECT location_name FROM location_ident WHERE user_id=={message.chat.id}"""
    )
    query = cursor1.fetchall()
    cursor11 = conn1.cursor()
    cursor11.execute(
      f"SELECT location_name, location_latitude, location_longitude FROM location_ident WHERE user_id=={message.chat.id}"
    )
    query1 = cursor11.fetchall()
    if message.text == '⬅ Ortga' or message.text == '⬅ Назад':
      await message.answer(
        dict_f[select[0][0]],
        reply_markup=keyboards_reply[select[0][0]]['Buyurtmalar'])
    elif (message.text, ) in query and message.text:
      for i in query1:
        if message.text in i:
          base, curr = DL.qui_sql()
          curr.execute(
            "UPDATE shopping SET location_name = ?, location_latitude = ?, location_longitude = ? WHERE user_id = ? AND is_fulfilled = ?",
            (i[0], i[1], i[2], message.chat.id, 'No'))
          base.commit()
          await message.answer(
            dict_f1[select[0][0]],
            reply_markup=keyboards_reply[select[0][0]]['Contact'])
          break
    else:
      await message.answer(
        dict_f2[select[0][0]],
        reply_markup=keyboards_reply[select[0][0]]['location'])
    await state.finish()
  except:
    await message.reply(
      "🇺🇿 Botimiz yangilangaligi tufayli /start buyruqi orqali ishga tushuring\n\n🇷🇺 В связи с обновлением бота перезапустите бот коммандой /start"
    )


@dp.message_handler(content_types=types.ContentType.CONTACT)
async def handle_contact(message, state: FSMContext):
  try:

    phone_number = message.contact.phone_number if message.contact and message.contact.phone_number else None
    conn, cursor = TRANSLATE_USER_LANG.qui_sql()
    cursor.execute(
      f"SELECT language FROM translates_from_id WHERE user_id = {message.chat.id}"
    )
    select = cursor.fetchall()

    dict_f2 = {
      'uzb': "Sizning ma'lumotlaringiz to'g'ri yozilib olindimi?",
      'rus': 'Ваши данные правильно записанны?'
    }
    dict_f1 = {
      'uzb': 'Siz bilan bog\'lanishimiz uchun aloqa raqamingizni yuboring',
      'rus': 'Отправьте контактный номер для того чтобы мы связались с вами'
    }

    if phone_number:

      conn1 = sqlite3.connect('flower.db')
      cursor1 = conn1.cursor()
      cursor1.execute(
        "UPDATE shopping SET contact = ? WHERE user_id = ? AND is_fulfilled = ?",
        (message.contact.phone_number, message.chat.id, 'No'))
      conn1.commit()
      cursor1.execute(
        "SELECT * FROM shopping WHERE user_id = ? AND is_fulfilled = ?",
        (str(message.chat.id), 'No'))
      for i in cursor1.fetchall():

        df_xozir = {
          "uzb": {
            "Buyurtmangiz:": i[4],
            "Nechtaligi:": i[5],
            "Guldastangiz yozuvi:": i[7],
            "Telefon raqamingiz:": i[9],
            "Buyurtmangiz manzili:": i[12],
            "Buyurtma vaqti:": 'xozir'
          },
          "rus": {
            "Ваши заказы:":
            i[4].split("-")[0] if i[4] != "Qutili" else "Букет в коробке",
            "Количество:":
            i[5],
            "Надпись на букете:":
            i[7] if i[7] != 'yoziqsiz' else "Без надписи",
            "Ваш телефон номер:":
            i[9],
            "Место для доставки:":
            GoogleTranslator(source='uz', target='ru').translate(i[12]),
            "Время доставки:":
            'Сейчас' if i[10] == 'xozir' else i[10]
          }
        }

        df_now = pd.DataFrame(df_xozir[select[0][0]], index=[0]).transpose()
        df_now.columns = [" "]
        await message.answer(
          dict_f2[select[0][0]],
          reply_markup=keyboards_reply[select[0][0]]['last_agree'])
        await message.answer(df_now)

    else:
      await message.answer(dict_f1[select[0][0]])

    await States.Agree.yes_or_no.set()

  except:
    await message.reply(
      "🇺🇿 Botimiz yangilangaligi tufayli /start buyruqi orqali ishga tushuring\n\n🇷🇺 В связи с обновлением бота перезапустите бот коммандой /start"
    )


@dp.message_handler(text=["❌ Yo'q", "❌ Нет"], state=States.Agree.yes_or_no)
async def last_process_no(message: types.Message, state: FSMContext):
  conn, cursor = TRANSLATE_USER_LANG.qui_sql()
  cursor.execute(
    f"SELECT language FROM translates_from_id WHERE user_id = {message.chat.id}"
  )
  select = cursor.fetchall()
  try_again = {
    'uzb': 'Qaytadan buyurtma berishingizni so\'raymiz',
    'rus': 'Просим вас заказать заново'
  }

  try:
    await message.answer(try_again[select[0][0]],
                         reply_markup=keyboards_reply[select[0][0]]['start'])
    await state.finish()

  except:
    await message.reply(
      "🇺🇿 Botimiz yangilangaligi tufayli /start buyruqi orqali ishga tushuring\n\n🇷🇺 В связи с обновлением бота перезапустите бот коммандой /start"
    )


@dp.message_handler(text=['✅ Ha', '✅ Да'], state=States.Agree.yes_or_no)
async def last_process_yes(message: types.Message, state: FSMContext):
  conn, cursor = TRANSLATE_USER_LANG.qui_sql()
  cursor.execute(
    f"SELECT language FROM translates_from_id WHERE user_id = {message.chat.id}"
  )
  select = cursor.fetchall()
  dict_f = {
    'uzb':
    'Buyurtma qilganingiz uchun rahmat,\nYaqin orada siz bilan bog\'lanishadi',
    'rus': 'Спасибо за заказ, В скором времени с вами свяжутся'
  }
  try:
    db = sqlite3.connect("flower.db")
    cursor = db.cursor()
    cursor.execute(
      "UPDATE shopping SET is_fulfilled = ?, order_time = ? WHERE user_id = ? AND is_fulfilled = ?",
      ('Yes', current_time_tash, message.chat.id, 'No'))
    db.commit()
    db.close()
    await message.answer(dict_f[select[0][0]],
                         reply_markup=keyboards_reply[select[0][0]]['start'])
    await state.finish()
  except:
    await message.reply(
      "🇺🇿 Botimiz yangilangaligi tufayli /start buyruqi orqali ishga tushuring\n\n🇷🇺 В связи с обновлением бота перезапустите бот коммандой /start"
    )


@dp.message_handler(content_types=types.ContentType.LOCATION)
async def handle_location(message, state: FSMContext):
  try:
    conn, cursor = TRANSLATE_USER_LANG.qui_sql()
    cursor.execute(
      f"SELECT language FROM translates_from_id WHERE user_id = {message.chat.id}"
    )
    select = cursor.fetchall()

    geolocator = Nominatim(user_agent="my_bot")
    location_latitude = message.location.latitude if message.location and message.location.latitude else None
    location_longitude = message.location.longitude if location_latitude else None
    loc = geolocator.reverse(f"{location_latitude}, {location_longitude}",
                             timeout=10) if location_latitude else None
    location_name = ' '.join(
      loc.address.split(" ")[::-1][:1] +
      loc.address.split(" ")[::-1][2:]) if location_latitude else None
    try:
      translated_location = GoogleTranslator(
        source='uz', target='ru').translate(location_name)
    except:
      translated_location = location_name
    dict_f = {
      'uzb': f"Siz jo'natgan manzil:{location_name} To'grimi?",
      'rus': f'Ваш адрес доставки: {translated_location} Правильно?'
    }
    await message.answer(
      dict_f[select[0][0]],
      reply_markup=keyboards_reply[select[0][0]]['YES_OR_NO_FOR_LOCATION'])
    address = loc.raw['address']
    city_or_state = address.get('state', '') if address.get(
      'state', '') else address.get('city', '')
    async with state.proxy() as data:
      country = address.get('country', '')
      if country == 'Oʻzbekiston':
        if city_or_state == 'Toshkent':
          data['location'] = location_name
        else:
          data['location'] = 'ishlamadi'
      data['loc_name'] = location_name
      data['loc_long'] = location_longitude
      data['loc_lati'] = location_latitude
    await States.Check_it_your.yes_no.set()
  except:
    await message.reply(
      "🇺🇿 Botimiz yangilangaligi tufayli /start buyruqi orqali ishga tushuring\n\n🇷🇺 В связи с обновлением бота перезапустите бот коммандой /start"
    )


@dp.message_handler(state=States.Check_it_your.yes_no)
async def Maybe(msg, state: FSMContext):
  try:
    conn, cursor = TRANSLATE_USER_LANG.qui_sql()
    cursor.execute(
      f"SELECT language FROM translates_from_id WHERE user_id = {msg.chat.id}")
    select = cursor.fetchall()

    dict_f = {
      'uzb':
      'Buyurtmani qabul qilib oladigan joyingiz yozib olindi,\nAloqa uchun nomeringizni qoldiring: 📞',
      'rus':
      'Ваш адрес доставки успешно сохранен\nТеперь для связи с вами неообходимо ваш контакт: 📞'
    }
    dict_f1 = {
      'uzb':
      "Kechirasiz, sizning manzilingiz bo'yicha yetkazib berish xizmati mavjud emas, xozircha faqat Toshkent bo'yicha",
      'rus':
      'Извените в настоящее время у не существует доставки кроме города Ташкент'
    }
    dict_f2 = {
      'uzb': "📍 Yetkazib berish manzilingizni qayta yuboring",
      'rus': '📍 Пожалуйста отправьте адрес доставки заново'
    }
    dict_f3 = {
      'uzb': "📍 Yetkazib berish manzilingizni qayta yuboring",
      'rus': '📍 Отправьте адрес доставки заново'
    }
    dict_f4 = {'uzb': 'Bot buni tushunmadi', 'rus': 'Бот этого не понял'}

    async with state.proxy() as data:
      if msg.text == '✅ Ha' or msg.text == '✅ Да':
        if data['location'] != 'ishlamadi':
          await msg.answer(
            dict_f[select[0][0]],
            reply_markup=keyboards_reply[select[0][0]]['Contact'])
          await LOCATION_DB.ADD_DB(
            values=(msg.chat.id, data['loc_name'], data['loc_lati'],
                    data['loc_long']),
            str_v=
            '(user_id, location_name, location_latitude, location_longitude)',
            how_many_values='(?,?,?,?)')
          base, curr = DL.qui_sql()
          curr.execute(
            "UPDATE shopping SET location_name = ?, location_latitude = ?, location_longitude = ? WHERE user_id = ? AND is_fulfilled = ?",
            (data['loc_name'], data['loc_lati'], data['loc_long'], msg.chat.id,
             'No'))
          base.commit()
          base.close()
        else:
          await msg.answer(
            dict_f1[select[0][0]],
            reply_markup=keyboards_reply[select[0][0]]['location'])
      elif msg.text == '❌ Yo\'q' or msg.text == '❌ Нет':
        await msg.answer(
          dict_f2[select[0][0]],
          reply_markup=keyboards_reply[select[0][0]]['location'])
      elif msg.text == '⬅ Ortga' or msg.text == '⬅ Назад':
        await msg.answer(dict_f3[select[0][0]],
                         reply_markup=keyboards_reply[select[0][0]]['Keyin'])
      else:
        await msg.answer(dict_f4[select[0][0]],
                         reply_markup=keyboards_reply[select[0][0]]['Keyin'])
      await state.finish()
  except:
    await msg.reply(
      "🇺🇿 Botimiz yangilangaligi tufayli /start buyruqi orqali ishga tushuring\n\n🇷🇺 В связи с обновлением бота перезапустите бот коммандой /start"
    )


@dp.message_handler(text=['⚙️ Sozlamalar', '⚙️ Настройки'])
async def settings(message: types.Message):
  try:
    conn, cursor = TRANSLATE_USER_LANG.qui_sql()
    cursor.execute(
      f"SELECT language FROM translates_from_id WHERE user_id = {message.chat.id}"
    )
    select = cursor.fetchall()
    dict_f = {'uzb': 'Harakatni tanlang', 'rus': 'Выберите действие:'}
    await message.answer(
      dict_f[select[0][0]],
      reply_markup=keyboards_reply[select[0][0]]['sozlamalar'])
    await States.Translate.uzb_ru.set()
  except:
    await message.reply(
      "🇺🇿 Botimiz yangilangaligi tufayli /start buyruqi orqali ishga tushuring\n\n🇷🇺 В связи с обновлением бота перезапустите бот коммандой /start"
    )


@dp.message_handler(state=States.Translate.uzb_ru)
async def choose_language(message: types.Message, state: FSMContext):
  try:
    conn, cursor = TRANSLATE_USER_LANG.qui_sql()
    cursor.execute(
      f"SELECT language FROM translates_from_id WHERE user_id = {message.chat.id}"
    )
    select = cursor.fetchall()
    dict_f = {'uzb': 'Quyidagilardan birini tanlang', 'rus': 'Выберите язык:'}
    dict_f1 = {'uzb': 'Tilni tanlang', 'rus': 'Выберите язык'}

    if message.text == '⬅ Ortga' or message.text == '⬅ Назад':
      await message.answer(dict_f[select[0][0]],
                           reply_markup=keyboards_reply[select[0][0]]['start'])
    else:
      await message.answer(
        dict_f1[select[0][0]],
        reply_markup=keyboards_reply[select[0][0]]['change_language'])
    await state.finish()
  except:
    await message.reply(
      "🇺🇿 Botimiz yangilangaligi tufayli /start buyruqi orqali ishga tushuring\n\n🇷🇺 В связи с обновлением бота перезапустите бот коммандой /start"
    )
