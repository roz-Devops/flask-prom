from flask import Flask, request, jsonify, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import mysql.connector
import time

app = Flask('__main__')

# Define Prometheus metrics
mysql_query_count = Counter('mysql_query_count', 'Total number of MySQL queries executed')
mysql_query_duration = Histogram('mysql_query_duration_seconds', 'Time taken to execute MySQL queries')

# MySQL connection config
db_config = {
    'user': 'root',       # Your MySQL username
    'password': 'password',  # Your MySQL password
    'host': '127.0.0.1',  # Change this if you're using Kubernetes or different host
    #'host': 'mysql-service.default.svc.cluster.local',
    'port': '3306',      # Port for MySQL
    'database': 'demo_db'  # Ensure this matches the database name
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

# Function to execute a MySQL query and collect metrics
def execute_mysql_query(query):
    start_time = time.time()
    result = None
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)  # Using dictionary=True to get results as dictionaries
        cursor.execute(query)
        result = cursor.fetchall()
        
        # Increment the query counter
        mysql_query_count.inc()
    except Exception as e:
        print(f"Error executing query: {e}")
    finally:
        # Record the duration and cleanup
        duration = time.time() - start_time
        mysql_query_duration.observe(duration)
        
        if cursor is not None:
            cursor.close()
        if connection is not None:
            connection.close()

    return result

@app.route('/')
def welcome():
    print("welcome to hell")
    return "Welcome to hell"

# Define an endpoint to run a specific query
@app.route('/query')
def query():
    query_type = request.args.get("type")  # Get query parameter 'type'
    if query_type == "primary":
        result = execute_mysql_query("SELECT * FROM colors WHERE color_type = 'primary'")
    elif query_type == "basic":
        result = execute_mysql_query("SELECT * FROM colors WHERE color_type = 'basic'")
    else:
        result = execute_mysql_query("SELECT * FROM colors")  # Default query
    
    return jsonify(result)

# Expose Prometheus metrics at the /metrics endpoint
@app.route('/metrics')
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


@app.route('/add_color')
def add_color():
        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert query
        query = "INSERT INTO colors (color, color_type) VALUES (%s, %s)"
        cursor.execute(query, ("coral", "basic"))
        conn.commit()

        # Return the ID of the newly created record
        new_id = cursor.lastrowid

        return jsonify({"message": "Record created successfully.", "id": new_id}), 201

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
