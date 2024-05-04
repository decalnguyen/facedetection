# importing the required libraries
import psycopg2

# Connect to the PostgreSQL database
conn = psycopg2.connect('<SERVICE_URI>')
cur = conn.cursor()
cur.execute('INSERT INTO pictures values (%s,%s)', (file_name, embedding.tolist()))
conn.commit()
conn.close()