
"""
This python file contains the database-related functions for managing various entities within
the XYZ Gym management system. It includes CRUD (Create, Read, Update, Delete) operations for 
managing members, classes, membership plans and payments, and checking the existence of members, class, instructor, and gyms. 

All functions interact with an SQLite database and include error handling to ensure smooth operation.

Authors: Alena Fischer, Devon Alonzo, Ludwig Scherer
Date: 03/23/2025
Last Updated: 4/28/2025
"""

import PySimpleGUI as sg      
import sqlite3
import os
import sys

__dataBaseName__ =  "XYZGym.sqlite"

def connectToDatabase():
    """
    Prompts the user to input the database name and connects to it if valid.
    
    Validates the user input to ensure:
    - A database name is entered
    - The entered name matches the expected datbase
    - The database file exists in the directory

    Returns:
        Connection object if successful, None if user cancels.
    """

    while True:
        # Ask user for the database name
        db_name = sg.popup_get_text('Enter database name (e.g., XYZGym.sqlite):')

        # If user cancels or closes the window
        if db_name is None:
            sg.popup("Exiting program.")
            return None

        # Check if the user input is empty
        if not db_name:
            sg.popup_error("No database name entered. Please provide a valid database name.")
            continue
    
        # Verify if the entered database name matches the expected one
        if db_name != __dataBaseName__:
            sg.popup_error(f"The database '{db_name}' is not valid. Please try again.")
            continue
    
        # Check if the database file exists in the current directory
        if not os.path.exists(db_name):
            sg.popup_error(f"The database '{db_name}' does not exist. Please check the database file.")
            continue
    
        try:
            # Attempt to connect to the database
            connection = sqlite3.connect(db_name)
            sg.popup('Connection successful!')
            return connection
        except sqlite3.Error as e:
            # Catch any SQLite connection errors
            sg.popup_error(f'Error: {e}')
            continue

def execute_query(query, connection, params=()):
    """
    Executes an SQL query and prints the results

    Parameters:
    - query (str): The SQL query to execute
    - connection: Database connection object
    - params (tuple): Parameters to be passed to the query (default is empty tuple)
    
    Returns:
    - list: Query results if successful.
    """

    # Create a cursor object from the connection
    cursor = connection.cursor()

    try:
        cursor.execute(query, params) # Execute the query with parameters
        results = cursor.fetchall() # Fetch all the results of the query
        return results
    except sqlite3.Error as e:
        # Print an error message if the query fails
        print(f"Database error: {e}")

# ------------------------ Member Functions ------------------------
def add_member(connection, name, email, phone, address, age, membershipStartDate, membershipEndDate):
    """
    This function inserts a new member into the Member table.

    Parameters:
    - connection (sqlite3.Connection): The active connection to the database.
    - name (str): The member's name.
    - email (str): The member's email address.
    - phone (str): The member's phone number.
    - address (str): The member's residential address.
    - age (int): Member's age (>= 15)
    - membershipStartDate (str): Start date (YYYY-MM-DD).
    - membershipEndDate (str): End date (YYYY-MM-DD).

    Returns:
    - int: New member ID if successful
    - bool: False if an error occurs.
    """
    
    # SQL query to add a new member to the database
    query = """
        INSERT INTO Member (name, email, phone, address, age, membershipStartDate, membershipEndDate)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """

    # Create a cursor object from the connection
    cursor = connection.cursor()

    try:
        cursor.execute(query, (name, email, phone, address, age, membershipStartDate, membershipEndDate))
        connection.commit() # Commit the changes to the database
        return cursor.lastrowid # Return newly generated member ID
    except sqlite3.Error as e:
        # Print an error message if insertion fails
        print(f"Error adding member: {e}")
        return False
    
def add_payment(connection, memberID, planID, amountPaid, paymentDate):
    """
    Insertes a payment record into the Payment table for a specific member.

    Parameters:
    - connection (sqlite3.Connection): The active connection to the database.
    - memberID (int): Member's ID.
    - planID (int): ID of the membership plan.
    - amountPaid (int): Amount paid.
    - paymentDate (str): Date of payment (YYYY-MM-DD).

    Returns:
    - bool: True if insertion succeeds, False otherwise.
    """
    
    # SQL query to insert a payment record
    query = """
        INSERT INTO Payment (memberID, planID, amountPaid, paymentDate)
        VALUES (?, ?, ?, ?)
    """

    # Create a cursor object from the connection
    cursor = connection.cursor()

    try:
        cursor.execute(query, (memberID, planID, amountPaid, paymentDate))
        connection.commit() # Commit the changes to the database
        return True
    except sqlite3.Error as e:
        # Print an error message if insertion fails
        print(f"Error adding payment: {e}")
        return False

