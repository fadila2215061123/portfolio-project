import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

# Load environment variables from .env file
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Get MongoDB URI and Database Name from environment variables
MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME = os.environ.get("DB_NAME")

# Initialize MongoDB client and access the database
client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

# Access the collection for contacts (you can replace 'contacts' with your preferred collection name)
contacts_collection = db.contacts

# Initialize Flask app
app = Flask(__name__)

# Define the home route (renders index.html for the landing page)
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle form submissions
@app.route('/submit', methods=['POST'])
def contact():
    try:
        # Get form data sent via POST request
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        # Prepare contact data to be inserted into MongoDB
        contact_data = {
            'name': name,
            'email': email,
            'message': message
        }

        # Insert the contact data into MongoDB collection
        contacts_collection.insert_one(contact_data)

        # Send success response
        return jsonify({'msg': 'Your message has been sent successfully!'})

    except Exception as e:
        # Handle any errors that occur and return a JSON error message
        return jsonify({'error': str(e)}), 500

# Run the app on localhost at port 3001
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3001, debug=True)
