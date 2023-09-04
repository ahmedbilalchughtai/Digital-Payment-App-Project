import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('test.db')
cursor = conn.cursor()
cursor.execute('drop table transaction_history')
cursor.execute('Create table transaction_history (username varchar(256),transaction_amount INTEGER,transaction_date datetime)')
conn.commit()