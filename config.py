import mysql.connector

# Define database configuration
db_config = {
    'user': 'your_username',
    'password': 'your_password',
    'host': 'your_host',
    'database': 'smart_waste'
}

# Create a connection to the database
cnx = mysql.connector.connect(**db_config)

# Create a cursor object to execute queries
cursor = cnx.cursor()

# Define a function to close the cursor and connection
def close_connection():
    cursor.close()
    cnx.close()

# Run the application if this script is executed directly
if __name__ == "__main__":
    close_connection()