def update_member(connection, member_id, name, email, phone, address, age, start_date, end_date):
    """
    Updates an existing member's information.

    Parameters:
    - connection (sqlite3.Connection): The active connection to the database.
    - member_id (int): ID of the member to update.
    - name (str): New name.
    - email (str): New email.
    - phone (str): New phone number.
    - address (str): New residential address.
    - age (int): New age.
    - start_date (str): Updated membership start date.
    - end_date (str): Updated membership end date.

    Returns:
    - bool: True if updated successfully, False otherwise.
    """
    
    # SQL query to update the member's information
    query = """
        UPDATE Member
        SET name = ?, email = ?, phone = ?, address = ?, age = ?,
            membershipStartDate = ?, membershipEndDate = ?
        WHERE memberID = ?
    """

    # Create a cursor object from the connection
    cursor = connection.cursor()

    try:
        cursor.execute(query, (name, email, phone, address, age, start_date, end_date, member_id))
        connection.commit() # Commit the changes to the database
        return True
    except sqlite3.Error as e:
        # Print an error message if insertion fails
        print(f"Error updating member: {e}")
        return False
    
def member_exists(connection, member_id):
    """
    Checks if a member exists in the database.

    Parameters:
    - connection (sqlite3.Connection): The active connection to the database.
    - member_id (int): Member's ID to check.

    Returns:
    - bool: True if member exists, False otherwise.
    """

    # SQL query to check if a member exists
    query = """
        SELECT 1 FROM Member WHERE memberID = ?
    """

    # Create a cursor object from the connection
    cursor = connection.cursor()
    try:
        cursor.execute(query, (member_id,))
        # Returns True if a member exists, False otherwise
        return cursor.fetchone() is not None
    except sqlite3.Error as e:
        # Print an error message if issue occurs
        print(f"Error checking member existence: {e}")
        return False
    
def delete_member(connection, member_id):
    """
    Deletes a member from the Member table in the database.

    Parameters:
    - connection (sqlite3.Connection): The active connection to the database.
    - member_id (int): ID of the member to delete.

    Returns:
    - bool: True if deletion succeeds, False otherwise.
    """

    # SQL query to delete a member
    query = """
        DELETE FROM Member
        WHERE memberID =?
    """

    # Create a cursor object from the connection
    cursor = connection.cursor()

    try:
        cursor.execute(query, (member_id,))
        connection.commit() # Commit the changes to the database
        return True
    except sqlite3.Error as e:
        # Print an error message if issue occurs
        print(f"Error deleting member: {e}")
        return False
    
# ------------------------ Class Functions ------------------------
def add_class(connection, className, classType, duration, classCapacity, instructorID, gymID):
    """
    Adds a new class to the database.

    Parameters:
    - connection (sqlite3.Connection): The active connection to the database.
    - className (str): Name of the class.
    - classType (str): Type of the class (Yoga, Zumba, etc.).
    - duration (int): Duration of the class in minutes.
    - classCapacity (int): Maximum number of participants.
    - instructorID (int): ID of the instructor teaching the class.
    - gymID (int): ID of the gym facility.

    Returns:
    - int: ID of the newly added class if successful.
    - bool: False if addition fails.
    """

    # SQL query to add a class to the database
    query = """
        INSERT INTO Class (className, classType, duration, classCapacity, instructorID, gymID)
        VALUES (?, ?, ?, ?, ?, ?)
    """

    # Create a cursor object from the connection
    cursor = connection.cursor()

    try:
        cursor.execute(query, (className, classType, duration, classCapacity, instructorID, gymID))
        connection.commit() # Commit the changes to the database
        return cursor.lastrowid # Return the ID of the new class
    except sqlite3.Error as e:
        # Print error message if insertion fails
        print(f"Error adding member: {e}")
        return False

