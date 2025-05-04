"""
This python file is responsible for providing the graphical user interface (GUI) for the XYZ Gym Management System.
It is built using the PySimpleGUI library and interacts with an SQLite database to manage gym members and classes.

The key features of this GUI include:
- Displaying member information (ID, name, email, age, membership plan)
- Adding, updating, viewing, and deleting members, along with their payment details
- Displaying and managing gym classes (ID, name, type, duration, capacity, instructor, gym)
- Validating user input for all actions (e.g., age restrictions, valid dates, unique email checks)
- Interacting with the database via functions from the 'file.py' module, which handles database operations

The program utilizes SQLite as the database backend and provides and easy-to-use GUI to facilitate day-to-day management
tasks in the gym.

Authors: Alena Fischer, Devon Alonzo, Ludwig Scherer
Date: 04/28/2025
Last Updated: 4/28/2025
"""
import PySimpleGUI as sg 
import sqlite3     
import file

# sg.theme('DarkBlue')

sg.theme('Black')


# Fixed database name
DB_NAME = "XYZGym.sqlite"

def logout_and_exit(connection):
    """
    Closes the active database connection and exits the program.

    Parameters:
    - connection (sqlite3.Connection): The active connection to the database.
    """

    connection.close()
    exit()

def show_members_and_membership_plan(connection):
    """
    Displays a list of all members along with their corresponding membership plan and details.

    This function fetches data using the helper function `get_members_and_membership_plan`
    and displays it in a pop-up window using a PySimpleGUI table. It handles cases where
    the database returns no results or encounters a query failure.

    Parameters:
    - connection (sqlite3.Connection): The active connection to the database.
    """

    # Fetches the members and their membership plan details
    results = file.get_members_and_membership_plan(connection)

    # Message if the query fails or returns None
    if results is None:
        sg.popup("Database query failed or no members found.")
        return
    
    # Converts each row into a list for easier handling
    results = [list(row) for row in results]

    # Message if the result is empty
    if not results:
        sg.popup("No members found.")
        return
    
    # Define the table headings
    headings = ['MemberID', 'Name', 'Email', 'Age', 'Membership Plan']
    
    # Create the table layout
    layout = [[sg.Table(values=results, headings=headings, max_col_width=35,
                       auto_size_columns=True,
                       display_row_numbers=False,
                       justification='center',
                       num_rows=10,
                       key='-TABLE-',
                       row_height=35)]
    ]
    
    # Create the window and display the table
    window = sg.Window("Member Information", layout)
    event, _ = window.read()

    # Close the window after use
    window.close()

