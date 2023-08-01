import mysql.connector

def get_shop(name, address, email, phone,user_id):
    # Check if any of the inputs are empty
    if not all((name, address, email, phone, user_id)):
        print("Error: All fields must be filled in.")
        return False

    # set up a connection to the database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="deteksi"
    )

    mycursor = mydb.cursor()
    insert_sql = "INSERT INTO shop (shop_name, adress, email, shop_phone,user_id) VALUES (%s, %s,%s,%s,%s)"
    insert_val = (name, address, email, phone, user_id)
    mycursor.execute(insert_sql, insert_val)
    mydb.commit()
    print("Success")
    return True

def delete_shop(id_shop):
    # Connect to MySQL database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="deteksi"
    )
    mycursor = mydb.cursor()

    try:
        # Delete corresponding rows in user table
        mycursor.execute("DELETE FROM user WHERE shop_id = %s", (id_shop,))
        print(mycursor.rowcount, "record(s) deleted from user table")
        
        # Delete row from shop table
        mycursor.execute("DELETE FROM shop WHERE id_shop = %s", (id_shop,))
        print(mycursor.rowcount, "record(s) deleted from shop table")
        
        # Commit the changes
        mydb.commit()

    except mysql.connector.Error as error:
        # Handle the error
        print("Failed to delete record from both tables: {}".format(error))
        mydb.rollback()

    finally:
        # Close the database connection
        mycursor.close()
        mydb.close()

