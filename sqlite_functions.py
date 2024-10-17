import sqlite3


def sqlite_connection():
    connect = sqlite3.connect('database.db')
    connect.row_factory = sqlite3.Row
    return connect

def get_table(name):
    connect = sqlite_connection() 
    cursor = connect.cursor()
    cursor.execute(f"select * from {name}")
    rows = cursor.fetchall()
    return rows     


def add_to_database(db, db_info):
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()

    db_question_mark_string = ', '.join(['?'] * len(db_info)) # This makes the '?,?',? part. by coming the , and ? into a string depending on the length of things being added to database
    db_string = ', '.join(db_info.keys()) # Makes the string except with the actual row sections in the table

    cursor.execute(f"INSERT INTO {db} ({db_string}) VALUES ({db_question_mark_string})", tuple(db_info.values())) # Converts the dictionary back to a tuple so it can be added to table.
    
    connect.commit()
    connect.close()