def add_new_member(connection):
    """
    Displays a form to add a new member and their initial payment.

    This function collects user input through a form and validates it:
    - Ensures all fields are filled
    - Enforces age restriction (15+)
    - Validates date logic (end > start)
    - Checks for unique email constraint

    On successful validation, it:
    - Inserts the member in to the Member table
    - Inserts an associated record into the Payment table

    Parameters:
    - connection (sqlite3.Connection): The active connection to the database.
    """

    # Define the form layout with input fields and buttons
    layout = [
        [sg.Text('Name'), sg.InputText(key='-NAME-')],
        [sg.Text('Email'), sg.InputText(key='-EMAIL-')],
        [sg.Text('Phone'), sg.InputText(key='-PHONE-')],
        [sg.Text('Address'), sg.InputText(key='-ADDRESS-')],
        [sg.Text('Age'), sg.InputText(key='-AGE-')],
        [sg.Text('Start Date (YYYY-MM-DD)'), sg.InputText(key='-START-')],
        [sg.Text('End Date (YYYY-MM-DD)'), sg.InputText(key='-END-')],
        [sg.Text('Plan ID'), sg.InputText(key='-PLANID-')],
        [sg.Text('Amount Paid'), sg.InputText(key='-AMOUNT-')],
        [sg.Text('Payment Date (YYYY-MM-DD)'), sg.InputText(key='-PAYDATE-')],
        [sg.Button('Submit'), sg.Button('Cancel')]
    ]

    # Create the input form window
    window = sg.Window('Add New Member', layout)
    
    while True:
        # Read user input and event
        event, values = window.read()
        
        # If the user closes the window or clicks Cancel
        if event in (sg.WIN_CLOSED, 'Cancel'):
            break
        elif event == 'Submit':                
                # Retreive the form values
                name = values['-NAME-']
                email = values['-EMAIL-']
                phone = is_integer(values['-PHONE-'], "phone number") # make sure phone number is integer
                address = values['-ADDRESS-']
                age = is_integer(values['-AGE-'], "age") # make sure integer input is given for age giled
                start_date = values['-START-']
                end_date = values['-END-']
                plan_id = is_integer(values['-PLANID-'], "plan id") # make sure plan id is an integer
                amount_paid = is_float(values['-AMOUNT-'], "payment")
                payment_date = values['-PAYDATE-']
                    
                # continue if any of the inputs were invalid
                if age is None or phone is None or plan_id is None or amount_paid is None:
                    continue

                # Valid age constraint (must be at least 15)
                if age < 15:
                    sg.popup_error("Age must be 15 or older.")
                    continue

                # Valid date logic (end must be after start)
                if start_date >= end_date:
                    sg.popup_error("End date must be later than start date.")
                    continue

                # Check if email already exists
                if file.check_email_exists(connection, email):
                    sg.popup_error("This email is already associated with an existing member.")
                    continue
                
                # Check if selected membership plan id exists
                if not file.membership_plan_exists(connection, plan_id):
                    sg.popup_error(
                        "Please enter a valid membership plan id. Options: \n",
                        *list(file.get_all_membership_plan_ids(connection))
                    )
                    continue

                # Ensure all fields of the form are filled
                if not (
                    name and email and phone and address and age and plan_id and amount_paid 
                    and start_date and end_date and payment_date
                ):
                    sg.popup_error("Please fill in all fields.")
                    continue
                
        # Try to add the member to the database
        member_id = file.add_member(connection, name, email, phone, address, int(age), start_date, end_date)
        if member_id:
            # If member added, attempt to record payment
            success = file.add_payment(connection, member_id, int(plan_id), float(amount_paid), payment_date)
            if success:
                sg.popup("Member and payment added successfully!")
                break
            else:
                sg.popup_error("Member added but payment failed.")
        else:
            sg.popup_error("Failed to add member.")

    # Close the form window
    window.close()

def update_member(connection):
    """
    Allows the user to update an existing member's details.

    The user inputs a member ID and the updated fields (name, email, etc.).
    Validates the member ID and ensures the member exists before proceeding.
    Calls the `update_member` function from the file module to apply changes.

    Parameters:
    - connection (sqlite2.Connection): The active connection to the database.
    """

    # Define the layout for updating member information
    layout = [
        [sg.Text('Enter Member ID to update'), sg.InputText(key='-ID-')],
        [sg.Text('New Name'), sg.InputText(key='-NAME-')],
        [sg.Text('New Email'), sg.InputText(key='-EMAIL-')],
        [sg.Text('New Phone'), sg.InputText(key='-PHONE-')],
        [sg.Text('New Address'), sg.InputText(key='-ADDRESS-')],
        [sg.Text('New Age'), sg.InputText(key='-AGE-')],
        [sg.Text('New Start Date (YYYY-MM-DD)'), sg.InputText(key='-START-')],
        [sg.Text('New End Date (YYYY-MM-DD)'), sg.InputText(key='-END-')],
        [sg.Button('Update'), sg.Button('Cancel')]
    ]

    # Create the window
    window = sg.Window('Update Member', layout)

    while True:
        # Read user input
        event, values = window.read()
        # If the user closes the window or clicks Cancel
        if event in (sg.WIN_CLOSED, 'Cancel'):
            break
        elif event == "Update":
            try:
                # Get and validate member ID
                member_id = int(values['-ID-'])

                # Check if the member exists
                if not file.member_exists(connection, member_id):
                    sg.popup_error("No member found with that ID.")
                    continue

                # Get updated values from the form
                name = values['-NAME-']
                email = values['-EMAIL-']
                phone = is_integer(values['-PHONE-'], "phone number")
                address = values['-ADDRESS-']
                age = is_integer(values['-AGE-'], "age")
                start_date = values['-START-']
                end_date = values['-END-']

                if phone is None or age is None: # make sure inputs are valid
                    continue

                # Valid age constraint (must be at least 15)
                if age < 15:
                    sg.popup_error("Age must be 15 or older.")
                    continue
                
                # Update the member in the database
                success = file.update_member(connection, member_id, name, email, phone, address, age, start_date, end_date)
                if success:
                    sg.popup("Member updated successfully!")
                else:
                    sg.popup_error("Failed to update member.")
            except Exception as e:
                sg.popup_error(f"Error: {e}")
            break

    # Close the window
    window.close()

