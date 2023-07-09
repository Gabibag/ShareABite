import sqlite3

connection = sqlite3.connect('database.sqlite')

cur = connection.cursor()
# clear table
cur.execute("DELETE FROM organizations")

cur.execute("INSERT INTO organizations (name, address, foods) VALUES (?, ?, ?)",
            ('corn society', '2005 Valley Ave Gate 8, Pleasanton, CA 94566', 'corn')
            )
cur.execute("INSERT INTO organizations (name, address, foods) VALUES (?, ?, ?)",
            ('potato ward', '7068 Koll Center Pkwy, Pleasanton, CA 94566', 'potato')
            )
cur.execute("INSERT INTO organizations (name, address, foods) VALUES (?, ?, ?)",
            ('tomato town', '5420 Sunol Blvd, Pleasanton, CA 94566', 'tomato')
            )
cur.execute("INSERT INTO organizations (name, address, foods) VALUES (?, ?, ?)",
            ('banana bay', '400 Tawny Dr, Pleasanton, CA 94566', 'banana')
            )
cur.execute("INSERT INTO organizations (name, address, foods) VALUES (?, ?, ?)",
            ('food for all', '3200 W Lagoon Rd, Pleasanton, CA 94588', '')
            )

connection.commit()
connection.close()
