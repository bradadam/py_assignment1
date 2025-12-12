import os
import customtkinter as ctk  # pip install customtkinter
import json
from tkinter import messagebox
from datetime import datetime
from PIL import Image  # pip install pillow

# --- SETTINGS ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# --- DATA ---
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
        "slots": {
            "day": "Friday",
            "time": "09:00-12:00",
        },  # Moved to Friday to match PDF & avoid clash
        "location": "Seminar Room 3, BATC",
    },
    {
        "code": "SAIA1023",
        "name": "AI AND ITS APPLICATION",
        "credit": 3,
        "slots": {
            "day": "Tuesday",
            "time": "14:00-17:00",
        },  # Updated from PDF (2pm - 5pm)
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


class CourseRegistrationApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("UTM Course Registration System • Faculty of AI")
        self.geometry("1200x800")
        self.minsize(1000, 700)

        # Main Layout Config
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)  # The table row expands

        # ===================== 1. HEADER =====================
        self.create_header()

        # ===================== 2. STUDENT INFO CARD =====================
        self.create_student_card()

        # ===================== 3. ACTION CARD =====================
        self.create_action_card()

        # ===================== 4. MODERN TIMETABLE =====================
        self.create_timetable_area()

        # ===================== 5. FOOTER =====================
        footer = ctk.CTkLabel(
            self,
            text=f"© {datetime.now().year} Universiti Teknologi Malaysia",
            text_color="gray50",
        )
        footer.grid(row=4, column=0, pady=10)

    def create_header(self):
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=30, pady=(20, 10), sticky="ew")

        # Title Stack
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.pack(side="right")

        ctk.CTkLabel(
            title_frame, text="Course Registration", font=("Segoe UI", 28)
        ).pack(anchor="w")
        ctk.CTkLabel(
            title_frame,
            text="Semester 1 2025/2026 • Faculty of Artificial Intelligence",
            font=("Segoe UI", 14),
            text_color="gray70",
        ).pack(anchor="w")

        # --- FIX 2: Updated Image Loading Logic ---
        logo_path = "py_assignment1/utm_logo.png"
        if os.path.exists(logo_path):
            try:
                # Open image using standard PIL
                img_data = Image.open(logo_path)

                # Use CTkImage instead of ImageTk.PhotoImage
                # size=(width, height) is required here for scaling
                self.utm_logo = ctk.CTkImage(
                    light_image=img_data, dark_image=img_data, size=(200, 60)
                )

                # Apply to label
                ctk.CTkLabel(header_frame, text="", image=self.utm_logo).pack(
                    side="left", padx=10
                )
            except Exception as e:
                print(f"Logo error: {e}")
                pass

    def create_student_card(self):
        self.card_info = ctk.CTkFrame(
            self, fg_color=("#2b2b2b", "#2b2b2b"), corner_radius=10
        )
        self.card_info.grid(row=1, column=0, padx=30, pady=10, sticky="ew")
        self.card_info.grid_columnconfigure((1, 3), weight=1)

        ctk.CTkLabel(self.card_info, text="Student Name:").grid(
            row=0, column=0, padx=(20, 10), pady=15
        )
        self.entry_name = ctk.CTkEntry(self.card_info, placeholder_text="Full Name")
        self.entry_name.grid(row=0, column=1, sticky="ew", padx=10)

        ctk.CTkLabel(self.card_info, text="Matric No:").grid(
            row=0, column=2, padx=10
        )
        self.entry_matric = ctk.CTkEntry(self.card_info, placeholder_text="A25AI...")
        self.entry_matric.grid(row=0, column=3, sticky="ew", padx=10)

        self.btn_register = ctk.CTkButton(
            self.card_info,
            text="Register Student",
            fg_color="#0056b3",
            command=self.register_student,
        )
        self.btn_register.grid(row=0, column=4, padx=20)

        self.lbl_credits = ctk.CTkLabel(
            self.card_info,
            text="0/21 Credits",
            font=("Arial", 20, "bold"),
            text_color="gray",
        )
        self.lbl_credits.grid(row=0, column=5, padx=(10, 30))

    def create_action_card(self):
        self.card_action = ctk.CTkFrame(
            self, fg_color=("#2b2b2b", "#2b2b2b"), corner_radius=10
        )
        self.card_action.grid(row=2, column=0, padx=30, pady=10, sticky="ew")

        ctk.CTkLabel(self.card_action, text="Select Course:").pack(
            side="left", padx=20, pady=15
        )

        course_list = [f"{c['code']} - {c['name']}" for c in courses_available]
        self.combo_course = ctk.CTkComboBox(
            self.card_action, values=course_list, width=400
        )
        self.combo_course.set("Select a course...")
        self.combo_course.pack(side="left", padx=10)

        self.btn_add = ctk.CTkButton(
            self.card_action,
            text="➕ Add Course",
            fg_color="#198754",
            hover_color="#146c43",
            width=120,
            command=self.add_course,
        )
        self.btn_add.pack(side="left", padx=10)

        self.btn_save = ctk.CTkButton(
            self.card_action,
            text="Save Data",
            fg_color="#6c757d",
            hover_color="#5c636a",
            width=100,
            command=self.save_data,
        )
        self.btn_save.pack(side="right", padx=20)

    def create_timetable_area(self):
        list_container = ctk.CTkFrame(self, fg_color="transparent")
        list_container.grid(row=3, column=0, padx=30, pady=10, sticky="nsew")
        list_container.grid_rowconfigure(1, weight=1)
        list_container.grid_columnconfigure(0, weight=1)

        header = ctk.CTkFrame(
            list_container, height=40, fg_color=("#3a3a3a", "#1f1f1f"), corner_radius=5
        )
        header.grid(row=0, column=0, sticky="ew", pady=(0, 5))
        header.grid_columnconfigure(4, weight=1)

        cols = [
            ("Day", 100),
            ("Time", 120),
            ("Code", 100),
            ("Location", 200),
            ("Course Name", 300),
            ("Credits", 80),
            ("Action", 80),
        ]

        for i in range(len(cols)):
            # 1. Get the data from the list using the index 'i'
            # 2. Unpack the tuple into txt and w
            txt, w = cols[i]

            # We move 'width=w' INSIDE the Label constructor
            lbl = ctk.CTkLabel(header, text=txt, font=("Arial", 12, "bold"), width=w)

            if i == 4:  # Name column special case
                lbl.configure(anchor="w")  # Align text left
                lbl.grid(row=0, column=i, sticky="w", padx=10, pady=5)
            else:
                # We removed 'width=w' from .grid()
                lbl.grid(row=0, column=i, pady=5)

        self.scroll_frame = ctk.CTkScrollableFrame(
            list_container, fg_color="transparent"
        )
        self.scroll_frame.grid(row=1, column=0, sticky="nsew")
        self.scroll_frame.grid_columnconfigure(0, weight=1)

        self.row_widgets = []

    def refresh_table(self):
        for widget in self.row_widgets:
            widget.destroy()
        self.row_widgets.clear()

        days_order = {
            "Monday": 1,
            "Tuesday": 2,
            "Wednesday": 3,
            "Thursday": 4,
            "Friday": 5,
        }
        sorted_courses = sorted(
            student["registered_courses"],
            key=lambda x: days_order.get(x["slots"]["day"], 99),
        )

        for course in sorted_courses:
            row = ctk.CTkFrame(
                self.scroll_frame, fg_color=("#333333", "#242424"), corner_radius=5
            )
            row.pack(fill="x", pady=2)
            row.grid_columnconfigure(4, weight=1)
            self.row_widgets.append(row)

            # Note: We also apply fixed widths here to align with the header
            ctk.CTkLabel(row, text=course["slots"]["day"], width=100).grid(
                row=0, column=0, pady=10
            )
            ctk.CTkLabel(
                row, text=course["slots"]["time"], text_color="#4cc9f0", width=120
            ).grid(row=0, column=1)
            ctk.CTkLabel(
                row, text=course["code"], font=("Segoe UI", 12, "bold"), width=100
            ).grid(row=0, column=2)
            ctk.CTkLabel(row, text=course["location"], width=200).grid(row=0, column=3)
            ctk.CTkLabel(row, text=course["name"], anchor="w").grid(
                row=0, column=4, sticky="ew", padx=10
            )
            ctk.CTkLabel(row, text=str(course["credit"]), width=80).grid(
                row=0, column=5
            )

            btn_del = ctk.CTkButton(
                row,
                text="×",
                width=30,
                height=30,
                fg_color="#dc3545",
                hover_color="#a71d2a",
                command=lambda c=course: self.delete_specific_course(c),
            )
            btn_del.grid(
                row=0, column=6, padx=25
            )  # Padding to center in the 80px column

    # ===================== LOGIC FUNCTIONS =====================

    def register_student(self):
        name = self.entry_name.get().strip()
        matric = self.entry_matric.get().strip().upper()

        if not name or not matric:
            messagebox.showerror(
                "Missing Info", "Please enter both Name and Matric Number."
            )
            return

        if len(name) < 3:
            messagebox.showerror(
                "Invalid Name", "Name too short! and please fill in your full name!"
            )
            self.entry_name.focus_set()  # puts cursor back to in matric id box
            return

        if any(char.isdigit() for char in name):
            messagebox.showerror(
                "Invalid Name", "Name cannot contain numbers. Please enter a valid name."
            )
            self.entry_name.focus_set()  # puts cursor back to in matric id box
            return

        if not matric.startswith("A25"):
            messagebox.showerror(
                "Invalid Matric Number", "Matric Number should start with 'A25'."
            )
            self.entry_matric.focus_set()  # puts cursor back to in matric id box
            return

        student.update(
            {
                "name": name,
                "matric": matric,
                "registered_courses": [],
                "total_credits": 0,
            }
        )
        self.update_ui_state()
        messagebox.showinfo("Success", f"Student {name} registered!")

    def add_course(self):
        if not student["name"]:
            messagebox.showwarning(
                "Action Blocked", "Please register the student first."
            )
            return

        selection = self.combo_course.get()
        if not selection or "Select" in selection:
            return

        code = selection.split(" - ")[0]
        course = next((c for c in courses_available if c["code"] == code), None)

        if course in student["registered_courses"]:
            messagebox.showinfo("Info", "Course already registered.")
            return

        if student["total_credits"] + course["credit"] > 21:
            messagebox.showerror("Limit Reached", "Cannot exceed 21 credits.")
            return

        for registered in student["registered_courses"]:
            if (
                registered["slots"]["day"] == course["slots"]["day"]
                and registered["slots"]["time"] == course["slots"]["time"]
            ):
                messagebox.showerror("Time Clash", f"Clash with {registered['code']}!")
                return

        student["registered_courses"].append(course)
        student["total_credits"] += course["credit"]
        self.update_ui_state()
        self.refresh_table()

    def delete_specific_course(self, course_to_remove):
        if course_to_remove in student["registered_courses"]:
            student["registered_courses"].remove(course_to_remove)
            student["total_credits"] -= course_to_remove["credit"]
            self.update_ui_state()
            self.refresh_table()

    def update_ui_state(self):
        creds = student["total_credits"]
        color = "#2ecc71" if creds > 0 else "gray"
        self.lbl_credits.configure(text=f"{creds}/21 Credits", text_color=color)

    def save_data(self):
        # 1. Check if there is actually a student to save
        if not student["matric"]:
            messagebox.showwarning("Warning", "No student data to save!")
            return

        filename = "student_database.json"
        all_students = {}

        # 2. Try to load existing data so we don't delete previous students
        if os.path.exists(filename):
            try:
                with open(filename, "r") as f:
                    all_students = json.load(f)
            except json.JSONDecodeError:
                all_students = {}  # Start fresh if file is corrupt/empty

        # 3. Add or Update the current student
        # We use the Matric Number as the unique Key
        all_students[student["matric"]] = student

        # 4. Save everything back to the file
        with open(filename, "w") as f:
            json.dump(all_students, f, indent=4)

        messagebox.showinfo(
            "Saved",
            f"Data for {student['name']} ({student['matric']}) has been saved. Stored in {filename}.",
        )


if __name__ == "__main__":
    app = CourseRegistrationApp()
    app.mainloop()