def delete_member(connection):
    """
    Deletes a member from the database based on the entered member ID.

    This function prompts the user for a member ID, confirms the action,
    and then deletes the member using the `delete_member` helper function.

    Parameters:
    - connection (sqlite3.Connection): The active connection to the database.
    """

    # Define the layout for deleting the member
    layout = [
        [sg.Text('Enter Member ID to delete:'), sg.InputText(key='-ID-')],
        [sg.Button('Delete'), sg.Button('Cancel')]
    ]

    # Create the window
    window = sg.Window('Delete Member', layout)

    while True:
        # Read the user input
        event, values = window.read()
        # If the user closes the window or clicks Cancel
        if event in (sg.WIN_CLOSED, 'Cancel'):
            break
        elif event == 'Delete':
            try:
                # Get the member ID
                member_id = int(values['-ID-'])

                if not file.member_exists(connection, member_id):
                    sg.popup_error("No member found with that ID.")
                    continue

                # Confirm deleting the member
                confirm = sg.popup_yes_no("Are you sure you want to delete this member?")
                if confirm == 'Yes':
                    # If yes, attempt to delete the member
                    success = file.delete_member(connection, member_id)
                    if success:
                        sg.popup("Member deleted successfully.")
                    else:
                        sg.popup_error("Failed to delete member.")
            except ValueError:
                # Handle non-integer input
                sg.popup_error("Invalid ID.")
            break
    
    # Close the window
    window.close()

def display_all_classes(connection):
    """
    Displays all classes in a table format using PySimpleGUI.

    This function retreives all class records from the database and displays
    them in a scrollable table window. If no classes are found, a popup
    is displayed with a corresponding message.

    Parameters:
    - connection (sqlite3.Connection): The active connection to the database.
    """

    # Fetches all class information
    results = file.get_all_classes(connection)

    # Message if the result is empty
    if not results:
        sg.popup("No classes found.")
        return
    
    # Convert each row into a list for easier handling
    results = [list(row) for row in results]
    
    # Define the table headings
    headings = ['ClassID', 'Class Name', 'Class Type', 'Duration', 'Capacity', 'Instructor', 'Gym']
    
    # Create the table layout
    layout = [[sg.Table(values=results, headings=headings, max_col_width=35,
                       auto_size_columns=True,
                       display_row_numbers=False,
                       justification='center',
                       num_rows=10,
                       key='-TABLE-',
                       row_height=35)]
    ]
    
    # Create the window and wait for any event
    window = sg.Window("Class Information", layout)
    event, _ = window.read()

    # Close the window
    window.close()

def add_class(connection):
    """
    Opens a window to input new class information and adds the class to the database.

    This function prompts the user to enter all required class details. It validates
    constraints such as positive integers, required fields, and foreign key references.
    It calls the the `add_class` method from file.py and displays either a success or failure
    message accordingly.

    Parameters:
    - connection (sqlite3.Connection): The active connection to the database.
    """

    # Define the layout with input fields and buttons
    layout = [
        [sg.Text('Class Name'), sg.InputText(key='-NAME-')],
        [sg.Text('Class Type'), sg.Combo(['Yoga', 'Zumba', 'HIIT', 'Weights'], key='-TYPE-')],
        [sg.Text('Duration (in minutes)'), sg.InputText(key='-DURATION-')],
        [sg.Text('Class Capacity'), sg.InputText(key='-CAPACITY-')],
        [sg.Text('Instructor ID'), sg.InputText(key='-INSTRUCTORID-')],
        [sg.Text('Gym ID'), sg.InputText(key='-GYMID-')],
        [sg.Button('Submit'), sg.Button('Cancel')]
    ]

    # Create the window
    window = sg.Window('Add New Class', layout)

    while True:
        # Read user input and event
        event, values = window.read()

        # If the user closes the window or clicks Cancel
        if event in (sg.WIN_CLOSED, 'Cancel'):
            break
        elif event == 'Submit':
            # Retrieve the form values from the input fields
            name = values['-NAME-']
            class_type = values['-TYPE-']
            duration = int(values['-DURATION-'])
            capacity = int(values['-CAPACITY-'])
            instructor_id = int(values['-INSTRUCTORID-'])
            gym_id = int(values['-GYMID-'])

            # Validation - name should not be empty
            if not name:
                sg.popup_error("Class name cannot be empty.")
                continue

            # Validation - class type must be valid
            if class_type not in ['Yoga', 'Zumba', 'HIIT', 'Weights']:
                sg.popup_error("Class type must be one of: Yoga, Zumba, HIIT, Weights.")
                continue

            # Validation - duration should be a nonnegative integer
            try:
                duration = int(duration)
                if duration <= 0:
                    raise ValueError
            except ValueError:
                sg.popup_error("Duration must be a positive integer.")
                continue

            # Validation - capacity should be a nonnegative integer
            try:
                capacity = int(capacity)
                if capacity <= 0:
                    raise ValueError
            except ValueError:
                sg.popup_error("Class capacity must be a positive integer.")
                continue

            # Validation - the instructor ID must exist
            try:
                instructor_id = int(instructor_id)
                if not file.instructor_exists(connection, instructor_id):
                    sg.popup_error(f"Instructor ID {instructor_id} does not exist.")
                    continue
            except ValueError:
                sg.popup_error("Instructor ID must be a valid integer.")
                continue

            # Validation - gym ID must exist
            try:
                gym_id = int(gym_id)
                if not file.gym_exists(connection, gym_id):
                    sg.popup_error(f"Gym ID {gym_id} does not exist.")
                    continue
            except ValueError:
                sg.popup_error("Gym ID must be a valid integer.")
                continue

            # Attempt to add the class
            success = file.add_class(connection, name, class_type, duration, capacity, instructor_id, gym_id)
            if success:
                sg.popup("Class added successfully!")
                break
            else:
                sg.popup_error("Failed to add class.")
    
    # Close the window
    window.close()

