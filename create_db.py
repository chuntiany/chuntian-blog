import pymysql
import os

# Try both passwords just in case
passwords = ['chuntian2025', 'wepie1501@']
host = '10.40.20.131'
user = 'root'

for pwd in passwords:
    try:
        print(f"Trying password: {pwd}")
        conn = pymysql.connect(host=host, user=user, password=pwd)
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS blog_db")
        print("Database blog_db created successfully")
        conn.close()
        break
    except Exception as e:
        print(f"Failed with {pwd}: {e}")
