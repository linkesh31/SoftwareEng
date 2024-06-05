import mysql.connector
from mysql.connector import Error
import random
from faker import Faker
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

# Create a Faker instance
fake = Faker()

# Function to create a connection to the MySQL database
def create_connection(host='localhost', username='root', password='calladoctor1234', database='calladoctor'):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host,
            user=username,
            passwd=password,
            database=database
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

# Function to execute SQL queries
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

# Function to insert random doctor users into the database
def insert_random_doctors(connection, num_doctors):
    cursor = connection.cursor()

    for _ in range(num_doctors):
        # Generate random data
        fullname = fake.name()
        username = fake.user_name()
        password = fake.password()
        email = fake.email()
        phone_number = fake.phone_number()
        date_of_birth = fake.date_of_birth(minimum_age=30, maximum_age=70)
        address = fake.address()

        # Insert user into Users table
        user_insert_query = f"""
        INSERT INTO Users (username, password, email, phone_number, date_of_birth, address, role)
        VALUES ('{username}', '{password}', '{email}', '{phone_number}', '{date_of_birth}', '{address}', 'doctor');
        """

        execute_query(connection, user_insert_query)

        # Get the user_id of the inserted user
        cursor.execute(f"SELECT user_id FROM Users WHERE username = '{username}'")
        user_id = cursor.fetchone()[0]

        # Insert doctor into Doctors table
        clinic_id = random.randint(1, 5)  # Assuming you have 5 clinics
        doctor_insert_query = f"""
        INSERT INTO Doctors (user_id, fullname, clinic_id, license_photo)
        VALUES ({user_id}, '{fullname}', {clinic_id}, 'dummy_license_photo');
        """

        execute_query(connection, doctor_insert_query)

# Replace with your own database connection details
connection = create_connection("localhost", "root", "calladoctor1234", "calladoctor")

# Creating tables (assuming they are already created as per your previous script)

# Insert 5 random doctors
insert_random_doctors(connection, 5)

# Example of how to fetch users
def fetch_users(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Users")
    users = cursor.fetchall()
    print("Users retrieved successfully")
    for user in users:
        print(user)

fetch_users(connection)
