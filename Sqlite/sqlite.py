# A simple example to use sqlite
import sqlite3

database_name = 'Sqlite.db'


# connect
connect = sqlite3.connect(database_name)
print("Successfully connect to database [{}]\n".format(database_name))
cursor = connect.cursor()


# delete exist table
try:
    cursor.execute("DROP TABLE company")
except sqlite3.OperationalError as e:
    print("No such table: company")


# create table
print("Now create table: company")
cursor.execute("""CREATE TABLE COMPANY(
    ID INT PRIMARY KEY     NOT NULL,
    NAME           TEXT    NOT NULL,
    AGE            INT     NOT NULL,
    ADDRESS        CHAR(50),
    SALARY         REAL);""")
connect.commit()
print('Successful!\n')


# insert data into database
print('Now insert data into database.')
cursor.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
      VALUES (1, 'Paul', 32, 'California', 20000.00 )")
cursor.execute("INSERT INTO COMPANY VALUES (2, 'Allen', 25, 'Texas', 15000.00 )")
cursor.execute("INSERT INTO COMPANY VALUES (3, 'Teddy', 23, 'Norway', 20000.00 )")
cursor.execute("INSERT INTO COMPANY VALUES (4, 'Mark', 25, 'Rich-Mond ', 65000.00 )")
connect.commit()
print('Successful!\n')


# query data
print('Now query data from database:')
results = cursor.execute("select id, name, address, salary from COMPANY")
print("Now, data in database is:")
for row in results:
    print("ID =", row[0])
    print("Name =", row[1])
    print("Address =", row[2])
    print("Salary =", row[3])
    print()


# update data
print('Now update data in database:')
cursor.execute("update COMPANY set SALARY = 25000.00 WHERE ID = 1")
connect.commit()
print("Total number of rows updated:", connect.total_changes)

results = cursor.execute("SELECT id, name, ADDRESS, salary FROM COMPANY")
print("Now, data in database is:")
for row in results:
    print("ID =", row[0])
    print("Name =", row[1])
    print("Address =", row[2])
    print("Salary =", row[3])
    print()


# delete data
print('Now delete data from database:')
cursor.execute('delete FROM COMPANY where id = 2')
connect.commit()
print("Total number of rows deleted:", connect.total_changes)

results = cursor.execute("select id, name, address, salary FROM COMPANY")
print("Now, data in database is:")
for row in results:
    print("ID =", row[0])
    print("Name =", row[1])
    print("Address =", row[2])
    print("Salary =", row[3])
    print()

connect.close()
