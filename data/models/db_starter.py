from pony.orm import Database, sql_debug

db = Database()
db.bind(provider='sqlite', filename='database.sqlite', create_db=True)

sql_debug(True)
