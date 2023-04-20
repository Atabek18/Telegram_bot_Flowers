from keyboards.reply.choise_reply_buttons import keyboards_reply
from keyboards.inline.choice_inline_buttons import inline_keyboards
from keyboards.inline.callback_datas import savat_callback, Delivary
from aiogram.types import CallbackQuery, Message
from database.sqlite_db_user import CREATE_DB
from aiogram.dispatcher import FSMContext
from handlers.uzb_users import States
from loader import dp, bot
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3
from handlers.uzb_users.each_buket import get_data

va_delivary = """(id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT, user_fname TEXT, user_lname TEXT,
        buket TEXT, how_many INTEGER, how_much_it TEXT,
        style TEXT,is_fulfilled TEXT,contact TEXT, zakaz_qilingan_vaqti TEXT, order_time TIMESTAMP,
        location_name TEXT, location_longitude TEXT, location_latitude TEXT)"""
DL = CREATE_DB(db_file_name='flower.db', tabel_name='shopping')
DL.ST_DB(values=va_delivary)


@dp.callback_query_handler(Delivary.filter(item_name='Delivary'))
async def buy_chooses(call: CallbackQuery, callback_data: dict,
                      state: FSMContext):
  try:
    t_conn = sqlite3.connect('flower.db')
    t_curr = t_conn.cursor()
    t_curr.execute(
      f"SELECT language FROM translates_from_id WHERE user_id = {call.message.chat.id}"
    )
    select = t_curr.fetchall()
    translate_dict = {
      'rus': 'Хотите чтобы была надпись в букете?',
      'uzb': 'Guldastaning ustida yozuv bo\'lisni xohlaysizmi?'
    }
    callback_data['how_many'] = call.message.reply_markup.inline_keyboard[0][
      1].text
    # logging.info( f'User_id: {call.message.chat.id}, Chat_id: {call.message.message_id},   {callback_data=}')
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    if callback_data['which_item'] == 'Qutili':
      open_p = 'Kоробкa'
    else:
      open_p = callback_data["which_item"].split('-')[0] + 'tali'
    async with state.proxy() as data:
      if callback_data['which_item'] == 'Qutili' or callback_data[
          'which_item'] == 'Kоробкa':
        data['which_item'] = 'Qutili'
      else:
        data['which_item'] = callback_data['which_item'].split(
          '-')[0] + '-tali'

    try:
      with open(f'imgs/{open_p}.jpg', 'rb') as photo_:
        await bot.send_photo(
          chat_id=call.message.chat.id,
          photo=photo_,
          caption=translate_dict[select[0][0]],
          reply_markup=keyboards_reply[select[0][0]]['yes_or_no'])
    except:
      with open('imgs/Kоробкa.jpg', 'rb') as photo_:
        await bot.send_photo(
          chat_id=call.message.chat.id,
          photo=photo_,
          caption=translate_dict[select[0][0]],
          reply_markup=keyboards_reply[select[0][0]]['yes_or_no'])

    v = '(user_id, user_fname, user_lname, buket, how_many, how_much_it, style, is_fulfilled, contact, zakaz_qilingan_vaqti, order_time)'
    async with state.proxy() as data:
      values = (call.message.chat.id, call.message.chat.first_name,
                call.message.chat.last_name, data['which_item'],
                int(callback_data['how_many']), callback_data['how_much_it'],
                'yoziqsiz', 'No', None, None, None)

    await DL.ADD_DB(values=values,
                    str_v=v,
                    how_many_values='(?,?,?,?,?,?,?,?,?,?,?)')
    await States.States_.CHOOSING_OPTION.set()
  except:
    await bot.send_message(
      call.message.chat.id,
      "🇺🇿 Botimiz yangilangaligi tufayli /start buyruqi orqali ishga tushuring\n\n🇷🇺 В связи с обновлением бота перезапустите бот коммандой /start"
    )


@dp.message_handler(text=["❌ Yo'q", '❌ Нет'],
                    state=States.States_.CHOOSING_OPTION)