def update_class(connection):
    """
    Opens a window to update details of an existing class in the database.
   
    The user provides a class ID and the updated class details.
    The function verifies that the class exists and validates user input.
    It then updates the class record using the `update_class` function from file.py

    Parameters:
    - connection (sqlite3.Connection): The active connection to the database.
    """

    # Define the layout for updating class information
    layout = [
        [sg.Text('Enter Class ID to update'), sg.InputText(key='-ID-')],
        [sg.Text('New Class Name'), sg.InputText(key='-NAME-')],
        [sg.Text('New Class Type'), sg.Combo(['Yoga', 'Zumba', 'HIIT', 'Weights'], key='-TYPE-')],
        [sg.Text('New Duration (in minutes)'), sg.InputText(key='-DURATION-')],
        [sg.Text('New Capacity'), sg.InputText(key='-CAPACITY-')],
        [sg.Text('New Instructor ID'), sg.InputText(key='-INSTRUCTORID-')],
        [sg.Text('New Gym ID'), sg.InputText(key='-GYMID-')],
        [sg.Button('Update'), sg.Button('Cancel')]
    ]

    # Create a window
    window = sg.Window('Update Class', layout)

    while True:
        # Read user input and event
        event, values = window.read()
        # If the user closes the window or clicks Cancel
        if event in (sg.WIN_CLOSED, 'Cancel'):
            break
        elif event == "Update":
            try:
                # Retrieve and validate the entered class ID
                class_id = int(values['-ID-'])

                # Check if the class exists in the database
                if not file.class_exists(connection, class_id):
                    sg.popup_error("No class found with that ID.")
                    continue

                # Get updated values from the form
                name = values['-NAME-']
                class_type = values['-TYPE-']
                duration = int(values['-DURATION-'])
                capacity = int(values['-CAPACITY-'])
                instructor_id = int(values['-INSTRUCTORID-'])
                gym_id = int(values['-GYMID-'])

                # Attempt to update the class in the database
                success = file.update_class(connection, class_id, name, class_type, duration, capacity, instructor_id, gym_id)
                if success:
                    sg.popup("Class updated successfully!")
                else:
                    sg.popup_error("Failed to update class.")
            except Exception as e:
                sg.popup_error(f"Error: {e}")
            break

    # Close the window
    window.close()