def update_class(connection, classID, className, classType, duration, classCapacity, instructorID, gymID):
    """
    Updates the details of an existing class.

    Parameters:
    - connection (sqlite3.Connection): The active connection to the database.
    - classID (int): ID of the class to update.
    - className (int): New name of the class.
    - classType (str): New class type.
    - duration (int): New duration.
    - classCapacity (int): New class capacity.
    - instructorID (int): New instructor ID.
    - gymID (int): New gym ID.

    Returns:
    - bool: True if updated successfully, False otherwise.
    """
    
    # SQL query to update a class's information
    query = """
        UPDATE Class
        SET className = ?, classType = ?, duration = ?, classCapacity = ?,
            instructorID = ?, gymID = ?
        WHERE classID = ?
    """

    # Create a cursor object from the connection
    cursor = connection.cursor()

    try:
        cursor.execute(query, (className, classType, duration, classCapacity, instructorID, gymID, classID))
        connection.commit() # Commit the changes to the databaes
        return True
    except sqlite3.Error as e:
        # Print error message if insertion fails
        print(f"Error updating member: {e}")
        return False

def delete_class(connection, class_id):
    """
    Deletes a class from the Class table in the database.

    Parameters:
    - connection (sqlite3.Connection): The active connection to the database.
    - class_id (int): ID of the class to delete.

    Returns:
    - bool: True if deletion succeeds, False otherwise.
    """

    # SQL query to delete a class
    query = """
        DELETE FROM Class
        WHERE classID = ?
    """

    # Create a cursor object from the connection
    cursor = connection.cursor()

    try:
        cursor.execute(query, (class_id,))
        connection.commit() # Commit the changes to the database
        return cursor.rowcount > 0 # Return True if the class was deleted 
    except sqlite3.Error as e:
        # Print an error message if deletion fails
        print(f"Error deleting class {e}")
        return False

def get_all_classes(connection):
    """
    Retrieves all class records from the database.

    Parameters:
    - connection (sqlite3.Connection): The active connection to the database.

    Returns:
    - list: List of all classes.
    """

    # SQL query to retrieve all class records
    query = """
        SELECT classID, className, classType, duration, classCapacity, instructorID, gymID
        FROM Class
    """

    # Execute query and return the results
    return execute_query(query, connection)

def get_classes_with_attendance(connection):
    """
    Retrieves classes along with the number of attendees.

    Parameters:
    - connection (sqlite3.Connection): The active connection to the database.

    Returns:
    - list: List of all classes with their attendance counts.
    """

    # SQL query to retrieve class details and number of attendees
    query = """
        SELECT
            c.classID,
            c.className,
            c.classType,
            c.duration,
            c.classCapacity,
            COUNT (a.memberID) AS num_attendees
        FROM Class c
        LEFT JOIN Attends a ON c.classID = a.classID
        GROUP BY c.classID
    """

    # Create a cursor object from the connection
    cursor = connection.cursor()

    # Execute the query and return the results
    cursor.execute(query)
    return cursor.fetchall()

def class_has_members(connection, class_id):
    """
    Checks if any members are registered for a specific class.

    Parameters:
    - connection (sqlite3.Connection): The active connection to the database.
    - class_id (int): ID of the class to check.

    Returns:
    - bool: True if class has registered members, False otherwise.
    """

    # SQl query to count the members registered for a specific class
    query = """
        SELECT COUNT(*) FROM Attends
        WHERE classID = ?
    """

    # Create a cursor object from the connection
    cursor = connection.cursor()

    # Execute the query and fetch the results
    cursor.execute(query, (class_id,))
    result = cursor.fetchone()
    return result[0] > 0 # Returns True if members are registered to the class

def move_members(connection, old_classID, new_classID):
    """
    Moves all members from one class to another.

    Parameters:
    - connection (sqlite3.Connection): The active connection to the database.
    - old_classID (int): ID of the class members are currently enrolled in.
    - new_classID (int): ID of the new class to move members to.

    Returns:
    - bool: True if any members were moved, False otherwise.
    """

    # SQl query to update the classID for all members in the old class
    query = """
        UPDATE Attends
        SET classID = ?
        WHERE classID = ?
    """

    # Create a cursor object from the connection
    cursor = connection.cursor()

    try:
        cursor.execute(query, (new_classID, old_classID))
        connection.commit() # Commit the changes to the database
        return cursor.rowcount > 0 # Returns True if members were successfully moved
    except sqlite3.Error as e:
        print(f"Error moving members: {e}")
        return False # Returns false if fails

def check_email_exists(connection, email):
    """
    Checks if a given email address is alreayd associated with a member.

    Parameters:
    - connection (sqlite3.Connection): The active connection to the database.
    - email (str): Email address to check.

    Returns:
    - bool: True if email exists, False otherwise
    """

    # SQL query to check if email address exists in the Member table
    query = """
        SELECT 1 FROM Member
        WHERE email = ?
    """

    # Execute the query and return the results
    result = execute_query(query, connection, (email,))
    return len(result) > 0

