from tabulate import tabulate
import json
import re # regex module for name validation

# ==========================================
# DATA (Global)
# ==========================================
students = []
courses_available = []


# ==========================================
# VALIDATION FUNCTIONS
# ==========================================
def validate_name(name):
    name = name.strip()
    if len(name) < 4:
        print("Error: Name is too short (minimum 4 characters).")
        return False
    if len(name.split()) < 2:
        print("Error: Please enter at least two words (e.g., First Last).")
        return False
    if any(char.isdigit() for char in name):
        print("Error: Name cannot contain numbers.")
        return False
    if not re.match(r"^[a-zA-Z\s\-\']+$", name): # checks if pattern matches from the start of string
        print(
            "Error: Name contains invalid characters. Only letters, spaces, hyphens, and apostrophes allowed."
        )
        return False
    return True


def validate_matric(matric):
    matric = matric.strip().upper()
    if len(matric) != 9:
        print("Error: Matric number must be exactly 9 characters long.")
        return False
    if not matric.startswith("A25AI"):
        print("Error: Matric number must start with 'A25AI'.")
        return False
    if not matric[5:].isdigit():
        print("Error: Last 4 digits of matric number must be numeric.")
        return False
    return matric


# ==========================================
# CORE FUNCTIONS
# ==========================================
def display_menu():
    print("\n" + "=" * 65)
    print("    STUDENT COURSE REGISTRATION & TIMETABLE BUILDER")
    print("=" * 65)
    print("1. Register New Student")
    print("2. Add Course")
    print("3. Drop Course")
    print("4. View Registered Courses")
    print("5. Generate Timetable")
    print("6. Save & Exit")
    print("-" * 65)


def check_credit_limit(current_credits, new_credit):
    if current_credits + new_credit > 21:
        print(
            f"Error: Cannot add! Exceeds 21 credits ({current_credits} + {new_credit} = {current_credits + new_credit})"
        )
        return False
    return True


def register_student():
    print("\n--- NEW STUDENT REGISTRATION ---")

    while True:
        name = input("Enter Full Name: ").title()
        if validate_name(name):
            break

    while True:
        matric_input = input("Enter Matric Number (e.g., A25AI1234): ")
        matric = validate_matric(matric_input)
        if matric:
            break

    # Check for duplicate matric
    if any(s["matric"] == matric for s in students):
        print("Error: This matric number is already registered!")
        return

    new_student = {
        "name": name,
        "matric": matric,
        "registered_courses": [],
        "total_credits": 0,
    }
    students.append(new_student)
    print(f"\nStudent {name} ({matric}) registered successfully!")

    # Force student to add courses until minimum 12 credits
    print("\nYou must register for at least 12 credits to complete registration.")
    while new_student["total_credits"] < 12:
        print(f"\nCurrent credits: {new_student['total_credits']}/12 required")
        add_course(matric)
        if new_student["total_credits"] >= 12:
            print("\nMinimum credit requirement met! You can now continue or exit.")


def find_student(matric):
    matric = matric.upper()
    for student in students:
        if student["matric"] == matric:
            return student
    print("Error: Student not found. Please register first (Option 1).")
    return None


def detect_clash(new_course, student):
    """Improved clash detection using proper time overlap logic"""
    for n_slot in new_course["slots"]:
        n_day, n_time = n_slot
        n_start_str, n_end_str = n_time.split("-")
        n_start = int(n_start_str.split(":")[0])
        n_end = int(n_end_str.split(":")[0])

        for reg_course in student["registered_courses"]:
            for r_slot in reg_course["slots"]:
                r_day, r_time = r_slot
                if n_day != r_day:
                    continue
                r_start_str, r_end_str = r_time.split("-")
                r_start = int(r_start_str.split(":")[0])
                r_end = int(r_end_str.split(":")[0])

                # Overlap if: max(start) < min(end)
                if max(n_start, r_start) < min(n_end, r_end):
                    print(
                        f"CLASH ALERT: Conflicts with {reg_course['code']} ({reg_course['name']}) on {n_day} {r_time}"
                    )
                    return True
    return False


