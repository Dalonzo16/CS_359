"""
This python file contains a program that - when executed, accepts an integer number from 1 to 10
as a command line argument. For the numbers 3, 4, 6, and 9, an additional argument being the 
<classId>, <type>, <instructorId>, and <classType> respectively, is required to be passed as well. 

Authors: Alena Fischer, Devon Alonzo, Ludwig Scherer
Date: 03/23/2025
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
    
    except:
        print("ERROR: Database connection unsuccessful.")
        sys.exit(1) # terminate program if connection fails
        
def checkForInteger(inputToCheck):
    
    if inputToCheck.isdigit():
        return int(inputToCheck)
    else:
        print("ERROR: The first parameter need to be a positive integer from 1 to 10.")
        sys.exit(1)
        
        
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
                # call function for task 6
                pass
            case 7:
                # call function for task 7
                pass
            case 8:
                # call function for task 8
                pass
            case 9:
                # call function for task 9
                pass
            case 10:
                # call function for task 10
                pass
            case default:
                print("ERROR: The integer passed must be one from 1 to 10.")
                sys.exit(1)
    
    finally:
        if connection:
            connection.close()
        
if __name__ == "__main__":
    main()