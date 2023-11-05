import sqlite3
import csv

conn = sqlite3.connect('/Users/rithikamuthukali/PycharmProjects/assignment1/StudentDB.db') #establish connection to db
mycursor = conn.cursor()
# Create the "student" table if it doesn't exist
mycursor.execute("""
    CREATE TABLE IF NOT EXISTS student (
        StudentId INTEGER PRIMARY KEY,
        FirstName TEXT,
        LastName TEXT,
        GPA REAL,
        Major TEXT,
        FacultyAdvisor TEXT,
        Address TEXT,
        City TEXT,
        State TEXT,
        ZipCode TEXT,
        MobilePhoneNumber TEXT,
        isDeleted TEXT
    )
""")
conn.commit()
"""
# CSV file to import
studentData = "students.csv"
# Open and read the CSV file
with open(studentData, 'r') as csvfile:
    csvreader = csv.reader(csvfile)

    # Skip the first row (header) of the CSV file
    next(csvreader)

    # Iterate over the CSV data and insert it into the "student" table
    for row in csvreader:
        # Rearrange the data based on the correct order of columns in the "student" table
        rearranged_data = [
            row[0],  # FirstName
            row[1],  # LastName
            row[8],  # GPA
            row[7],  # Major
            '',  # FacultyAdvisor (empty because not available in the CSV)
            row[2],  # Address
            row[3],  # City
            row[4],  # State
            row[5],  # ZipCode
            row[6],  # MobilePhoneNumber
            ''  # isDeleted (empty because not available in the CSV)
        ]

        mycursor.execute("INSERT INTO student (FirstName, LastName, GPA, Major, FacultyAdvisor, Address, City, State, ZipCode, MobilePhoneNumber, isDeleted) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ", rearranged_data)
        conn.commit()
"""

while True:
        print("\n")
        print("Student Database Menu:")
        print("1. Display students")
        print("2. Add a student")
        print("3. Update a student")
        print("4. Delete a student")
        print("5. Search a student based on Major, GPA, City, State, and Advisor ")
        print("6. Exit")

        choice = input("Enter your choice (1/2/3/4/5/6): ")

        if choice == '1':
            mycursor.execute("SELECT * FROM student")
            rows = mycursor.fetchall()
            for row in rows:
                print(row)
        elif choice == '2':
            # Collect user input for all attributes
            FirstName = input("Enter the student's first name: ")
            LastName = input("Enter the student's last name: ")
            GPA = input("Enter the student's GPA: ")
            Major = input("Enter the student's major: ")
            FacultyAdvisor = input("Enter the faculty advisor: ")
            Address = input("Enter the student's address: ")
            City = input("Enter the city: ")
            State = input("Enter the state: ")
            ZipCode = input("Enter the ZIP code: ")
            MobilePhoneNumber = input("Enter the mobile phone number: ")

            # Validate the GPA input
            try:
                GPA = float(GPA)
            except ValueError:
                print("Invalid GPA. Please enter a numeric value for GPA.")
                conn.close()
                exit()

            # Insert the new student into the "student" table
            mycursor.execute("""
                INSERT INTO student (FirstName, LastName, GPA, Major, FacultyAdvisor, Address, City, State, ZipCode, MobilePhoneNumber, isDeleted)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
            FirstName, LastName, GPA, Major, FacultyAdvisor, Address, City, State, ZipCode, MobilePhoneNumber, ''))
            conn.commit()
        elif choice == '3':
            # Prompt the user for the StudentId of the student to update
            student_id = input("Enter the StudentId of the student to update: ")

            # Check if the provided StudentId exists in the database
            mycursor.execute("SELECT * FROM student WHERE StudentId = ?", (student_id,))
            existing_student = mycursor.fetchone()

            if existing_student is None:
                print("Student not found. No records updated.")
            else:
                # Prompt the user for the fields to update
                major = input("Enter the new major: ")
                faculty_advisor = input("Enter the new faculty advisor: ")
                mobile_phone_number = input("Enter the new mobile phone number: ")

                # Update the specified fields for the student
                mycursor.execute("""
                        UPDATE student
                        SET Major = ?, FacultyAdvisor = ?, MobilePhoneNumber = ?
                        WHERE StudentId = ?
                    """, (major, faculty_advisor, mobile_phone_number, student_id))

                conn.commit()
                print("Student record updated successfully.")
        elif choice == '4':
            student_id = input("Enter the StudentId of the student to delete: ")
            # Check if the provided StudentId exists in the database
            mycursor.execute("SELECT * FROM student WHERE StudentId = ?", (student_id,))
            existing_student = mycursor.fetchone()

            if existing_student is None:
                print("Student not found. No records deleted.")
            else:
                # Perform a "soft" delete by setting isDeleted to 1 (true)
                mycursor.execute("""
                        UPDATE student
                        SET isDeleted = 1
                        WHERE StudentId = ?
                    """, (student_id,))

                conn.commit()
                print("Student record deleted (soft delete).")
        elif choice == '5':
            major = input("Enter Major (leave empty to skip): ")
            gpa = input("Enter GPA (leave empty to skip): ")
            city = input("Enter City (leave empty to skip): ")
            state = input("Enter State (leave empty to skip): ")
            advisor = input("Enter Advisor (leave empty to skip): ")

            # Construct a dynamic query with the provided attributes
            query = "SELECT * FROM student WHERE 1=1"
            params = []

            if major:
                query += " AND Major = ?"
                params.append(major)
            if gpa:
                query += " AND GPA = ?"
                params.append(float(gpa))
            if city:
                query += " AND City = ?"
                params.append(city)
            if state:
                query += " AND State = ?"
                params.append(state)
            if advisor:
                query += " AND FacultyAdvisor = ?"
                params.append(advisor)

            mycursor.execute(query, params)

            # Retrieve and display the search results
            results = mycursor.fetchall()

            if not results:
                print("No matching students found.")
            else:
                for row in results:
                    print(f"StudentId: {row[0]}, FirstName: {row[1]}, LastName: {row[2]}, Major: {row[3]}")
        elif choice == '6':
            conn.close()
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter a valid option.")
