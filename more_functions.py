import sqlite_functions

def approve(id):
  print("Approved Review")
  employ_ids = sqlite_functions.select_from_table('USERS')
  approved_user = sqlite_functions.select_from_table('USERS', category= 'ID', value= id)
  check_users = [row[0] for row in employ_ids]
  if id not in check_users:
    approved_user_info = approved_user[0]
    sqlite_functions.insert_into_table('Employees', ['ID', 'cart', 'name', 'email', 'gender', 'password'], 
                                       (approved_user_info[0], approved_user_info[1], approved_user_info[2], approved_user_info[3], approved_user_info[4], approved_user_info[5]))
    sqlite_functions.delete_from_Table('Employ_Application', 'ID', (id,))


def deny(id):
   print("Denied Review")
   sqlite_functions.delete_from_Table('Employ_Application', 'ID', (id,))


def add_product():
  product_added = True
  return product_added


def remove_product():
  print('Deleting product from cafe')





