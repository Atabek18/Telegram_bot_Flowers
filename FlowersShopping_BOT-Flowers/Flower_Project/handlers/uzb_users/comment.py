from keyboards.reply.choise_reply_buttons import keyboards_reply
from database.sqlite_db_user import CREATE_DB
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from handlers.uzb_users import States
from aiogram.types import Message
from loader import dp
from handlers.uzb_users.purchase1 import TRANSLATE_USER_LANG
import pytz
from datetime import datetime

uzb_tz = pytz.timezone('Asia/Tashkent')
utc_now = datetime.utcnow()
uzb_now = utc_now.astimezone(uzb_tz)

va_comments = "(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT NOT NULL, comments TEXT NOT NULL, yozgan_vaqti TEXT NOT NULL)"
creat_db = CREATE_DB(db_file_name='flower.db', tabel_name='comment')
creat_db.ST_DB(values=va_comments)


@dp.message_handler(text=['✍️ Прокомментировать', '✍️ Fikr Bildirish'])
async def commenting(message: Message, state: FSMContext):
  try:
    conn, cursor = TRANSLATE_USER_LANG.qui_sql()
    dict_f = {
      'uzb':
      'Botimiz haqida fikringiz bo\'lsa yoki kamchiliklari bo\'lsa yozib qoldiring biz to\'g\'irlashga harakat qilamiz',
      'rus':
      'Напишите свои мысли о нашем боте или недостатки бота мы постараемся исправить'
    }
    cursor.execute(
      f"SELECT language FROM translates_from_id WHERE user_id = {message.chat.id}"
    )
    select = cursor.fetchall()
    await message.answer(
      dict_f[select[0][0]],
      reply_markup=keyboards_reply[select[0][0]]['Back_for_Ha'])
    await States.Comments_.comments.set()
  except:
    await message.reply(
      "🇺🇿 Botimiz yangilangaligi tufayli /start buyruqi orqali ishga tushuring\n\n🇷🇺 В связи с обновлением бота перезапустите бот коммандой /start"
    )


@dp.message_handler(state=States.Comments_.comments)
async def write_comment(message: Message, state: FSMContext):
  try:
    conn, cursor = TRANSLATE_USER_LANG.qui_sql()
    dict_f = {'uzb': 'Siz asosiy menyuga qaytiz', 'rus': 'Вы в главном меню'}
    dict_f1 = {
      'uzb':
      'Fikr bildirganingiz uchun raxmat, biz uchun har bir sizning fikringiz muhum',
      'rus': ' Спасибо что оценили нашу услугу, Ваше мнение очень важна нам'
    }
    cursor.execute(
      f"SELECT language FROM translates_from_id WHERE user_id = {message.chat.id}"
    )
    select = cursor.fetchall()

    user_id = message.chat.id if message.chat.id else None
    if message.text == '⬅ Ortga' or message.text == '⬅ Назад':
      await message.answer(dict_f[select[0][0]],
                           reply_markup=keyboards_reply[select[0][0]]['start'])
    else:
      await creat_db.ADD_DB(values=(user_id, message.text, str(uzb_now)),
                            str_v="(user_id, comments, yozgan_vaqti)",
                            how_many_values="(?, ?, ?)")
      await message.answer(dict_f1[select[0][0]],
                           reply_markup=keyboards_reply[select[0][0]]['start'])
    await state.finish()
  except:
    await message.reply(
      "🇺🇿 Botimiz yangilangaligi tufayli /start buyruqi orqali ishga tushuring\n\n🇷🇺 В связи с обновлением бота перезапустите бот коммандой /start"
    )
