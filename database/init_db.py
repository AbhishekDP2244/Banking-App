# import mysql.connector as sql
# from config import DB_CONFIG

# db = sql.connect(**DB_CONFIG)
# mycur = db.cursor()

# mycur.execute("CREATE DATABASE IF NOT EXISTS bank")
# print("Database created successfully!!")
# db.commit()

# db.close()

import mysql.connector as sql
from config import DB_CONFIG

try:
    # Connect to MySQL server
    db = sql.connect(**DB_CONFIG)
    mycur = db.cursor()
    print("Connected to MySQL server successfully.")

    # Create database if it does not exist
    mycur.execute("CREATE DATABASE IF NOT EXISTS bank")
    db.commit()
    print("Database 'bank' created successfully!!")

except sql.Error as err:
    print(f"Error: {err}")

finally:
    # Ensure the cursor and connection are closed
    if mycur:
        mycur.close()
    if db:
        db.close()
    print("MySQL connection closed.")