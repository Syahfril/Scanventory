import mysql.connector

def get_table_data(id_user):
    # Connect to MySQL database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="deteksi"
    )
    mycursor = mydb.cursor()

    # Execute SQL query
    query = f"SELECT * FROM shop WHERE user_id = {id_user}"
    
    mycursor.execute(query)
    data = mycursor.fetchall()

    # Get column names
    column_names = [i[0] for i in mycursor.description]
    print(query)

    # Close the database connection
    mycursor.close()
    mydb.close()

    return data, column_names
   