async def process_cancel_style(message: Message, state: FSMContext):
  try:
    t_conn = sqlite3.connect('flower.db')
    t_curr = t_conn.cursor()
    t_curr.execute(
      f"SELECT language FROM translates_from_id WHERE user_id = {message.chat.id}"
    )
    select = t_curr.fetchall()
    translate_dict = {
      'rus': 'Выбранный тип упаковки добавлен в корзину',
      'uzb': "Siz tanlagan guldasta savatga qo'shildi"
    }
    async with state.proxy() as data:
      if data['which_item'] == 'Qutili':
        await message.answer(
          translate_dict[select[0][0]],
          reply_markup=keyboards_reply[select[0][0]]['Karobka'])
      else:
        await message.answer(
          translate_dict[select[0][0]],
          reply_markup=keyboards_reply[select[0][0]]['Buket'])
    await state.finish()
  except:
    await message.reply(
      "🇺🇿 Botimiz yangilangaligi tufayli /start buyruqi orqali ishga tushuring\n\n🇷🇺 В связи с обновлением бота перезапустите бот коммандой /start"
    )


@dp.message_handler(text=['✅ Ha', '✅ Да'],
                    state=States.States_.CHOOSING_OPTION)
async def process_make_style(message: Message, state: FSMContext):
  try:
    t_conn = sqlite3.connect('flower.db')
    t_curr = t_conn.cursor()
    t_curr.execute(
      f"SELECT language FROM translates_from_id WHERE user_id = {message.chat.id}"
    )
    select = t_curr.fetchall()
    translate_dict = {
      'rus':
      'Напишите слово которое хотели бы видеть в букете',
      'uzb':
      'Guldasta ustiga yozuv yozilishi uchun birorta so\'z yozib qoldiring\nNamuna: Ona'
    }

    await States.States_.STYLE_NAME.set()
    await message.answer(
      translate_dict[select[0][0]],
      reply_markup=keyboards_reply[select[0][0]]['Back_for_Ha'])
  except:
    await message.reply(
      "🇺🇿 Botimiz yangilangaligi tufayli /start buyruqi orqali ishga tushuring\n\n🇷🇺 В связи с обновлением бота перезапустите бот коммандой /start"
    )


@dp.message_handler(state=States.States_.STYLE_NAME)
async def process_write(message: Message, state: FSMContext):
  try:
    t_conn = sqlite3.connect('flower.db')
    t_curr = t_conn.cursor()
    t_curr.execute(
      f"SELECT language FROM translates_from_id WHERE user_id = {message.chat.id}"
    )
    select = t_curr.fetchall()
    translate_dict = {'uzb': 'Siz ortga qaytingiz', 'rus': 'Вы вернулись'}
    translate_dict1 = {
      'uzb':
      'Yozgan yozuvingizni guldastaning ustiga yozilsinmi?',
      'rus':
      'Подтверждаете выше написанный текст чтобы был надписью букета которого вы выбрали?'
    }
    async with state.proxy() as data:
      if (message.text == '⬅ Ortga' and data['which_item'] == 'Qutili') or (
          message.text == '⬅ Назад' and data['which_item'] == 'Qutili'):
        await message.answer(
          translate_dict[select[0][0]],
          reply_markup=keyboards_reply[select[0][0]]['Karobka'])
        await state.finish()
      elif message.text == '⬅ Ortga' or message.text == '⬅ Назад':
        await message.answer(
          translate_dict[select[0][0]],
          reply_markup=keyboards_reply[select[0][0]]['Buket'])
        await state.finish()
      else:
        data['style'] = message.text
        await message.answer(
          translate_dict1[select[0][0]],
          reply_markup=inline_keyboards[select[0][0]]['confirmation'])
        await States.States_.CONFIRMATION.set()
  except:
    await message.reply(
      "🇺🇿 Botimiz yangilangaligi tufayli /start buyruqi orqali ishga tushuring\n\n🇷🇺 В связи с обновлением бота перезапустите бот коммандой /start"
    )