def delete_class(connection):
    """
    Opens a window to receive a class ID to delete from the database.

    This function prompts the user to input a class ID and check if any members are registered.
    If members are enrolled, deleted is prevented unless another class ID is provided to move the
    members to. Otherwise, the class is deleted using the `delete_class` function from file.py.

    Parameters:
    - connection (sqlite3.Connection): The active connection to the database.
    """

    # Define the layout for deleting a class
    layout = [
        [sg.Text('Enter Class ID to delete'), sg.InputText(key='-ID-')],
        [sg.Button('Delete'), sg.Button('Cancel')]
    ]

    # Create the window
    window = sg.Window('Delete Class', layout)

    while True:
        # Read user input and event
        event, values = window.read()
        # If the user closes the window or clicks Cancel
        if event in (sg.WIN_CLOSED, 'Cancel'):
            break
        elif event == "Delete":
            try:
                # Retrieve and validate the entered class ID
                class_id = int(values['-ID-'])

                # Check if the class exists in the database
                if not file.class_exists(connection, class_id):
                    sg.popup_error("No class found with that ID.")
                    continue

                # Check if the class has members
                if file.class_has_members(connection, class_id):
                    # Ask user to select another class to move members to
                    new_class_id = sg.popup_get_text("Enter a new class ID to move members to:")
                    # Move the members to the new class and delete the class
                    if new_class_id and file.move_members(connection, class_id, int(new_class_id)):
                        sg.popup("Members moved successfully. Deleting class now...")
                        if file.delete_class(connection, class_id):
                            sg.popup("Class deleted succesfully!")
                        else:
                            sg.popup_error("Failed to delete the class.")
                    else:
                        sg.popup_error("No valid class selected to move members to.")
                else:
                    # If there are no members in the class, delete directly
                    if file.delete_class(connection, class_id):
                        sg.popup("Class deleted successfully!")
                    else:
                        sg.popup_error("Failed to delete the class.")
            except Exception as e:
                sg.popup_error(f"Error: {e}")
            break

    # Close the window
    window.close()

def find_members_by_class(connection):
    """
    Displays a list of all members registered in a specific class.

    Prompts the user to enter a class ID, fetches associated members, and
    displays them in a table. Handles validation for non-existent classes.

    Parameters:
    - connection (sqlite3.Connection): The active connection to the database.
    """

    # Define the layout
    layout = [
        [sg.Text('Enter Class ID:'), sg.InputText(key='-CLASSID-')],
        [sg.Button('Search'), sg.Button('Cancel')]
    ]

    # Create the window
    window = sg.Window('Find Members by Class', layout)

    while True:
        # Read user input and event
        event, values = window.read()
        # If the user closes the window or clicks Cancel
        if event in (sg.WIN_CLOSED, 'Cancel'):
            break
        elif event == 'Search':
            try:
                # Retrieve and validate the entered class ID
                class_id = int(values['-CLASSID-'])
                results = file.get_members_in_class(connection, class_id)

                # Message is displayed if there are no members in the given class
                if not results:
                    sg.popup("No members found for this class.")
                # If there are members, create a table
                else:
                    # Define the table headings
                    headings = ['Member ID', 'Name', 'Email', 'Age']
                    # Convert each row into a list for easier handling
                    data = [list(row) for row in results]
                    # Create the window with the table
                    sg.Window('Members in Class', [[
                        sg.Table(values=data, headings=headings,
                                 auto_size_columns=True,
                                 justification='center',
                                 num_rows=10)
                    ]]).read(close=True)

            except ValueError:
                sg.popup_error("Invalid Class ID.")

    # Close the window
    window.close()

def list_classes_and_attendance(connection):
    """
    Lists all classes alon with their current number of registered members.

    This function retrieves class attendance information and displays it in
    a table format. It uses `get_classes_with_attendance` from file.py.

    Parameters:
    - connection (sqlite3.Connection): The active connection to the database.
    """

    # Fetches all class data from file.py ***
    results = file.get_classes_with_attendance(connection)

    # Message displayed if results are empty
    if not results:
        sg.popup("No classes or attendance data found.")
        return
    
    # Convert each row into a list for easier handling
    results = [list(row) for row in results]
    
    # Define the headings
    headings = ['Class ID', 'Name', 'Type', 'Duration', 'Capacity', '# of Attendees']

    # Define the layout with the table
    layout = [[sg.Table(values=results, headings=headings, max_col_width=35,
                       auto_size_columns=True,
                       display_row_numbers=False,
                       justification='center',
                       num_rows=10,
                       key='-TABLE-',
                       row_height=35)]
    ]

    # Create the window and wait for any event
    window = sg.Window("Class Attendance", layout)
    event, _ = window.read()
    window.close() # Close the window


