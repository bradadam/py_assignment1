from tabulate import *  # for prettier tables
import json
import customtkinter as ctk

# ==========================================
#                  BRAD
# ==========================================
# FUNCTIONS:
# 1. display_menu()
# 2. add_course()
# 3. remove_course() (mapped to drop_course)
# 4. check_credit_limit()

#test - just for testing

def display_menu():
    # display main menu – called every loop
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
    # return True if adding course keeps total <= 21
    if current_credits + new_credit > 21:
        print(
            f"Error: Cannot add! Exceeds 21 credits ({current_credits} + {new_credit} = {current_credits + new_credit})"
        )
        return False
    return True


def register_student():
    print("\n--- NEW STUDENT REGISTRATION ---")
    new_student = {}
    new_student["name"] = input("Enter Name: ")
    new_student["matric"] = input("Enter Matric Number: ")
    new_student["registered_courses"] = []
    new_student["total_credits"] = 0
    students.append(new_student)
    print(f"Student {new_student['name']} registered successfully!")

    while find_student(new_student["matric"])["total_credits"] < 12:
        print(
            f"Please add courses to reach minimum 12 credits. Current: {new_student['total_credits']} credits."
        )
        add_course(new_student["matric"])


def find_student(matric):
    for i in students:
        if i["matric"] == matric:
            return i
    else:
        print("Please register student first (Option 1)!")
        return 0


def add_course(matric):
    # add course with full validation

    student = find_student(matric)
    if not student:
        return

    # 1. display list
    print("\nAvailable Courses (Year 1, Sem 1):")
    print(
        tabulate(courses_available, headers="keys", tablefmt="fancy_grid")
    )  # pretty table

    # for c in courses_available:
    #    print(f"{c['code']} - {c['name']} ({c['slots']['day']} {c['slots']['time']})")

    code = input("\nEnter course code to add: ").strip().upper()

    # 2. find course
    course = None
    for c in courses_available:
        if c["code"] == code:
            course = c
            break

    if not course:
        print("Course not found!")
        return

    # 3. validation: check if already registered
    if course in student["registered_courses"]:
        print("You already added this course!")
        return

    # 4. validation: credits
    if not check_credit_limit(student["total_credits"], course["credit"]):
        return

    # 5. validation: clashes
    # INTEGRATION POINT: This will call the function detect_clash() below
    if detect_clash(course, student):
        print(f"TIMETABLE CLASH DETECTED! Cannot add {course['code']}.")
        return

    # 6. finalize add
    student["registered_courses"].append(course)
    student["total_credits"] += course["credit"]
    print(f"Course {course['code']} added successfully!")
    print(f"Total credits: {student['total_credits']}/21")


def drop_course(matric):
    student = find_student(matric)  # find the student
    if not student:
        return

    # remove registered course
    if not student["registered_courses"]:
        print("No courses registered yet!")
        return

    code = input("\nEnter course code to drop: ").strip().upper()

    # range(len(...)) creates a list of indices: [0, 1, 2, etc.]
    for i in range(len(student["registered_courses"])):
        # access the course manually using the index 'i'
        c = student["registered_courses"][i]

        if c["code"] == code:
            if student["total_credits"] - c["credit"] < 12:
                print("Cannot drop! Minimum 12 credits required.")
                return
            removed = student["registered_courses"].pop(i)
            student["total_credits"] -= removed["credit"]
            print(f"Course {code} dropped successfully!")
            print(f"Total credits now: {student['total_credits']}/21")
            break
    else:
        print("Course not found in your registration!")


def view_registered_courses(matric):
    student = find_student(matric)  # find the student
    if not student:
        return

    if not student["registered_courses"]:
        print("\nNo courses registered.")
    else:
        print(f"\nRegistered Courses for {student['name']}:")
        print(
            tabulate(
                student["registered_courses"], headers="keys", tablefmt="fancy_grid"
            )
        )
        # for c in student["registered_courses"]:
        #    print(f"- {c['code']}: {c['name']} ({c['credit']} credits)")
        print(f"Total Credits: {student['total_credits']}")


def detect_clash(new_course, student):
    """
    check if new_course time slot overlap with any registered course
    return True if a clash exists.
    """
    for slot in new_course["slots"]:
        new_day, new_time = slot

        for registered in student["registered_courses"]:
            reg_slots = registered["slots"]
            for reg_slot in reg_slots:
                reg_day, reg_time = reg_slot
                # if day matches AND time matches
                if new_day == reg_day and new_time == reg_time:
                    print(
                        f"CLASH ALERT: New course conflicts with {registered['code']} ({registered['name']})"
                    )
                    return True

    return False


def generate_timetable(matric):
    student = find_student(matric)
    if not student:
        return
    registered_courses = student["registered_courses"]
    courses = {course["code"]: course["slots"] for course in registered_courses}

    timetable = [
        {
            "day": "",
            "08:00": "",
            "09:00": "",
            "10:00": "",
            "11:00": "",
            "12:00": "",
            "13:00": "",
            "14:00": "",
            "15:00": "",
            "16:00": "",
        }
        for _ in range(5)
    ]
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    for i in range(5):
        timetable[i]["day"] = days[i]
        for j in range(8, 17):
            timetable[i][f"{j:02d}:00"] = "  ---  "

    for code, slots in courses.items():
        for slot in slots:
            day, time = slot  # Assuming one slot per course for simplicity
            start_time, end_time = time.split("-")
            start_hour = int(start_time.split(":")[0])
            end_hour = int(end_time.split(":")[0])
            day_index = days.index(day)
            for hour in range(start_hour, end_hour):
                timetable[day_index][f"{hour:02d}:00"] = code
    display_timetable(timetable, student["name"])


def display_timetable(timetable, student_name):
    print(f"\nTimetable for {student_name}:")
    print(tabulate(timetable, headers="keys", tablefmt="fancy_grid"))


def save_and_exit():
    with open("students.json", "w") as sf:
        json.dump(students, sf, indent=4)
    with open("courses.json", "w") as cf:
        json.dump(courses_available, cf, indent=4)


def load_data():
    global students, courses_available
    try:
        with open("students.json", "r") as f:
            students = json.load(f)
    except FileNotFoundError:
        print("No existing student data found. Starting fresh.")
        students = []

    with open("courses.json", "r") as f:
        courses_available = json.load(f)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x300")
        self.title("Student Course Registration")
        label = ctk.CTkLabel(self, text="Welcome to Student Course Registration")
        label.pack(pady=20)

    def register_matric(self):
        entry = ctk.CTkEntry(self, placeholder_text="Enter Matric Number")
        entry.pack(pady=10)
        matric = entry.get()
        button = ctk.CTkButton(
            self, text="Submit", command=lambda: print(f"Matric Number: {entry.get()}")
        )
        button.pack(pady=10)
        return matric

    def run(self):
        self.register_matric()
        self.mainloop()


def main():
    load_data()

    while True:
        display_menu()
        choice = input("Select an option (1-6): ").strip()

        if choice == "1":
            register_student()
        elif choice == "2":
            matric = input("Enter your Matric Number: ").strip().upper()
            add_course(matric)
        elif choice == "3":
            matric = input("Enter your Matric Number: ").strip().upper()
            drop_course(matric)
        elif choice == "4":
            matric = input("Enter your Matric Number: ").strip().upper()
            view_registered_courses(matric)
        elif choice == "5":
            matric = input("Enter your Matric Number: ").strip().upper()
            generate_timetable(matric)
        elif choice == "6":
            save_and_exit()
            break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
