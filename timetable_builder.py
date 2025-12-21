from tabulate import tabulate
import json
import re

# ==========================================
# DATA (Global)
# ==========================================
students = []
courses_available = []
current_student = None  # Tracks the logged-in student


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
    if not re.match(r"^[a-zA-Z\s\-\']+$", name):
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
    print("\n" + "=" * 70)
    print("    STUDENT COURSE REGISTRATION & TIMETABLE BUILDER")
    print("=" * 70)

    if current_student:
        print(f"Logged in as: {current_student['name']} ({current_student['matric']})")
    else:
        print("Status: No student logged in")

    print("\n1. Register New Student")
    print("2. Login")
    print("3. Add Course")
    print("4. Drop Course")
    print("5. View Registered Courses")
    print("6. Generate Timetable")
    print("7. Log Out")
    print("8. Save & Exit")
    print("-" * 70)


def check_credit_limit(current_credits, new_credit):
    if current_credits + new_credit > 21:
        print(
            f"Error: Cannot add! Exceeds 21 credits ({current_credits} + {new_credit} = {current_credits + new_credit})"
        )
        return False
    return True


def register_student():
    global current_student
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
    current_student = new_student  # Auto login after registration
    print(f"\nStudent {name} ({matric}) registered and logged in successfully!")
    print("\nYou must register for at least 12 credits.")
    while current_student["total_credits"] < 12:
        print(f"\nCurrent credits: {current_student['total_credits']}/12 required")
        add_course()
        if current_student["total_credits"] >= 12:
            print("\nMinimum credit requirement met!")


def login():
    global current_student
    if current_student:
        print("You are already logged in!")
        return

    matric_input = input("Enter your Matric Number: ").strip().upper()
    validated_matric = validate_matric(matric_input)
    if not validated_matric:
        return

    student = next((s for s in students if s["matric"] == validated_matric), None)
    if student:
        current_student = student
        print(f"Login successful! Welcome back, {student['name']}.")
    else:
        print("Student not found. Please register first.")


def logout():
    global current_student
    if not current_student:
        print("No one is logged in.")
        return
    print(f"Logged out from {current_student['name']}.")
    current_student = None


def require_login():
    if not current_student:
        print("Please login first (Option 2).")
        return False
    return True


def find_course_by_partial_code(partial_code):
    partial_code = partial_code.strip().upper()

    # Exact match first
    for course in courses_available:
        if course["code"] == partial_code:
            return course

    # SAIA + 4 digits
    if len(partial_code) == 4 and partial_code.isdigit():
        full_code = "SAIA" + partial_code
        for course in courses_available:
            if course["code"] == full_code:
                return course

    # Partial match in code
    for course in courses_available:
        if partial_code in course["code"]:
            return course

    return None


def detect_clash(new_course):
    for n_slot in new_course["slots"]:
        n_day, n_time = n_slot
        n_start_str, n_end_str = n_time.split("-")
        n_start = int(n_start_str.split(":")[0])
        n_end = int(n_end_str.split(":")[0])

        for reg_course in current_student["registered_courses"]:
            for r_slot in reg_course["slots"]:
                r_day, r_time = r_slot
                if n_day != r_day:
                    continue
                r_start_str, r_end_str = r_time.split("-")
                r_start = int(r_start_str.split(":")[0])
                r_end = int(r_end_str.split(":")[0])

                if max(n_start, r_start) < min(n_end, r_end):
                    print(
                        f"CLASH ALERT: Conflicts with {reg_course['code']} ({reg_course['name']}) on {n_day} {r_time}"
                    )
                    return True
    return False


def add_course():
    if not require_login():
        return

    print("\nAvailable Courses:")
    print(tabulate(courses_available, headers="keys", tablefmt="fancy_grid"))
    print("\nTip: Enter just the number (e.g., 1113 for SAIA1113, 1032 for ULRS1032)")

    code_input = input("\nEnter course code to add: ").strip()
    course = find_course_by_partial_code(code_input)

    if not course:
        print("Error: Course not found!")
        return

    print(f"Found: {course['code']} - {course['name']}")

    if course in current_student["registered_courses"]:
        print("Error: Already registered for this course!")
        return

    if not check_credit_limit(current_student["total_credits"], course["credit"]):
        return

    if detect_clash(course):
        print(f"Cannot add {course['code']} due to clash.")
        return

    current_student["registered_courses"].append(course)
    current_student["total_credits"] += course["credit"]
    print(f"Course {course['code']} added successfully!")
    print(f"Total credits: {current_student['total_credits']}/21")


def drop_course():
    if not require_login():
        return

    if not current_student["registered_courses"]:
        print("No courses registered yet!")
        return

    print("\nYour Registered Courses:")
    print(
        tabulate(
            current_student["registered_courses"], headers="keys", tablefmt="fancy_grid"
        )
    )
    print("\nTip: Enter just the number or full code")

    code_input = input("\nEnter course code to drop: ").strip()
    course = find_course_by_partial_code(code_input)

    if not course:
        print("Error: Course not found!")
        return

    if course not in current_student["registered_courses"]:
        print("Error: You are not registered for this course!")
        return

    if current_student["total_credits"] - course["credit"] < 12:
        print("Cannot drop! Would fall below minimum 12 credits.")
        return

    current_student["registered_courses"].remove(course)
    current_student["total_credits"] -= course["credit"]
    print(f"Course {course['code']} dropped successfully!")
    print(f"Total credits: {current_student['total_credits']}/21")


def view_registered_courses():
    if not require_login():
        return

    print(
        f"\nRegistered Courses for {current_student['name']} ({current_student['matric']}):"
    )
    if not current_student["registered_courses"]:
        print("No courses registered yet.")
    else:
        print(
            tabulate(
                current_student["registered_courses"],
                headers="keys",
                tablefmt="fancy_grid",
            )
        )
    print(f"Total Credits: {current_student['total_credits']}/21")


def generate_timetable():
    if not require_login():
        return

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    timetable = {day: {f"{h:02d}:00": "---" for h in range(8, 17)} for day in days}

    for course in current_student["registered_courses"]:
        for slot in course["slots"]:
            day, time_range = slot
            if day not in days:
                continue
            start_str, end_str = time_range.split("-")
            start_h = int(start_str.split(":")[0])
            end_h = int(end_str.split(":")[0])
            for h in range(start_h, end_h):
                timetable[day][f"{h:02d}:00"] = course["code"]

    table_data = []
    headers = ["Day"] + [f"{h:02d}:00" for h in range(8, 17)]
    for day in days:
        row = [day] + [timetable[day][f"{h:02d}:00"] for h in range(8, 17)]
        table_data.append(row)

    print(f"\nTimetable for {current_student['name']} ({current_student['matric']}):")
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
        choice = input("Select an option (1-8): ").strip()

        if choice == "1":
            register_student()
        elif choice == "2":
            login()
        elif choice == "3":
            add_course()
        elif choice == "4":
            drop_course()
        elif choice == "5":
            view_registered_courses()
        elif choice == "6":
            generate_timetable()
        elif choice == "7":
            logout()
        elif choice == "8":
            save_and_exit()
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
