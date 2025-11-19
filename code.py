import sqlite3
from datetime import datetime

# ------------------------------
# DATABASE CONNECTION
# ------------------------------
conn = sqlite3.connect("attendance.db")  
cursor = conn.cursor()

# ------------------------------
# TABLE CREATION
# ------------------------------
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    roll INTEGER PRIMARY KEY,
    name TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    roll INTEGER,
    date TEXT,
    status TEXT,
    FOREIGN KEY (roll) REFERENCES students(roll)
)
""")

conn.commit()

# ------------------------------
# FUNCTIONS
# ------------------------------

def add_student():
    roll = int(input("Enter Roll Number: "))
    name = input("Enter Name: ")
    cursor.execute("INSERT INTO students (roll, name) VALUES (?, ?)", (roll, name))
    conn.commit()
    print("Student added successfully!\n")

def mark_attendance():
    roll = int(input("Enter Roll Number: "))
    status = input("Enter Status (P/A): ").upper()
    date = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("INSERT INTO attendance (roll, date, status) VALUES (?, ?, ?)",
                   (roll, date, status))
    conn.commit()
    print("Attendance marked!\n")

def view_attendance():
    cursor.execute("SELECT * FROM attendance")
    rows = cursor.fetchall()
    print("\n--- Attendance Records ---")
    for r in rows:
        print(r)
    print()

def attendance_percentage():
    roll = int(input("Enter Roll Number: "))
    
    cursor.execute("SELECT COUNT(*) FROM attendance WHERE roll = ?", (roll,))
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM attendance WHERE roll = ? AND status='P'", (roll,))
    present = cursor.fetchone()[0]

    if total == 0:
        print("No attendance records found.\n")
    else:
        percent = (present / total) * 100
        print(f"Attendance Percentage: {percent:.2f}%\n")

def view_students():
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    print("\n--- Students List ---")
    for r in rows:
        print(r)
    print()

# ------------------------------
# MAIN MENU
# ------------------------------
while True:
    print("""
============================
   ATTENDANCE TRACKER
============================
1. Add Student
2. Mark Attendance
3. View Attendance Records
4. Attendance Percentage
5. View Students
6. Exit
""")

    choice = int(input("Enter your choice: "))

    if choice == 1:
        add_student()
    elif choice == 2:
        mark_attendance()
    elif choice == 3:
        view_attendance()
    elif choice == 4:
        attendance_percentage()
    elif choice == 5:
        view_students()
    elif choice == 6:
        print("Exiting...")
        break
    else:
        print("Invalid Choice! Try again.\n")

conn.close()
