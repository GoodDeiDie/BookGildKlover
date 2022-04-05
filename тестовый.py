import sqlite3 as sql 


con = sql.connect('libgild.db')


cur = con.cursor()
# cur.execute("""CREATE TABLE IF NOT EXISTS user(
#     id TEXT,
#     idnumber int,
#     count INT,
#     admin INT,
#     reserv1 TEXT);
# """)

# cur.execute("""DROP TABLE book;""")

# cur.execute("""CREATE TABLE IF NOT EXISTS book(
#     name TEXT,
#     id Int,
#     coast INT,
#     icon int);
# """)


cur.execute("INSERT INTO user VALUES(?,?,?,?,?);", (('[id177617355|александр]',177617355,0,1,'reserv')))
# cur.executemany("INSERT INTO myDate VALUES(?,?,?,?);", ((3930401,0,0,0),))
# cur.executemany("INSERT INTO myDate VALUES(?,?,?,?);", ((62973352,0,0,0),))

# cur = con.cursor()
# cur.execute("""CREATE TABLE IF NOT EXISTS help(
#     id TEXT,
#     description TEXT);
# """)
con.commit()