def display_all_equipment(connection):
    """
    Displays all equipment in a table format using PySimpleGUI.

    This function retreives all equipment records from the database and displays
    them in a scrollable table window. If no equipment is found, a popup
    is displayed with a corresponding message.

    Parameters:
    - connection (sqlite3.Connection): The active connection to the database.
    """

    # Fetches all equipment information
    results = file.get_all_equipment(connection)

    # Message if the result is empty
    if not results:
        sg.popup("No equipment found.")
        return
    
    # Convert each row into a list for easier handling
    results = [list(row) for row in results]
    
    # Define the table headings
    headings = ['EquipmentID', 'Equipment Name', 'Equipment Type', 'Quantity', 'Gym']
    
    # Create the table layout
    layout = [[sg.Table(values=results, headings=headings, max_col_width=35,
                       auto_size_columns=True,
                       display_row_numbers=False,
                       justification='center',
                       num_rows=10,
                       key='-TABLE-',
                       row_height=35)]
    ]

     # Create the window and wait for any event
    window = sg.Window("Equipment Information", layout)
    event, _ = window.read()

    # Close the window
    window.close()


def add_equipment(connection):
    """
    Opens a window to input new equipment information and adds the equipment to the database.

    This function prompts the user to enter all required equipment details. It validates
    constraints such as positive integers, required fields, and foreign key references.
    It calls the the `add_equipment` method from file.py and displays either a success or failure
    message accordingly.

    Parameters:
    - connection (sqlite3.Connection): The active connection to the database.
    """

    # Define the layout with input fields and buttons
    layout = [
        [sg.Text('Equipment Name'), sg.InputText(key='-NAME-')],
        [sg.Text('Equipment Type'), sg.Combo(['Cardio', 'Strength', 'Flexibility', 'Recovery'], key='-TYPE-')],
        [sg.Text('quantity'), sg.InputText(key='-QUANTITY-')],
        [sg.Text('Gym ID'), sg.InputText(key='-GYMID-')],
        [sg.Button('Submit'), sg.Button('Cancel')]
    ]

    window = sg.Window('Add New Equipment', layout)

    while True:
        # Read user input and event
        event, values = window.read()

        # If the user closes the window or clicks Cancel
        if event in (sg.WIN_CLOSED, 'Cancel'):
            break
        elif event == 'Submit':
            # Retrieve the form values from the input fields
            name = values['-NAME-']
            equipment_type = values['-TYPE-']
            quantity = int(values['-QUANTITY-'])
            gym_id = int(values['-GYMID-'])

            # Validation - name should not be empty
            if not name:
                sg.popup_error("Equipment name cannot be empty.")
                continue

            # Validation - equipment type must be valid
            if equipment_type not in ['Cardio', 'Strength', 'Flexibility', 'Recovery']:
                sg.popup_error("Class type must be one of: Cardio, Strength, Flexibility, Recovery.")
                continue

            # Validation - quantity should be a nonnegative integer
            try:
                quantity = int(quantity)
                if quantity <= 0:
                    raise ValueError
            except ValueError:
                sg.popup_error("Quantity must be a positive integer.")
                continue


            # Validation - gym ID must exist
            try:
                gym_id = int(gym_id)
                if not file.gym_exists(connection, gym_id):
                    sg.popup_error(f"Gym ID {gym_id} does not exist.")
                    continue
            except ValueError:
                sg.popup_error("Gym ID must be a valid integer.")
                continue

            # Attempt to add the class
            success = file.add_equipment(connection, name, equipment_type, quantity, gym_id)
            if success:
                sg.popup("Equipment added successfully!")
                break
            else:
                sg.popup_error("Failed to add class.")
    
    # Close the window
    window.close()

