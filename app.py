from flask import Flask

# Create a new instance of the Flask class
app = Flask(__name__)

# Define a route for the root URL
@app.route("/")
def index():
    return "Welcome to Smart Waste Management App"

# Run the application if this script is executed directly
if __name__ == "__main__":
    app.run(debug=True)
