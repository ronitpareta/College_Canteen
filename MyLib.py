import pymysql

#create the dependency injection
def create_connection():
    con = pymysql.connect(host="localhost", user="root", port=3306, db="canteen", passwd="", autocommit=True)
    cur = con.cursor()
    return cur

def check_photo(email):
    cur = create_connection()
    cur.execute("SELECT * FROM photo_data where email='" + email + "'")
    n=cur.rowcount
    photo="nophoto"
    if n>0:
        row=cur.fetchone()
        photo=row[1]
    return photo

def check_item_photo(id):
    cur = create_connection()
    cur.execute("SELECT * FROM food_category where id=%s", (id,))
    row = cur.fetchone()
    if row and row[4]:
        return row[4]
    else:
        return 'nophoto'


def check_balance(st_id):
    cur = create_connection()
    try:
        cur.execute("SELECT balance FROM user_data WHERE st_id = %s", (st_id,))
        row = cur.fetchone()
        if row:
            return row[0]   # balance column
        return 0
    finally:
        cur.close()

def fetch_studnet_name(email):
    cur = create_connection()
    cur.execute("SELECT * FROM user_data  WHERE email = %s", (email,))
    n=cur.rowcount
    name=None
    if n>0:
        row=cur.fetchone()
        name=row[1]
    return name