import mysql.connector as sql
from config import DB_CONFIG

db = sql.connect(**DB_CONFIG)
mycur = db.cursor()

mycur.execute("CREATE DATABASE IF NOT EXISTS bank")
db.commit()

db.close()
