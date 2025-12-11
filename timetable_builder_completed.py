import json

courses_available = [
    {
        "code": "SAIA1113",
        "name": "PYTHON PROGRAMMING",
        "credit": 3,
        "slots": {"day": "Monday", "time": "08:00-10:00"},
        "location": "Lecture Room 1, Lvl 15",
    },
    {
        "code": "SAIA1143",
        "name": "DISCRETE MATHEMATICS",
        "credit": 3,
        "slots": {"day": "Tuesday", "time": "08:00-10:00"},
        "location": "Lecture Room 1, Lvl 15",
    },
    {
        "code": "SAIA1013",
        "name": "RESPONSIBLE AI AND ETHICS",
        "credit": 3,
        "slots": {"day": "Tuesday", "time": "14:00-16:00"},
        "location": "Seminar Room 3, BATC",
    },
    {
        "code": "SAIA1123",
        "name": "INTRODUCTION TO AI",
        "credit": 3,
        "slots": {"day": "Wednesday", "time": "08:00-10:00"},
        "location": "Lecture Room 1, Lvl 15",
    },
    {
        "code": "ULRS1032",
        "name": "INTEGRITY AND ANTI-CORRUPTION",
        "credit": 2,
        "slots": {"day": "Wednesday", "time": "10:00-12:00"},
        "location": "Lecture Room 1, Lvl 15",
    },
    {
        "code": "SAIA1133",
        "name": "DATA MANAGEMENT",
        "credit": 3,
        "slots": {"day": "Wednesday", "time": "12:00-14:00"},
        "location": "Lecture Room 1, Lvl 15",
    },
    {
        "code": "SAIA1153",
        "name": "MATHEMATICS FOR ML",
        "credit": 3,
        "slots": {"day": "Thursday", "time": "08:00-10:00"},
        "location": "Lecture Room 2, Lvl 15",
    },
]

student = {"name": "", "matric": "", "registered_courses": [], "total_credits": 0}

# ==========================================
#        BRAD
# ==========================================
# FUNCTIONS:
# 1. display_menu()
# 2. add_course()
# 3. remove_course() (mapped to drop_course)
# 4. check_credit_limit()


def display_menu():
    """Display the main menu – called every loop"""
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
    """Return True if adding course keeps total <= 21"""
    if current_credits + new_credit > 21:
        print(
            f"Error: Cannot add! Exceeds 21 credits ({current_credits} + {new_credit} = {current_credits + new_credit})"
        )
        return False
    return True


def register_student():
    """Helper function for Member A (Option 1)"""
    print("\n--- NEW STUDENT REGISTRATION ---")

    # 1. Name Validation Loop
    while True:
        name_input = input("Enter Name: ").strip()
        if len(name_input) < 3:
            print("Error: Name too short! and please fill in your full name!")
        else:
            student["name"] = name_input
            break

    # 2. Matric Validation Loop
    while True:
        matric_input = input("Enter Matric Number: ").strip().upper()
        if not matric_input.startswith("A25"):
            print("Error: Matric number must start with 'A25'.")
        else:
            student["matric"] = matric_input
            break

    student["registered_courses"] = []
    student["total_credits"] = 0
    print(f"Student {student['name']} registered successfully!")


def add_course():
    """Add a course with full validation"""
    if not student["name"]:
        print("Please register student first (Option 1)!")
        return

    # 1. Display list
    print("\nAvailable Courses (Year 1, Sem 1):")
    for c in courses_available:
        print(f"{c['code']} - {c['name']} ({c['slots']['day']} {c['slots']['time']})")

    code = input("\nEnter course code to add: ").strip().upper()

    # 2. Find course
    course = None
    for c in courses_available:
        if c["code"] == code:
            course = c
            break

    if not course:
        print("Course not found!")
        return

    # 3. Validation: Check if already registered
    if course in student["registered_courses"]:
        print("You already added this course!")
        return

    # 4. Validation: Credits
    if not check_credit_limit(student["total_credits"], course["credit"]):
        return

    # 5. Validation: Clashes
    # INTEGRATION POINT: Member A calls Member B's function here
    if detect_clash(course):
        print(f"TIMETABLE CLASH DETECTED! Cannot add {course['code']}.")
        return

    # 6. Finalize Add
    student["registered_courses"].append(course)
    student["total_credits"] += course["credit"]
    print(f"Course {course['code']} added successfully!")
    print(f"Total credits: {student['total_credits']}/21")


