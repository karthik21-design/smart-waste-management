from flask import Flask
import mysql.connector

# Create a new instance of the Flask class
app = Flask(__name__)

# Define a route for the root URL
@app.route("/")
def index():
    return "Welcome to Smart Waste Management App"

# Function to connect to database and retrieve data
def get_data_from_database(bin_id):
    try:
        # Establish connection to database
        cnx = mysql.connector.connect(
            user='username',
            password='password',
            host='127.0.0.1',
            database='smart_waste_management'
        )
        
        # Create a cursor object
        cursor = cnx.cursor()
        
        # SQL query to retrieve data from bins table
        query = "SELECT * FROM bins WHERE bin_id = %s"
        cursor.execute(query, (bin_id,))
        
        # Fetch the result
        result = cursor.fetchone()
        
        # Close the cursor and connection
        cursor.close()
        cnx.close()
        
        return result
    
    except mysql.connector.Error as err:
        print("Error: {}".format(err))
        return None

# Run the application if this script is executed directly
if __name__ == "__main__":
    app.run(debug=True)
