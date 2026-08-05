import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        if connection.is_connected():
            print("✅ Successfully connected to the CodeArena MySQL Database!")
            return connection
    except Error as e:
        print(f"❌ Error connecting to MySQL: {e}")
        return None

if __name__ == "__main__":
    get_db_connection()