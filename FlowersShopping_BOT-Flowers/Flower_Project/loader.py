import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import os

load_dotenv()

PROXY_URL = "http://proxy.server:3128"
bot = Bot(token=os.environ.get('TOKEN'))


async def my_middleware(update, dispatcher, next_handler):
  await next_handler(update)


dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(
  format=
  u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
  level=logging.INFO,
)
