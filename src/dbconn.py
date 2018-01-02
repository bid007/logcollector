#Author : Bidhya Nandan Sharma
#Date 12/18/2017

import psycopg2
try:
    conn = psycopg2.connect("dbname='logdb' user='loguser' host='localhost' password='minilp'")
    cur = conn.cursor()
    cur.execute("""
                CREATE TABLE IF NOT EXISTS logtable (
                ID SERIAL PRIMARY KEY,
                IP VARCHAR(20),
                LOG VARCHAR(1000),
                TIMESTAMP TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
                """)
    cur.close()
    conn.commit()
except Exception as e:
    print(e)
    print("Unable to establish connection with db")