def update_equipment(connection):
    """
    Opens a window to update details of an existing piece of equipment in the database.
   
    The user provides an equipment ID and the updated equipment details.
    The function verifies that the equipment exists and validates user input.
    It then updates the equipment record using the `update_equipment` function from file.py

    Parameters:
    - connection (sqlite3.Connection): The active connection to the database.
    """

    # Define the layout for updating class information
    layout = [
        [sg.Text('Enter Equipment ID to update'), sg.InputText(key='-ID-')],
        [sg.Text('New Equipment Name'), sg.InputText(key='-NAME-')],
        [sg.Text('New Equipment Type'), sg.Combo(['Cardio', 'Strength', 'Flexibility', 'Recovery'], key='-TYPE-')],
        [sg.Text('New quantity'), sg.InputText(key='-QUANTITY-')],
        [sg.Text('New Gym ID'), sg.InputText(key='-GYMID-')],
        [sg.Button('Update'), sg.Button('Cancel')]
    ]

    # Create a window
    window = sg.Window('Update Equipment', layout)

    while True:
        # Read user input and event
        event, values = window.read()
        # If the user closes the window or clicks Cancel
        if event in (sg.WIN_CLOSED, 'Cancel'):
            break
        elif event == "Update":
            try:
                # Retrieve and validate the entered class ID
                equipment_id = int(values['-ID-'])

                # Check if the class exists in the database
                if not file.equipment_exists(connection, equipment_id):
                    sg.popup_error("No equipment found with that ID.")
                    continue

                # Get updated values from the form
                name = values['-NAME-']
                equipment_type = values['-TYPE-']
                quantity = int(values['-QUANTITY-'])
                gym_id = int(values['-GYMID-'])

                # Attempt to update the class in the database
                success = file.update_equipment(connection, equipment_id, name, equipment_type, quantity, gym_id)
                if success:
                    sg.popup("Equipment updated successfully!")
                else:
                    sg.popup_error("Failed to update equipment.")
            except Exception as e:
                sg.popup_error(f"Error: {e}")
            break

    # Close the window
    window.close()

def delete_equipment(connection):
    """
    Opens a window to receive a equipment ID to delete from the database.

    The user provides an equipment ID to check to make sure it exists in the database.
    If it does then it is deleted from the database using the 'delete_equipment' function
    from file.py

    Parameters:
    - connection (sqlite3.Connection): The active connection to the database.
    """

    # Define the layout for deleting a class
    layout = [
        [sg.Text('Enter Equipment ID to delete'), sg.InputText(key='-ID-')],
        [sg.Button('Delete'), sg.Button('Cancel')]
    ]

    # Create the window
    window = sg.Window('Delete Equipment', layout)


    while True:
        # Read the user input
        event, values = window.read()
        # If the user closes the window or clicks Cancel
        if event in (sg.WIN_CLOSED, 'Cancel'):
            break
        elif event == 'Delete':
            try:
                # Get the member ID
                equipment_id = int(values['-ID-'])
                
                # Check if the class exists in the database
                if not file.equipment_exists(connection, equipment_id):
                    sg.popup_error("No equipment found with that ID.")
                    continue

                # Confirm deleting the member
                confirm = sg.popup_yes_no("Are you sure you want to delete this equipment?")
                if confirm == 'Yes':
                    # If yes, attempt to delete the member
                    success = file.delete_equipment(connection, equipment_id)
                    if success:
                        sg.popup("Equipment deleted successfully.")
                    else:
                        sg.popup_error("Failed to delete equipment.")

            except ValueError:
                # Handle non-integer input
                sg.popup_error("Invalid ID.")
            break
    
    # Close the window
    window.close()

# Main menu for the system
def main_menu():
    """
    Displays the main menu for the XYZGym Management System.

    Returns:
    - event (str): The button clicked by the user.
    """

    # Define the layout for the Main Menu
    layout = [
        [sg.Button('Members Menu')],
        [sg.Button('Classes Menu')],
        [sg.Button('Equipment Menu')],
        [sg.Button('Logout and Exit')]
    ]

    # Create the window with the layout
    window = sg.Window('Gym Management System', layout)
    event, _ = window.read()
    window.close() # Close the window
    return event # Return the event

def members_menu(connection):
    """
    Displays the Members Menu and handles member-related actions.

    Parameters:
    - connection (sqlite3.Connection): The active connection to the database.
    """

    # Define the layour for the Members Menu
    layout = [
        [sg.Button('Display All Members')],
        [sg.Button('Add New Member')],
        [sg.Button('Update Member')],
        [sg.Button('Delete Member')],
        [sg.Button('Return to Main Menu')],
        [sg.Button('Logout and Exit')]
    ]

    # Create the window
    window = sg.Window('Members Menu', layout)

    while True:
        # Read user input and event
        event, values = window.read()

        # If the user closes the window or clicks 'Logout and Exit'
        if event == sg.WINDOW_CLOSED or event == "Logout and Exit":
            window.close()
            logout_and_exit(connection)
            break
        # Returns user to the main menu
        elif event == "Return to Main Menu":
            window.close()
            return
        # Option 1 - View all members in the database
        elif event == "Display All Members":
            show_members_and_membership_plan(connection)
        # Option 2 - Add a new member to the database
        elif event == "Add New Member":
            add_new_member(connection)
        # Option 3 - Update a member's information in the database
        elif event == "Update Member":
            update_member(connection)
        # Option 4 - Delete a member from the database
        elif event == "Delete Member":
            delete_member(connection)

    # Close the window
    window.close()