@dp.callback_query_handler(text='confirm', state=States.States_.CONFIRMATION)
async def confirm_style(call: CallbackQuery, state: FSMContext):
  try:
    t_conn = sqlite3.connect('flower.db')
    t_curr = t_conn.cursor()
    t_curr.execute(
      f"SELECT language FROM translates_from_id WHERE user_id = {str(call.message.chat.id)}"
    )
    select = t_curr.fetchall()
    translate_dict1 = {
      'uzb': 'Yozganningizni qabul qildik',
      'rus': 'Ваша надпись принята'
    }
    async with state.proxy() as data:
      if data['which_item'] == 'Qutili':
        conn = sqlite3.connect('flower.db')
        cursor = conn.cursor()
        cursor.execute(
          "SELECT id FROM shopping WHERE user_id = ? AND id ORDER BY id DESC LIMIT 1",
          (str(call.message.chat.id), ))
        last_id = cursor.fetchall()[0]
        cursor.execute(
          "UPDATE shopping SET style = ? WHERE user_id = ? AND buket = ? AND id = ?",
          (data['style'], call.message.chat.id, data['which_item'],
           last_id[0]))
        conn.commit()
        await bot.send_message(
          chat_id=call.message.chat.id,
          text=translate_dict1[select[0][0]],
          reply_markup=keyboards_reply[select[0][0]]['Karobka'])
      else:
        conn = sqlite3.connect('flower.db')
        cursor = conn.cursor()
        cursor.execute(
          "SELECT id FROM shopping WHERE user_id = ? AND id ORDER BY id DESC LIMIT 1",
          (str(call.message.chat.id), ))
        last_id = cursor.fetchall()[0]
        cursor.execute(
          "UPDATE shopping SET style = ? WHERE user_id = ? AND buket = ? AND id = ?",
          (data['style'], call.message.chat.id, data['which_item'],
           last_id[0]))
        conn.commit()
        conn.close()
        await bot.send_message(
          chat_id=call.message.chat.id,
          text=translate_dict1[select[0][0]],
          reply_markup=keyboards_reply[select[0][0]]['Buket'])

      await bot.delete_message(chat_id=call.message.chat.id,
                               message_id=call.message.message_id)
      await state.finish()
  except:
    await bot.send_message(
      chat_id=call.message.chat.id,
      text=
      "🇺🇿 Botimiz yangilangaligi tufayli /start buyruqi orqali ishga tushuring\n\n🇷🇺 В связи с обновлением бота перезапустите бот коммандой /start"
    )


@dp.callback_query_handler(text='cancel', state=States.States_.CONFIRMATION)
async def reject_style(call: CallbackQuery, state: FSMContext):
  try:
    t_conn = sqlite3.connect('flower.db')
    t_curr = t_conn.cursor()
    t_curr.execute(
      f"SELECT language FROM translates_from_id WHERE user_id = {call.message.chat.id}"
    )
    select = t_curr.fetchall()
    translate_dict = {
      'uzb': 'Siz yozganlaringizni bekor qildingiz',
      'rus': 'Вы отменили то, что написали'
    }
    async with state.proxy() as data:
      if data['which_item'] == 'Qutili':
        await bot.send_message(
          chat_id=call.message.chat.id,
          text=translate_dict[select[0][0]],
          reply_markup=keyboards_reply[select[0][0]]['Karobka'])
      else:
        await bot.send_message(
          chat_id=call.message.chat.id,
          text=translate_dict[select[0][0]],
          reply_markup=keyboards_reply[select[0][0]]['Buket'])
    await bot.delete_message(chat_id=call.message.chat.id,
                             message_id=call.message.message_id)
    await state.finish()

  except:
    await bot.send_message(
      chat_id=call.message.chat.id,
      text=
      "🇺🇿 Botimiz yangilangaligi tufayli /start buyruqi orqali ishga tushuring\n\n🇷🇺 В связи с обновлением бота перезапустите бот коммандой /start"
    )


