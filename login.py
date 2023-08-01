import mysql.connector
import bcrypt

def do_login(username, password):
    # Connect to the database
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="deteksi"
    )

    cursor = db.cursor()

    cursor.execute("SELECT id_user, password, role_id FROM user WHERE username = %s", (username,))
    result = cursor.fetchone()

    if result:
        id_user = result[0]
        hashed_password = result[1].encode('utf-8')
        role_id = result[2]

        if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
            print("Login successful")
            return id_user, role_id
        else:
            print("Invalid username or password")
            return None
    else:
        print("Invalid username or password")
        return None