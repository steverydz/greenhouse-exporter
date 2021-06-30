import os
import psycopg2


connection = psycopg2.connect(os.getenv("GREENHOUSE_DATABASE_URL"))

cursor = connection.cursor()

cursor.execute("SELECT * FROM applications;")
print(cursor.fetchone())