def class_exists(connection, class_id):
    """
    Check if a class exists in the database.

    Parameters:
    - connection (sqlite3.Connection): The active connection to the database.
    - class_id (int): Class ID to check.

    Returns:
    - bool: True if class exists, False otherwise.
    """

    # SQL query to check if the class exists in the Class table
    query = """
        SELECT 1 FROM Class WHERE classID = ?
    """

    # Create a cursor object from the connection
    cursor = connection.cursor()

    try:
        cursor.execute(query, (class_id,))
        # Returns True if a class exists, False otherwise
        return cursor.fetchone() is not None
    except sqlite3.Error as e:
        # Print error message if issue occurs
        print(f"Error checking member existence: {e}")
        return False

def get_members_and_membership_plan(connection):
    """
    Retrieves all members along with their membership plan.

    Parameters:
    - connection (sqlite3.Connection): The active connection to the database.

    Returns:
    - list: List of all members with their names, email, ages, and plan IDs.
    """

    # SQl query to select members and their associated membership plan details
    query = """
        SELECT
            m.memberID,
            m.name, 
            m.email, 
            m.age,
            mp.planId
        FROM Member m 
        JOIN Payment p ON m.memberID = p.memberID
        JOIN MembershipPlan mp ON p.planId = mp.planId
    """

    # Execute the query and return the result
    return execute_query(query, connection)

def membership_plan_exists(connection, mempership_id) :
    """
    Check if a membership plan exists in the database.

    Parameters:
    - connection (sqlite3.Connection): The active connection to the database.
    - mempership_id (int): membership ID to check.

    Returns:
    - bool: True if plan exists, False otherwise.
    """

    # SQL query to check if the plan exists in the MembershipPlan table
    query = """
        SELECT 1 FROM MembershipPlan WHERE planId = ?
    """

    # Create a cursor object from the connection
    cursor = connection.cursor()

    try:
        cursor.execute(query, (mempership_id,))
        # Returns True if the equipment exists, False otherwise
        return cursor.fetchone() is not None
    except sqlite3.Error as e:
        # Print error message if issue occurs
        print(f"Error checking member existence: {e}")
        return False
    
def get_all_membership_plan_ids(connection):
    """
    Retrieves all plan id's from the database.

    Parameters:
    - connection (sqlite3.Connection): The active connection to the database.

    Returns:
    - list: List of all plan id's.
    """

    # SQL query to retrieve all plan id's
    query = """
        SELECT planID
        FROM MembershipPlan
    """

    # Execute query and return the results
    return execute_query(query, connection)
    
def get_members_in_class(connection, class_id):
    """
    Retrieves all members registered to a specific class.

    Parameters:
    - connection (sqlite3.Connection): The active connection to the database.
    - class_id (int): Class ID to retrieve members of.

    Returns:
    - list: List of members attending the specified class.
    """

    # SQL wuery to seelct members registered for a specific class
    query = """
        SELECT 
            m.memberID,
            m.name,
            m.email,
            m.age
        FROM Member m
        INNER JOIN Attends a ON m.memberID = a.memberID
        WHERE a.classID = ?
    """

    # Create a cursor object from the connection
    cursor = connection.cursor()

    # Execute the query and fetch the results
    cursor.execute(query, (class_id,))
    return cursor.fetchall()

def instructor_exists(connection, instructor_id):
    """
    Check if an instructor exists in the database.

    Parameters:
    - connection (sqlite3.Connection): The active connection to the database.
    - instructor_id (int): Instructor's ID to check.

    Returns:
    - bool: True if instructor exists, False otherwise.
    """

    # SQL query to check if the instructor exists in the Instructor table
    query = """
        SELECT 1 FROM Instructor WHERE instructorID = ?
    """

    # Create a cursor object from the connection
    cursor = connection.cursor()

    try:
        cursor.execute(query, (instructor_id,))
        # Returns True if instructor exists, False otherwise
        return cursor.fetchone() is not None
    except sqlite3.Error as e:
        # Print error message if issue occurs
        print(f"Error checking instructor existence: {e}")
        return False
    