@dp.callback_query_handler(lambda query: query.data.startswith('del'))
async def del_each_delivary(call: CallbackQuery):
  try:
    t_conn = sqlite3.connect('flower.db')
    t_curr = t_conn.cursor()
    t_curr.execute(
      f"SELECT language FROM translates_from_id WHERE user_id = {call.message.chat.id}"
    )
    select = t_curr.fetchall()
    translate_dict = {
      'uzb': 'Kechirasiz, nimadir noto‘g‘ri ketdi, qayta urinib ko‘ring',
      'rus': 'Извините что-то пошло не так, попробуйте еще раз'
    }
    translate_dict1 = {
      'uzb': 'Sizning savatingiz boshadi',
      'rus': 'Ваша корзина пуста'
    }
    data = call.data
    t = data.split('del')[1].split('-')[0] + '-tali' if data.split(
      'del')[1] != 'Qutili' else 'Qutili'
    try:
      conn = sqlite3.connect('flower.db')
      cursor = conn.cursor()
      cursor.execute(
        "DELETE FROM shopping WHERE buket = ? AND user_id = ? AND is_fulfilled = ?",
        (t, str(call.message.chat.id), "No"))
      conn.commit()
      cursor.execute(
        "SELECT how_many, buket, how_much_it FROM shopping WHERE user_id=? AND is_fulfilled=?",
        (call.message.chat.id, 'No'))
      query = cursor.fetchall()
      set_select = set([i[1] for i in query])

      if select[0][0] == 'uzb' and set_select:
        group, total_narx_, yol_haqqi, total = get_data(query)
        key = [
          types.InlineKeyboardButton(text='❌' + i,
                                     callback_data='del{}'.format(i))
          for i in set_select
        ]
        new_but = InlineKeyboardMarkup(
          inline_keyboard=[[
            InlineKeyboardButton(text='🚖 Buyurtma Berish',
                                 callback_data='open_delivery',
                                 cache_time=1)
          ],
                           [
                             InlineKeyboardButton(text='⬅ Ortga',
                                                  callback_data='close'),
                             InlineKeyboardButton(text='🗑 Savatni tozalash',
                                                  callback_data='clear_to_')
                           ]]).add(*key)
        await bot.edit_message_text(
          chat_id=call.message.chat.id,
          message_id=call.message.message_id,
          text=
          f'📥 Savat ichida:\n{group.to_string(index=False, header=False)}\nTovarlar: {str(total_narx_)} sum\nYo\'l haqqi: {yol_haqqi}\nJami: {total} sum',
          reply_markup=new_but)
      elif set_select and select[0][0] == 'rus':
        group, total_narx_, yol_haqqi, total = get_data(query)
        uzb = [
          '101-tali', '201-tali', '301-tali', '401-tali', '501-tali',
          '601-tali', '701-tali', '1001-tali', 'Qutili'
        ]
        rus = [
          '101', '201', '301', '401', '501', '601', '701', '1001', 'Kоробкa'
        ]
        get_it = dict(zip(uzb, rus))
        key = [
          types.InlineKeyboardButton(text='❌' + get_it[i],
                                     callback_data='del{}'.format(i))
          for i in set_select
        ]
        new_but = InlineKeyboardMarkup(
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
        await bot.edit_message_text(
          chat_id=call.message.chat.id,
          message_id=call.message.message_id,
          text=
          f'📥 Внутри корзины имеется:\n{group.to_string(index=False, header=False)}\nтоваров: {str(total_narx_)} сумма\nЗа заказ: {yol_haqqi}\n Общая сумма: {total} суммов',
          reply_markup=new_but)

      else:
        await bot.send_message(chat_id=call.message.chat.id,
                               text=translate_dict1[select[0][0]])
        await bot.delete_message(chat_id=call.message.chat.id,
                                 message_id=call.message.message_id)
    except:
      await call.message.answer(text=translate_dict[select[0][0]])
      await bot.delete_message(chat_id=call.message.chat.id,
                               message_id=call.message.message_id)
  except:
    await bot.send_message(
      call.message.chat.id,
      "🇺🇿 Botimiz yangilangaligi tufayli /start buyruqi orqali ishga tushuring\n\n🇷🇺 В связи с обновлением бота перезапустите бот коммандой /start"
    )


@dp.callback_query_handler(savat_callback.filter(item_name='minus'))
async def sub_the_choise(call: CallbackQuery, callback_data: dict):

  await call.answer(cache_time=1)
  minus = -1
  text = int(call.message.reply_markup.inline_keyboard[0][1].text) + minus
  if text > 0:
    call.message.reply_markup.inline_keyboard[0][1].text = str(text)
    temp = types.InlineKeyboardMarkup(
      inline_keyboard=call.message.reply_markup.inline_keyboard)
    await bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                        message_id=call.message.message_id,
                                        reply_markup=temp)


