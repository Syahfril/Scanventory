import mysql.connector
import datetime
import csv

def get_report(item,user_id, timestamp_filter):
    # Connect to MySQL database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="deteksi"
    )
    mycursor = mydb.cursor()

    # Define the base query to select all relevant data
    query = f"""SELECT i.id_item,i.item_name,i.user_id, w.name AS worker_name, s.shop_name, i.timestamp
                FROM item i
                JOIN user w ON i.user_id = w.id_user AND w.role_id = 1
                JOIN shop s ON w.shop_id = s.id_shop
                JOIN user o ON s.user_id = o.id_user AND o.role_id = 2
                WHERE o.id_user = {user_id}"""
    

    if timestamp_filter == "Last 1 day":
        query += " AND DATE(i.timestamp) = CURDATE()"
    elif timestamp_filter == "Last 1 week":
        query += " AND YEARWEEK(i.timestamp, 1) = YEARWEEK(NOW(), 1)"
    elif timestamp_filter == "Last 1 month":
        query += f" AND YEAR(i.timestamp) = YEAR(NOW()) AND MONTH(i.timestamp) = MONTH(NOW() - INTERVAL 1 MONTH)"

    # Execute the query and get the data and column names
    #print(query)
    mycursor.execute(query)
    data = mycursor.fetchall()
    column_names = [i[0] for i in mycursor.description]

    # Close the database connection
    mycursor.close()
    mydb.close()

    return data, column_names

def delete_report(item, user_id):
    # Connect to MySQL database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="deteksi"
    )
    mycursor = mydb.cursor()


    # Execute SQL query
    query = f"DELETE FROM {item} WHERE user_id=%s"
    mycursor.execute(query, (user_id,))
    mydb.commit()
    print(mycursor.rowcount, "record(s) deleted")

    # Close the database connection
    mycursor.close()
    mydb.close()

def print_table_all_item(user_id, filename, timestamp_filter):
    data, column_names = get_report("item", user_id, timestamp_filter)
    if not data:
        print("tidak ada data to print as CSV")
        return

    # Find the index of the "id" column in the list of column names
    id_index = column_names.index("id_item")
    id_user_index = column_names.index("user_id")

    # Remove the "id" column from the list of column names
    column_names_without_id = [name for name in column_names if name not in ("id_item", "user_id")]

    with open(filename, "w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(column_names_without_id)

        # Write all data rows except for the "id" column to the CSV file
        for row in data:
            csv_writer.writerow(row[:id_index] + row[id_index+1:id_user_index] + row[id_user_index+1:])

    print(f"Table data printed as CSV to {filename}")
