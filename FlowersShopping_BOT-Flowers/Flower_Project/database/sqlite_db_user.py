import sqlite3
from aiogram import types
from loader import dp


class CREATE_DB:

  def __init__(self, *, db_file_name: str, tabel_name: str):
    self.db_file_name = db_file_name
    self.table_name = tabel_name

  def ST_DB(self, *, values: str):
    conn = sqlite3.connect(self.db_file_name)
    cursor = conn.cursor()
    cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {self.table_name} {values}
    """)
    conn.commit()
    conn.close()

  async def ADD_DB(self, *, values: tuple, str_v: str, how_many_values: str):
    base = sqlite3.connect(self.db_file_name)
    cursor = base.cursor()
    cursor.execute(
      f"""INSERT INTO {self.table_name} {str_v}
                                            VALUES {how_many_values}""",
      values)
    base.commit()
    base.close()

  def qui_sql(self):
    conn = sqlite3.connect(self.db_file_name)
    cursor = conn.cursor()
    return conn, cursor