@dp.callback_query_handler(savat_callback.filter(item_name='sum'))
async def how_many_choises(call: CallbackQuery, callback_data: dict):
  try:
    t_conn = sqlite3.connect('flower.db')
    t_curr = t_conn.cursor()
    t_curr.execute(
      f"SELECT language FROM translates_from_id WHERE user_id = {call.message.chat.id}"
    )
    select = t_curr.fetchall()
    translate_dict = {'uzb': 'ta', 'rus': 'штук'}
    await call.answer(translate_dict[select[0][0]])
  except:
    await bot.send_message(
      call.message.chat.id,
      "🇺🇿 Botimiz yangilangaligi tufayli /start buyruqi orqali ishga tushuring\n\n🇷🇺 В связи с обновлением бота перезапустите бот коммандой /start"
    )


@dp.callback_query_handler(savat_callback.filter(item_name='plus'))
async def add_the_choise(call: CallbackQuery, callback_data: dict):
  try:
    t_conn = sqlite3.connect('flower.db')
    t_curr = t_conn.cursor()
    t_curr.execute(
      f"SELECT language FROM translates_from_id WHERE user_id = {call.message.chat.id}"
    )
    select = t_curr.fetchall()
    translate_dict = {
      'uzb':
      'Iltimos, kutib turing bu bir necha daqiqa vaqt olishi mumkin, sabringiz uchun raxmat',
      'rus':
      'Пожайлуйста подождите, это может занять несколько минут, благодарим за тепрение'
    }

    await call.answer(cache_time=1)
    minus = 1
    text = int(call.message.reply_markup.inline_keyboard[0][1].text)
    call.message.reply_markup.inline_keyboard[0][1].text = str(text + minus)
    temp = types.InlineKeyboardMarkup(
      inline_keyboard=call.message.reply_markup.inline_keyboard)
    try:
      await bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                          message_id=call.message.message_id,
                                          reply_markup=temp)
    except:
      await call.answer(translate_dict[select[0][0]])
  except:
    await bot.send_message(
      call.message.chat.id,
      "🇺🇿 Botimiz yangilangaligi tufayli /start buyruqi orqali ishga tushuring\n\n🇷🇺 В связи с обновлением бота перезапустите бот коммандой /start"
    )


@dp.callback_query_handler(text='close')
async def back_for_inline(call: CallbackQuery):
  await bot.delete_message(chat_id=call.message.chat.id,
                           message_id=call.message.message_id)


@dp.callback_query_handler(text='clear_to_')
async def clear_for_inline(call: CallbackQuery):
  conn = sqlite3.connect('flower.db')
  cursor = conn.cursor()
  cursor.execute("DELETE FROM shopping WHERE user_id = ? AND is_fulfilled = ?",
                 (call.message.chat.id, 'No'))
  conn.commit()
  conn.close()
  await bot.delete_message(chat_id=call.message.chat.id,
                           message_id=call.message.message_id)


@dp.callback_query_handler(text='open_delivery')
async def FORWARD(call: CallbackQuery):
  try:
    t_conn = sqlite3.connect('flower.db')
    t_curr = t_conn.cursor()
    t_curr.execute(
      f"SELECT language FROM translates_from_id WHERE user_id = {call.message.chat.id}"
    )
    select = t_curr.fetchall()
    translate_dict = {
      'uzb': 'Buyurtma berish uchun qulay vaqtni tanlang:',
      'rus': 'Выберите вам удобное время для принятия заказа:'
    }
    await bot.delete_message(chat_id=call.message.chat.id,
                             message_id=call.message.message_id)
    await call.message.answer(
      text=translate_dict[select[0][0]],
      reply_markup=keyboards_reply[select[0][0]]['Buyurtmalar'])
  except:
    await bot.send_message(
      call.message.chat.id,
      "🇺🇿 Botimiz yangilangaligi tufayli /start buyruqi orqali ishga tushuring\n\n🇷🇺 В связи с обновлением бота перезапустите бот коммандой /start"
    )
