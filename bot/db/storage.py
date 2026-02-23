from aiogram_sqlite_storage.sqlitestore import SQLStorage

fsm_storage = SQLStorage('db.sqlite', serializing_method = 'pickle')