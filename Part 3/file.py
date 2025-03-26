"""
This python file contains a program that - when executed, accepts an integer number from 1 to 10
as a command line argument. For the numbers 3, 4, 6, and 9, an additional argument being the 
<classId>, <type>, <instructorId>, and <classType> respectively, is required to be passed as well. 

Authors: Alena Fischer, Devon Alonzo, Ludwig Scherer
Date: 03/23/2025
Last Updated: 3/26/2025
"""

import sqlite3
import sys

__dataBaseName__ =  "XYZGym.sqlite"

def connectToDatabase() :
    """This method tries to connect to the XYZGym Database file. Terminates program on failure

    Returns:
        Cursor: the cursor for database communication
    """
    try:
        connection = sqlite3.connect(__dataBaseName__)
        print(f"Successfully connected to {__dataBaseName__}")
        return connection, connection.cursor() # return the cursor for further database interaction
    
    except Exception as e:
        print(f"ERROR: Database connection unsuccessful. Reason: {e}")
        sys.exit(1) # terminate program if connection fails
        
def checkForInteger(inputToCheck):
    """Function to check if a String represents a a postivie integer

    Args:
        inputToCheck (String): the String to check

    Returns:
        int: the integer if applicable
    """
    
    if inputToCheck.isdigit():
        return int(inputToCheck)
    else:
        print("ERROR: The first parameter needs to be a positive integer from 1 to 10.")
        sys.exit(1)

def execute_query(db_name, query, params=()):
    """
    Executes an SQL query and prints the results

    Parameters:
    - db_name: The database name
    - query: The SQL query to execute
    - params: Parameters to be passed to the query (default is empty tuple)
    """

    # Establish a database connection and cursor
    connection, cursor = connectToDatabase()

    try:
        cursor.execute(query, params) # Execute the query with parameters
        results = cursor.fetchall() # Fetch all the results of the query

        # If there are result, print them
        if results:
            for row in results:
                print(row)
        # If there are no results, a message is printed
        else:
            print("No results found.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        connection.close() # Close the database connection after the query is executed


def get_classes_by_instructor(instructor_id):
    """
    Fetches the list of classes taught by a specific instructor with details.
    """

    query = """
        SELECT 
            i.name AS instructor_name,
            i.phone AS instructor_phone,
            c.className AS class_name,
            c.classType AS class_type,
            c.duration,
            c.classCapacity AS capacity
        FROM Instructor i
        JOIN Class c ON i.instructorID = c.instructorID
        WHERE i.instructorID = ?
    """
    execute_query(__dataBaseName__, query, (instructor_id,))  

def get_average_age_active_memerbship():
    """
    Fetches the average age of members with active memberships.
    """

    query = """
        SELECT AVG(age) AS average_age
        FROM Member
        WHERE membershipEndDate > DATE('now');
    """
    execute_query(__dataBaseName__, query)

def get_average_age_expired_memerbship():
    """
    Fetches the average age of members with expired memberships.
    """

    query = """
        SELECT AVG(age) AS average_age
        FROM Member
        WHERE membershipEndDate <= DATE('now');
    """
    execute_query(__dataBaseName__, query)

def get_top_instructors():
    """
    Fetches the top 3 instructor with the most taught classes.
    """
    
    query = """
        SELECT
            i.name AS instructor_name,
            COUNT(c.classID) AS class_count
        FROM Instructor i
        JOIN Class c ON i.instructorID = c.instructorID
        GROUP BY i.instructorID
        ORDER BY class_count DESC
        LIMIT 3;
    """
    execute_query(__dataBaseName__, query)

def get_members_attended_classes(class_type):
    """
    Fetches the members who attended classes of a specific type.
    """

    query =  """
        SELECT m.memberID, m.name
        FROM Member m
        JOIN Attends a ON m.memberID = a.memberID
        JOIN Class c ON a.classID = c.classID
        WHERE c.classType LIKE ?
        GROUP BY m.memberID;
    """
    execute_query(__dataBaseName__, query, (class_type,))  

def members_attended_classes_last_month():
    """
    Fetches members who attended classes last month and their details.
    """

    query = """
        SELECT m.name AS member_name,
            COUNT(c.classID) AS total_classes,
            GROUP_CONCAT(c.className, ', ') AS class_names,
            GROUP_CONCAT(c.classType, ', ') AS class_types
        FROM Member m
        JOIN Attends a ON m.memberID = a.memberID
        JOIN Class c on a.classID = c.classID
        WHERE a.attendanceDate >= DATE('now', '-1 month')
        GROUP BY m.memberID;
    """
    
    # Execute query, process results, and print attendance details
    connection, cursor = connectToDatabase()
    try:
        cursor.execute(query)
        results = cursor.fetchall() # Fetch the query results

        print("Recent Class Attendance:")
        print(f"{'Member Name':<25}{'Total Classes Attended':<40}{'Classes Attended':<30}{'Class Types':<20}")
        print("=" * 120)

        # Print results for each member
        for row in results:
            member_name = row[0]
            total_classes = row[1]
            class_name = row[2]
            class_type = row[3]

            print(f"{member_name:<25}{total_classes:<40}{class_name:<30}{class_type:<20}")

    # Print error if database query fails
    except sqlite3.Error as e:
        print(f"Error executing query: {e}")

    # Close connection after query execution
    finally:
        connection.close()
        
def main():
    """The main function. Calls database connection function and fetches command line arguments.
        Then checks the first passed parameter for validity (positive integer or not) and passes
        it to a switch statement for further processing
    """
    connection = None
    
    try:
        connection, cursor = connectToDatabase()
        
        cmdLineArgs = sys.argv
        
        if len(cmdLineArgs) > 1: # check if task was specified 
            taskNumber = checkForInteger(cmdLineArgs[1]) # make sure first arg is positive int
        else:
            print("ERROR. Please pass a command line argument.")
            sys.exit(1)
        
        secondArg = None
        if len(cmdLineArgs) > 2: # check if second arg was passed
            secondArg = cmdLineArgs[2]
        
        match taskNumber:
            case 1:
                # call function for task 1
                pass
            case 2:
                # call function for task 2
                pass
            case 3:
                # call function for task 3
                pass
            case 4:
                # call function for task 4
                pass
            case 5:
                # call function for task 5
                pass
            case 6:
                # For task 6, get instructor ID from second argument and fetch their classes
                if secondArg:
                    instructor_id = checkForInteger(secondArg)
                    get_classes_by_instructor(instructor_id)
                else:
                    print("ERROR: Please provide an instructor ID.")
            case 7:
                # Calling function to caluclate active membership average age
                print("Calculating average age for active memerbships...")
                get_average_age_active_memerbship()

                # Calling function to calculate expired membership average age
                print("Calculating average age for expired memerbships...")
                get_average_age_expired_memerbship()
            case 8:
                # For task 8, get and display the top 3 instructors
                get_top_instructors() 
            case 9:
                # For task 9, get class type from second argument and display members who attended
                if secondArg:
                    class_type = secondArg
                    get_members_attended_classes(class_type)
                else:
                    print("ERROR: Please provide an class type.")
            case 10:
                # Display members who attended classes last month
                members_attended_classes_last_month()
                pass
            case default:
                # Handle invalid task number
                print("ERROR: The integer passed must be one from 1 to 10.")
                sys.exit(1)
    
    finally:
        if connection:
            connection.close()
        
if __name__ == "__main__":
    main()