def drop_course():
    """Remove a registered course"""
    if not student["registered_courses"]:
        print("No courses registered yet!")
        return

    code = input("\nEnter course code to drop: ").strip().upper()

    found = False
    for i in range(len(student["registered_courses"])):
        # access the course manually using the index 'i'
        c = student["registered_courses"][i]

        if c["code"] == code:
            removed = student["registered_courses"].pop(i)
            student["total_credits"] -= removed["credit"]
            print(f"Course {code} dropped successfully!")
            print(f"Total credits now: {student['total_credits']}/21")
            found = True
            break

    if not found:
        print("Course not found in your registration!")


def view_registered_courses():
    """Helper for Option 4"""
    if not student["registered_courses"]:
        print("\nNo courses registered.")
    else:
        print(f"\nRegistered Courses for {student['name']}:")
        for c in student["registered_courses"]:
            print(f"- {c['code']}: {c['name']} ({c['credit']} credits)")
        print(f"Total Credits: {student['total_credits']}")


# ==========================================
#        IDRIS
# ==========================================
# FUNCTIONS:
# 1. detect_clash(student, new_course)
# 2. generate_timetable(student)
# 3. display_timetable(timetable)


def detect_clash(new_course):
    """
    Checks if new_course time slot overlaps with any registered course.
    Returns True if a clash exists.
    """
    new_day = new_course["slots"]["day"]
    new_time = new_course["slots"]["time"]

    for registered in student["registered_courses"]:
        reg_day = registered["slots"]["day"]
        reg_time = registered["slots"]["time"]

        # If Day matches AND Time matches
        if new_day == reg_day and new_time == reg_time:
            print(
                f"CLASH ALERT: New course conflicts with {registered['code']} ({registered['name']})"
            )
            return True

    return False


def generate_timetable(student_dict):
    """
    Prepares the timetable data.
    Logic: Sorts the registered courses by Day of the week.
    """
    timetable = student_dict["registered_courses"]

    # Helper dict to sort days correctly (Mon=1, Tue=2...)
    days_order = {"Monday": 1, "Tuesday": 2, "Wednesday": 3, "Thursday": 4, "Friday": 5}

    # Sort the list based on the day order
    timetable.sort(key=lambda x: days_order.get(x["slots"]["day"], 6))

    return timetable


def display_timetable(timetable):
    """Displays the formatted table"""
    if not timetable:
        print("\nTimetable is empty. Register for courses first.")
        return

    print("\n" + "=" * 95)
    print(
        f"{'DAY':<12} | {'TIME':<15} | {'CODE':<10} | {'LOCATION':<25} | {'COURSE NAME'}"
    )
    print("-" * 95)

    for course in timetable:
        print(
            f"{course['slots']['day']:<12} | {course['slots']['time']:<15} | {course['code']:<10} | {course['location']:<25} | {course['name']}"
        )

    print("=" * 95)


# ==========================================
#        BONUS / SHARED TASK
# ==========================================
# Responsibilities: save_to_file / load_from_file


def save_to_file():
    """Saves student data to JSON"""
    filename = "student_data.json"
    try:
        with open(filename, "w") as file:
            json.dump(student, file, indent=4)
        print(f"\nData saved successfully to {filename}")
    except Exception as e:
        print(f"Error saving file: {e}")


# ==========================================
#        MAIN PROGRAM LOOP
# ==========================================


def main():
    while True:
        display_menu()  # Member A function
        choice = input("Enter selection (1-6): ")

        if choice == "1":
            register_student()  # Member A
        elif choice == "2":
            add_course()  # Member A (Calls Member B internally)
        elif choice == "3":
            drop_course()  # Member A
        elif choice == "4":
            view_registered_courses()  # Member A
        elif choice == "5":
            # Member B Workflow
            timetable_data = generate_timetable(student)
            display_timetable(timetable_data)
        elif choice == "6":
            save_to_file()  # Bonus
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid selection. Please try again.")


if __name__ == "__main__":
    main()
