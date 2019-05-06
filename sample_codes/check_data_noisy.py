import sqlite3
dataset_path = 'prutor-deepfix-09-12-2017.db'
with sqlite3.connect(dataset_path) as conn:
   cur = conn.cursor()
   query = "SELECT user_id, tokenized_code FROM Code;"
   code = []
   for row in cur.execute(query):
      user_id, tokenized_code = map(str, row)
      code.append((user_id, tokenized_code))

