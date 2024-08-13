from urllib.parse import quote_plus
import pandas as pd
from sqlalchemy import create_engine
from flask import Flask, jsonify
import os
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Function to get environment variables with error handling
def get_env_variable(var_name):
    value = os.getenv(var_name)
    if value is None:
        raise EnvironmentError(f"Environment variable {var_name} not set.")
    return value

# Define your PostgreSQL connection parameters
DATABASE_TYPE = 'postgresql'
DBAPI = 'psycopg2'
ENDPOINT = get_env_variable('ENDPOINT')
USER = get_env_variable('USER')
PASSWORD = get_env_variable('PASSWORD')
PASSWORD = quote_plus(PASSWORD)  # Ensure PASSWORD is a string before quoting
PORT = get_env_variable('PORT')
DATABASE = get_env_variable('DATABASE')

# Create a SQLAlchemy engine
engine = create_engine(f'{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}')

# Specify the table name you want to read from
table_name = 'customer_bharathi'  # Replace with your table name

@app.route('/data', methods=['GET'])
def get_data():
    try:
        # Read data from the PostgreSQL table into a DataFrame
        df = pd.read_sql_table(table_name, engine)

        # Convert the DataFrame to a dictionary and then to JSON
        data = df.to_dict(orient='records')

        # Return the data as JSON
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5100, debug=True)
