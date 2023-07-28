import sqlite3 as sq


with sq.connect("simple_database.db") as conn:
    """Creating connection with the database called simple_database and creating a table called users.
    Best practice would be to use context managers as I did, otherwise if errors occur, the connection
    with the database will not be closed and that's a bad practice"""
    c = conn.cursor()

    c.execute(""" CREATE TABLE IF NOT EXISTS users (
                name TEXT NOT NULL,
                surname TEXT,
                age INTEGER NOT NULL
                )""")


def add_one(name, surname, age):
    """Add A New Record To The Table"""
    # Connect to the database simple_database.db
    conn = sq.connect('simple_database.db')
    # Create a cursor
    c = conn.cursor()

    # Inserting a new record to the users table
    c.execute("INSERT INTO users VALUES(?,?,?)", 
              (name, surname, age))
    
    # Commit the command
    conn.commit()
    # Close the connection
    conn.close()


def add_many(list):
    """Add multiple records to the database table at once"""
    conn = sq.connect('simple_database.db')
    c = conn.cursor()

    c.executemany("INSERT INTO users VALUES(?,?,?)", (list))

    conn.commit()
    conn.close()


def update_one(id, name, surname, age):
    """Updating the specific record values"""
    conn = sq.connect('simple_database.db')
    c = conn.cursor()

    c.execute("UPDATE users SET name = (?), surname = (?), age = (?) WHERE rowid = (?)", 
              (name, surname, age, id))
    
    conn.commit()
    conn.close()


def delete_one(id):
    """Deleting the specific record in the database table"""
    conn = sq.connect('simple_database.db')
    c = conn.cursor()

    c.execute("DELETE FROM users WHERE rowid = (?)", id)

    conn.commit()
    conn.close()


def show_all():
    """Query the database and return all the records"""
    conn = sq.connect('simple_database.db')
    c = conn.cursor()

    c.execute("SELECT rowid, * FROM users")
    items = c.fetchall()

    # Printing all the records
    for item in items:
        print(item)

    conn.close()