def classes_menu(connection):
    """
    Displays the Classes Menu and handles class-related actions.

    Parameters:
    - connection (sqlite3.Connection): The active connecion to the database.
    """

    # Define the layout for the Classes Menu
    layout = [
        [sg.Button('Display All Classes')],
        [sg.Button('Add New Class')],
        [sg.Button('Update Class')],
        [sg.Button('Delete Class')],
        [sg.Button('List Classes with Attendance')],
        [sg.Button('Find Members by Class')],
        [sg.Button('Return to Main Menu')],
        [sg.Button('Logout and Exit')]
    ]

    # Create the window
    window = sg.Window('Classes Menu', layout)

    while True:
        # Read user input and event
        event, values = window.read()

        # If the user closes the window or clicks 'Logout and Exit'
        if event == sg.WINDOW_CLOSED or event == "Logout and Exit":
            window.close()
            logout_and_exit(connection)
            break
        # Returns user to main menu
        elif event == "Return to Main Menu":
            window.close()
            return
        # Option 1 - View all classes in the database
        elif event == "Display All Classes":
            display_all_classes(connection)
        # Option 2- Add new class to the database
        elif event == "Add New Class":
            add_class(connection)
        # Option 3 - Update class information in the databse
        elif event == "Update Class":
            update_class(connection)
        # Option 4 - Delete a class from the database
        elif event == "Delete Class":
            delete_class(connection)
        # Option 5 - List classes with member attendance
        elif event == "List Classes with Attendance":
            list_classes_and_attendance(connection)
        # Option 6 - Display members by class
        elif event == "Find Members by Class":
            find_members_by_class(connection)

    # Close window
    window.close()

def equipment_menu(connection):
    # Define the layout for the Classes Menu
    layout = [
        [sg.Button('Display All Equipment')],
        [sg.Button('Add New Equipment')],
        [sg.Button('Update Equipment')],
        [sg.Button('Delete Equipment')],
        [sg.Button('Return to Main Menu')],
        [sg.Button('Logout and Exit')]
    ]

    # Create the window
    window = sg.Window('Equipment Menu', layout)

    

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == "Logout and Exit":
            window.close()
            logout_and_exit(connection)
            break
        # Returns user to main menu
        elif event == "Return to Main Menu":
            window.close()
            return
        # Option 1 - View all classes in the database
        elif event == "Display All Equipment":
            display_all_equipment(connection)
        # Option 2- Add new class to the database
        elif event == "Add New Equipment":
            add_equipment(connection)
        # Option 3 - Update class information in the databse
        elif event == "Update Equipment":
            update_equipment(connection)
        # Option 4 - Delete a class from the database
        elif event == "Delete Equipment":
            delete_equipment(connection)

def run_program():
    """
    Runs the XYZGym Management System program.
    Establishes a database conncetion and displays the main menu.
    """

    # Establish connection to the database
    connection = file.connectToDatabase()
    if connection:
        while True:
            # Initially display the main menu
            event = main_menu()

            # 1. Members Menu
            if event == 'Members Menu':
                members_menu(connection)

            # 2. Classes Menu
            elif event == 'Classes Menu':
                classes_menu(connection)

            # 3. Equipment Menu
            elif event == 'Equipment Menu':
                equipment_menu(connection)
            
            # 4. Exit from the program
            elif event == 'Logout and Exit':
                logout_and_exit(connection)
                break
            
def is_integer(input, input_field_name):
    if not input.strip():
        sg.popup_error(f"ERROR: The {input_field_name} field cannot be empty.")
        return None
    try:
        return int(input)
    except ValueError:
        sg.popup_error(f"ERROR: Only integer numbers allowed in {input_field_name} field.")
        return None
    
def is_float(input, input_field_name):
    if not input.strip():
        sg.popup_error(f"ERROR: The {input_field_name} field cannot be empty.")
        return None
    try:
        return float(input)
    except ValueError:
        sg.popup_error(f"ERROR: Only decimal numbers allowed in {input_field_name} field.")
        return None

# Run the program
if __name__ == '__main__':
    run_program()
