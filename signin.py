import bcrypt
import mysql.connector

def signin(name, user_phone, username, password, role_id):
    # set up a connection to the database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="deteksi"
    )

    # create a cursor object to execute queries
    mycursor = mydb.cursor()

    # execute a SELECT query to check if the user exists
    sql = "SELECT * FROM user WHERE username = %s"
    val = (username,)
    mycursor.execute(sql, val)
    result = mycursor.fetchone()

    # check the result of the query
    if not result:
        # generate a salt and hash the password
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)


        # insert the new user into the database
        
        insert_sql = "INSERT INTO user (name, user_phone, username, password, role_id) VALUES (%s, %s,%s,%s,%s)"
        insert_val = (name, user_phone, username, password_hash, role_id)
        mycursor.execute(insert_sql, insert_val)
        mydb.commit()
        print("New user created!")

        # return to login ui
        return True
        
    else:
        print("Invalid email or password")
        # stay in signin ui
        return False