def add_course(matric):
    student = find_student(matric)
    if not student:
        return

    print("\nAvailable Courses:")
    print(tabulate(courses_available, headers="keys", tablefmt="fancy_grid"))

    code = input("\nEnter course code to add: ").strip().upper()
    course = next((c for c in courses_available if c["code"] == code), None)

    if not course:
        print("Error: Course not found!")
        return

    if course in student["registered_courses"]:
        print("Error: You have already registered for this course!")
        return

    if not check_credit_limit(student["total_credits"], course["credit"]):
        return

    if detect_clash(course, student):
        print(f"Cannot add {course['code']} due to timetable clash.")
        return

    student["registered_courses"].append(course)
    student["total_credits"] += course["credit"]
    print(f"Course {course['code']} added successfully!")
    print(f"Total credits: {student['total_credits']}/21")


def drop_course(matric):
    student = find_student(matric)
    if not student:
        return

    if not student["registered_courses"]:
        print("No courses registered yet!")
        return

    print("\nYour Registered Courses:")
    print(
        tabulate(student["registered_courses"], headers="keys", tablefmt="fancy_grid")
    )

    code = input("\nEnter course code to drop: ").strip().upper()
    for i, c in enumerate(student["registered_courses"]):
        if c["code"] == code:
            if student["total_credits"] - c["credit"] < 12:
                print("Cannot drop! Would fall below minimum 12 credits required.")
                return
            removed = student["registered_courses"].pop(i)
            student["total_credits"] -= removed["credit"]
            print(f"Course {code} dropped successfully!")
            print(f"Total credits now: {student['total_credits']}/21")
            return
    print("Course not found in your registration!")


def view_registered_courses(matric):
    student = find_student(matric)
    if not student:
        return

    print(f"\nRegistered Courses for {student['name']} ({student['matric']}):")
    if not student["registered_courses"]:
        print("No courses registered yet.")
    else:
        print(
            tabulate(
                student["registered_courses"], headers="keys", tablefmt="fancy_grid"
            )
        )
    print(f"Total Credits: {student['total_credits']}/21")


def generate_timetable(matric):
    student = find_student(matric)
    if not student:
        return

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    timetable = {day: {f"{h:02d}:00": "---" for h in range(8, 17)} for day in days}

    for course in student["registered_courses"]:
        for slot in course["slots"]:
            day, time_range = slot
            if day not in days:
                continue
            start_str, end_str = time_range.split("-")
            start_h = int(start_str.split(":")[0])
            end_h = int(end_str.split(":")[0])
            for h in range(start_h, end_h):
                timetable[day][f"{h:02d}:00"] = course["code"]

    # Convert to list for tabulate
    table_data = []
    headers = ["Day"] + [f"{h:02d}:00" for h in range(8, 17)]
    for day in days:
        row = [day] + [timetable[day][f"{h:02d}:00"] for h in range(8, 17)]
        table_data.append(row)

    print(f"\nTimetable for {student['name']} ({student['matric']}):")
    print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))


def save_and_exit():
    with open("students.json", "w") as f:
        json.dump(students, f, indent=4)
    print("Data saved successfully. Goodbye!")


def load_data():
    global students, courses_available
    try:
        with open("students.json", "r") as f:
            students = json.load(f)
    except FileNotFoundError:
        print("No existing student data found. Starting fresh.")
        students = []

    try:
        with open("courses.json", "r") as f:
            courses_available = json.load(f)
    except FileNotFoundError:
        print("Error: courses.json not found! Please ensure it exists.")
        exit()


# ==========================================
# MAIN LOOP
# ==========================================
def main():
    load_data()
    print("Welcome to UTM AI Student Course Registration System")

    while True:
        display_menu()
        choice = input("Select an option (1-6): ").strip()

        if choice == "1":
            register_student()
        elif choice == "2":
            matric = input("Enter your Matric Number: ").strip()
            add_course(matric)
        elif choice == "3":
            matric = input("Enter your Matric Number: ").strip()
            drop_course(matric)
        elif choice == "4":
            matric = input("Enter your Matric Number: ").strip()
            view_registered_courses(matric)
        elif choice == "5":
            matric = input("Enter your Matric Number: ").strip()
            generate_timetable(matric)
        elif choice == "6":
            save_and_exit()
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
