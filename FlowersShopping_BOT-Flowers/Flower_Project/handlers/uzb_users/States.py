from aiogram.dispatcher.filters.state import State, StatesGroup


class State_Loc(StatesGroup):
  your_loc = State()


class State_tovar(StatesGroup):
  choose = State()


class Buyurtma_vaqt_state(StatesGroup):
  start_vaqt = State()


class States_(StatesGroup):
  CHOOSING_OPTION = State()
  STYLE_NAME = State()
  CONFIRMATION = State()


class Check_it_your(StatesGroup):
  yes_no = State()


class Authentication(StatesGroup):
  password = State()


class CHANGE_Karobka(StatesGroup):
  narxi_korish = State()


class Change_Buket(StatesGroup):
  to_narx = State()
  narxi_korish1 = State()


class Comments_(StatesGroup):
  comments = State()


class Translate(StatesGroup):
  uzb_ru = State()


class Agree(StatesGroup):
  yes_or_no = State()


class Advertisement(
    StatesGroup
):  # Here i created for fsm_context to admin sending advertisement for each user
  adver = State()


class Change_pic(StatesGroup):
  show_picture = State()
  change_picture = State()
