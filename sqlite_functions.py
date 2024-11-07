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


def execute_task(task, values=()): # values is a tuple. If it doesnt get tuple values then the tuple will be empty
    connect = sqlite_connection()
    cursor = connect.cursor()
    cursor.execute(task, values)
    result = cursor.fetchall()
    connect.commit()
    connect.close()
    return result



def insert_into_table(table, category, values):

    values_string = ', '.join(['?'] * len(values)) # combines , and ? to make ,? depending on how many values are added to table.
    category_string = ', '.join(category)
    insert = f"INSERT INTO {table} ({category_string}) VALUES ({ values_string })"
    execute_task(insert, values)


def delete_from_Table(table, category, values):
    
    delete = f"DELETE FROM {table} WHERE {category} = ?"
    execute_task(delete, values)



def select_from_table(table, columns="*", category=None, value=None):
 
    columns_string = ', '.join(columns) if isinstance(columns, (tuple, list)) else columns # This will do * by default otherwise it will do the specific columns put in the parameter if they are a tuple or list.
    select = f"SELECT {columns_string} FROM {table}"
    tuple_values = ()
    if category and value is not None: # only activates this part if both category and value parameters are used
        select += f" WHERE {category} = ?"
        tuple_values  = (value,)
    result = execute_task(select, tuple_values)
    return result if result else [] # Returns the values from the table. If its empty returns an empty list in order to prevent errors.

