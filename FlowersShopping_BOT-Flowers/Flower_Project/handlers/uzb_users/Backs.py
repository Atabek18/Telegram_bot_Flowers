from aiogram import types
from keyboards.reply.choise_reply_buttons import keyboards_reply
from loader import dp
from handlers.uzb_users.purchase1 import TRANSLATE_USER_LANG


@dp.message_handler(text=['⬅ Ortga', '⬅ Назад'])
async def Back(message: types.Message):

  try:
    conn, cursor = TRANSLATE_USER_LANG.qui_sql()
    dict_f = {
      'uzb': 'Quyidagilardan birini tanlang',
      'rus': 'Выберите одну из следующих:'
    }
    cursor.execute(
      f"SELECT language FROM translates_from_id WHERE user_id = {message.chat.id}"
    )
    select = cursor.fetchall()
    await message.answer(dict_f.get(select[0][0], dict_f['uzb']),
                         reply_markup=keyboards_reply.get(
                           select[0][0], dict_f['uzb'])['start'])
  except:
    await message.reply(
      "🇺🇿 Botimiz yangilangaligi tufayli /start buyruqi orqali ishga tushuring\n\n🇷🇺 В связи с обновлением бота перезапустите бот коммандой /start"
    )


@dp.message_handler(text=['⬅ Geolokatsiya qaytish', '⬅ Назад в геолокацию'])
async def _back_location(message: types.Message):
  try:
    conn, cursor = TRANSLATE_USER_LANG.qui_sql()
    dict_f = {
      'uzb':
      '📍 Geolokatsiyani yuboring yoki yetkazib berish manzilini tanlang',
      'rus': '📍 Отправьте геолокацию место доставки'
    }
    cursor.execute(
      f"SELECT language FROM translates_from_id WHERE user_id = {message.chat.id}"
    )
    select = cursor.fetchall()
    await message.answer(dict_f.get(select[0][0], dict_f['uzb']),
                         reply_markup=keyboards_reply.get(
                           select[0][0], dict_f['uzb'])['location'])
  except:
    await message.reply(
      "🇺🇿 Botimiz yangilangaligi tufayli /start buyruqi orqali ishga tushuring\n\n🇷🇺 В связи с обновлением бота перезапустите бот коммандой /start"
    )


@dp.message_handler(text=['⬅ Buketlarga qaytish', '⬅ Вернуться к букетам'])
async def Back_to_Buket(message: types.Message):
  try:
    conn, cursor = TRANSLATE_USER_LANG.qui_sql()
    dict_f = {
      'uzb': 'Mana buketlar turi, o\'zingiz xohlagan buket turini tanlang',
      'rus': 'Выберите букеты:'
    }
    cursor.execute(
      f"SELECT language FROM translates_from_id WHERE user_id = {message.chat.id}"
    )
    select = cursor.fetchall()
    await message.answer(dict_f.get(select[0][0], dict_f['uzb']),
                         reply_markup=keyboards_reply.get(
                           select[0][0], dict_f['uzb'])['Buket'])
  except:
    await message.reply(
      "🇺🇿 Botimiz yangilangaligi tufayli /start buyruqi orqali ishga tushuring\n\n🇷🇺 В связи с обновлением бота перезапустите бот коммандой /start"
    )


@dp.message_handler(text=['⬅ Menyuga qaytish', '⬅ Назад в меню'])
async def Back_to_Menu(message: types.Message):
  try:
    conn, cursor = TRANSLATE_USER_LANG.qui_sql()
    dict_f = {
      'uzb': 'Quyidagilardan birini tanlang',
      'rus': 'Выберите одну из следующих:'
    }
    cursor.execute(
      f"SELECT language FROM translates_from_id WHERE user_id = {message.chat.id}"
    )
    select = cursor.fetchall()
    await message.answer(dict_f.get(select[0][0], dict_f['uzb']),
                         reply_markup=keyboards_reply.get(
                           select[0][0], dict_f['uzb'])['Menu'])
  except:
    await message.reply(
      "🇺🇿 Botimiz yangilangaligi tufayli /start buyruqi orqali ishga tushuring\n\n🇷🇺 В связи с обновлением бота перезапустите бот коммандой /start"
    )


@dp.message_handler(
  text=['⬅ Ortga vaqtni belgilashga', '⬅ Назад назначить время'])
async def buyurma_qaytish(message: types.Message):
  try:
    conn, cursor = TRANSLATE_USER_LANG.qui_sql()
    dict_f = {
      'uzb': 'Quyidagilardan birini tanlang',
      'rus': 'Выберите одну из следующих:'
    }
    cursor.execute(
      f"SELECT language FROM translates_from_id WHERE user_id = {message.chat.id}"
    )
    select = cursor.fetchall()
    await message.answer(dict_f.get(select[0][0], dict_f['uzb']),
                         reply_markup=keyboards_reply.get(
                           select[0][0], dict_f['uzb'])['Buyurtmalar'])
  except:
    await message.reply(
      "🇺🇿 Botimiz yangilangaligi tufayli /start buyruqi orqali ishga tushuring\n\n🇷🇺 В связи с обновлением бота перезапустите бот коммандой /start"
    )
