import sqlite3

connection = sqlite3.connect('database.sqlite')

cur = connection.cursor()
# clear table
cur.execute("DELETE FROM organizations")

cur.execute("INSERT INTO organizations (name, address, foods, phone) VALUES (?, ?, ?, ?)",
            ('corn society', '2005 Valley Ave Gate 8, Pleasanton, CA 94566', 'corn', '925-426-7600')
            )
cur.execute("INSERT INTO organizations (name, address, foods, phone) VALUES (?, ?, ?, ?)",
            ('potato ward', '7068 Koll Center Pkwy, Pleasanton, CA 94566', 'potato', '425-564-1000')
            )
cur.execute("INSERT INTO organizations (name, address, foods, phone) VALUES (?, ?, ?, ?)",
            ('tomato town', '5420 Sunol Blvd, Pleasanton, CA 94566', 'tomato', '661-253-7500')
            )
cur.execute("INSERT INTO organizations (name, address, foods, phone) VALUES (?, ?, ?, ?)",
            ('banana bay', '400 Tawny Dr, Pleasanton, CA 94566', 'banana',  '699-213-7222')
            )
cur.execute("INSERT INTO organizations (name, address, foods, phone) VALUES (?, ?, ?, ?)",
            ('food for all', '3200 W Lagoon Rd, Pleasanton, CA 94588', '', '925-426-7600')
            )


connection.commit()
connection.close()
