import mysql.connector
from mysql.connector import Error

def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

# Replace with your own database connection details
connection = create_connection("your_host", "your_username", "your_password", "your_db_name")

# Example usage:
# Creating a table
create_table_query = """
CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT, 
  name TEXT NOT NULL, 
  age INT, 
  gender TEXT, 
  nationality TEXT, 
  PRIMARY KEY (id)
) ENGINE = InnoDB
"""

execute_query(connection, create_table_query)

# Inserting data
insert_user_query = """
INSERT INTO users (name, age, gender, nationality) VALUES 
('James', 25, 'male', 'USA'), 
('Leila', 32, 'female', 'France'),
('Brigitte', 35, 'female', 'UK')
"""

execute_query(connection, insert_user_query)

# Reading data
select_users_query = "SELECT * FROM users"
users = execute_read_query(connection, select_users_query)

for user in users:
    print(user)
