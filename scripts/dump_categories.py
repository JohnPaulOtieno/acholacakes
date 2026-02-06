import sqlite3
import os
p = os.path.join(os.path.dirname(__file__), '..', 'db.sqlite3')
print('DB path:', os.path.abspath(p))
conn = sqlite3.connect(p)
c = conn.cursor()
try:
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = c.fetchall()
    print('Tables:', tables)
    c.execute("SELECT id, name, slug FROM store_category")
    rows = c.fetchall()
    if rows:
        for r in rows:
            print(r)
    else:
        print('No rows in store_category')
except Exception as e:
    print('ERROR:', e)
finally:
    conn.close()
