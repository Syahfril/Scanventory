import csv
import mysql.connector

def get_table_item(item,user_id,timestamp_filter):
    # Connect to MySQL database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="deteksi"
    )
    mycursor = mydb.cursor()

    query = f"SELECT id_item, item_name, item_count,user_id, name, timestamp FROM item JOIN user on user.id_user = item.user_id WHERE user_id = {user_id}"
    
    if timestamp_filter == "Last 1 day":
        query += " AND DATE(i.timestamp) = CURDATE()"
    elif timestamp_filter == "Last 1 week":
        query += " AND YEARWEEK(i.timestamp, 1) = YEARWEEK(NOW(), 1)"
    elif timestamp_filter == "Last 1 month":
        query += f" AND YEAR(i.timestamp) = YEAR(NOW()) AND MONTH(i.timestamp) = MONTH(NOW() - INTERVAL 1 MONTH)"

    
    
    mycursor.execute(query)
    data = mycursor.fetchall()

    # Get column names
    column_names = [i[0] for i in mycursor.description]

    # Close the database connection
    mycursor.close()
    mydb.close()

    return data, column_names

def delete_item(item, user_id):
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

def print_table_item(user_id, filename, timestamp_filter):
    data, column_names = get_table_item("item", user_id, timestamp_filter)
    if not data:
        print("No data to print as CSV")
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