def gym_exists(connection, gym_id):
    """
    Checks if a gym facility exists in the database.

    Parameters:
    - connection (sqlite3.Connection): The active connection to the database.
    - gym_id (int): Gym ID to check.

    Returns:
    - bool: True if ym exists, False otherwise.
    """

    # SQl query to check if the gym exists in the GymFacility table
    query = """
        SELECT 1 FROM GymFacility WHERE gymID = ?
    """

    # Create a cursor object from the connection
    cursor = connection.cursor()

    try:
        cursor.execute(query, (gym_id,))
        # Returns True if the gym exists, False otherwise
        return cursor.fetchone() is not None
    except sqlite3.Error as e:
        # Print error message if issue occurs
        print(f"Error checking gym existence: {e}")
        return False
    
# ------------------------ Equipment Functions ------------------------

def get_all_equipment(connection):
    """
    Retrieves all equipment records from the database.

    Parameters:
    - connection (sqlite3.Connection): The active connection to the database.

    Returns:
    - list: List of all equipment.
    """
    # query to get all equipment
    query = """SELECT * FROM Equipment"""

    # return the equipment
    return execute_query(query, connection)

def add_equipment(connection, equipmentName, equipmentType, quantity, gymID):
    """
    Adds a new piece of equipment to the database.

    Parameters:
    - connection (sqlite3.Connection): The active connection to the database.
    - equipmentName (str): Name of the equipment.
    - equipmentType (str): Type of the equipment (Cardio, Strength, etc.).
    - quantity (int): quantity of the piece of equipment.
    - gymID (int): ID of the gym facility.

    Returns:
    - int: ID of the newly added equipment if successful.
    - bool: False if addition fails.
    """

    # SQL query to add a piece of equipment to the database
    query = """
        INSERT INTO Equipment (name, classType, quantity, gymID)
        VALUES (?, ?, ?, ?)
    """

    # Create a cursor object from the connection
    cursor = connection.cursor()

    try:
        cursor.execute(query, (equipmentName, equipmentType, quantity, gymID))
        connection.commit() # Commit the changes to the database
        return cursor.lastrowid # Return the ID of the new equipment
    except sqlite3.Error as e:
        # Print error message if insertion fails
        print(f"Error adding member: {e}")
        return False
    
def update_equipment(connection, equipmentID, equipmentName, equipmentType, quantity, gymID):
    """
    Updates the details of an existing piece of equipment.

    Parameters:
    - connection (sqlite3.Connection): The active connection to the database.
    - equipmentID (int): ID of the equipment to update.
    - equipmentName (int): New name of the equipment.
    - equipmentType (str): New equipment type.
    - qunatity (int): New quantity.
    - gymID (int): New gym ID.

    Returns:
    - bool: True if updated successfully, False otherwise.
    """
    
    # SQL query to update a class's information
    query = """
        UPDATE Equipment
        SET name = ?, classType = ?, quantity = ?, gymID = ?
        WHERE equipmentID = ?
    """

    # Create a cursor object from the connection
    cursor = connection.cursor()

    try:
        cursor.execute(query, (equipmentName, equipmentType, quantity, gymID, equipmentID))
        connection.commit() # Commit the changes to the databaes
        return True
    except sqlite3.Error as e:
        # Print error message if insertion fails
        print(f"Error updating equipment: {e}")
        return False
    
def delete_equipment(connection, equipment_id):
    """
    Deletes a piece of equipment from the Equipment table in the database.

    Parameters:
    - connection (sqlite3.Connection): The active connection to the database.
    - equipment_id (int): ID of the equipment to delete.

    Returns:
    - bool: True if deletion succeeds, False otherwise.
    """

    # SQL query to delete a piece of a equipment
    query = """
        DELETE FROM Equipment
        WHERE equipmentID = ?
    """

    # Create a cursor object from the connection
    cursor = connection.cursor()

    try:
        cursor.execute(query, (equipment_id,))
        connection.commit() # Commit the changes to the database
        return True
    except sqlite3.Error as e:
        # Print an error message if issue occurs
        print(f"Error deleting member: {e}")
        return False
    
def equipment_exists(connection, equipment_id):
    """
    Check if a piece of equipment exists in the database.

    Parameters:
    - connection (sqlite3.Connection): The active connection to the database.
    - equipment_id (int): Equipment ID to check.

    Returns:
    - bool: True if class exists, False otherwise.
    """

    # SQL query to check if the equipment exists in the Equipment table
    query = """
        SELECT 1 FROM Equipment WHERE equipmentID = ?
    """

    # Create a cursor object from the connection
    cursor = connection.cursor()

    try:
        cursor.execute(query, (equipment_id,))
        # Returns True if the equipment exists, False otherwise
        return cursor.fetchone() is not None
    except sqlite3.Error as e:
        # Print error message if issue occurs
        print(f"Error checking member existence: {e}")
        return False

