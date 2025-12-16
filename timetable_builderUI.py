import customtkinter as ctk # pip install customtkinter
import json
import os
import time # pip install pillow
import random
from PIL import Image, ImageDraw

# ==========================================
# CONFIGURATION & THEME
# ==========================================
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")
APP_NAME = "UTM AI: Student Scheduler"
MAX_CREDITS = 21

# Color palette for timetable blocks
COURSE_COLORS = [
    "#2980b9",
    "#27ae60",
    "#8e44ad",
    "#c0392b",
    "#d35400",
    "#16a085",
    "#2c3e50",
]


# ==========================================
# DATA HANDLING
# ==========================================
def create_initial_data():
    if not os.path.exists("courses.json"):
        courses = [
            {
                "code": "SAIA1113",
                "name": "PYTHON PROGRAMMING",
                "credit": 3,
                "slots": [["Monday", "08:00-10:00"], ["Tuesday", "08:00-10:00"]],
                "location": "Lab 1",
            },
            {
                "code": "SAIA1143",
                "name": "DISCRETE MATHEMATICS",
                "credit": 3,
                "slots": [["Tuesday", "10:00-12:00"]],
                "location": "LR 15",
            },
            {
                "code": "SAIA1013",
                "name": "RESPONSIBLE AI & ETHICS",
                "credit": 3,
                "slots": [["Wednesday", "14:00-16:00"]],
                "location": "Seminar 3",
            },
            {
                "code": "SAIA1123",
                "name": "INTRODUCTION TO AI",
                "credit": 3,
                "slots": [["Tuesday", "08:00-10:00"]],
                "location": "LR 15",
            },
            {
                "code": "ULRS1032",
                "name": "INTEGRITY & ANTI-CORRUPTION",
                "credit": 2,
                "slots": [["Wednesday", "10:00-12:00"]],
                "location": "LR 15",
            },
            {
                "code": "SAIA1133",
                "name": "DATA MANAGEMENT",
                "credit": 3,
                "slots": [["Thursday", "10:00-12:00"]],
                "location": "LR 15",
            },
            {
                "code": "SAIA1153",
                "name": "MATHEMATICS FOR ML",
                "credit": 3,
                "slots": [["Friday", "08:00-10:00"]],
                "location": "LR 2",
            },
            {
                "code": "UHIS1022",
                "name": "PHILOSOPHY ISSUES",
                "credit": 2,
                "slots": [["Monday", "14:00-16:00"]],
                "location": "Hall A",
            },
        ]
        with open("courses.json", "w") as f:
            json.dump(courses, f, indent=4)

    if not os.path.exists("students.json"):
        with open("students.json", "w") as f:
            json.dump([], f, indent=4)


# ==========================================
# UI CLASS STRUCTURE
# ==========================================
class GROUP2App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(APP_NAME)
        self.geometry("1280x800")
        self.minsize(1000, 700)
        self.resizable(True, True)  # Allow resizing

        self.students = []
        self.courses_available = []
        self.current_student = None
        self.notification_label = None

        # Store reference to the timetable tab so we can refresh it
        self.timetable_tab_frame = None

        create_initial_data()
        self.load_data()

        self.logo_image = self.get_logo_image()

        # Configure Grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.show_login_screen()

    def get_logo_image(self):
        try:
            # Try to load the actual image file
            # Ensure "utm_logo.png" is in the same folder as this script
            img = Image.open("utm_logo.png")

            # Resize it to fit the UI nicely
            return ctk.CTkImage(light_image=img, dark_image=img, size=(150, 50))

        except FileNotFoundError:
            # FALLBACK: If image is missing, draw the placeholder
            print("Warning: 'utm_logo.png' not found. Using placeholder.")
            img = Image.new(
                "RGB", (60, 60), color=(128, 0, 0)
            )  # Dark red to indicate missing file
            d = ImageDraw.Draw(img)
            d.text((10, 20), "LOGO?", fill=(255, 255, 255))
            return ctk.CTkImage(light_image=img, dark_image=img, size=(60, 60))

    def load_data(self):
        try:
            with open("students.json", "r") as f:
                self.students = json.load(f)
        except:
            self.students = []
        try:
            with open("courses.json", "r") as f:
                self.courses_available = json.load(f)
        except:
            self.courses_available = []

    def save_data(self):
        with open("students.json", "w") as f:
            json.dump(self.students, f, indent=4)

    # ==========================================
    # UTILS & NOTIFICATIONS
    # ==========================================
    def show_toast(self, message, is_error=False):
        """Shows a non-intrusive notification at the bottom"""
        color = "#e74c3c" if is_error else "#27ae60"

        if self.notification_label:
            self.notification_label.destroy()

        self.notification_label = ctk.CTkLabel(
            self,
            text=message,
            fg_color=color,
            text_color="white",
            corner_radius=6,
            height=40,
            font=("Roboto", 14, "bold"),
        )
        # Place at bottom center over everything
        self.notification_label.place(
            relx=0.5, rely=0.95, anchor="center", relwidth=0.4
        )

        # Auto hide after 3 seconds
        self.after(
            3000,
            lambda: (
                self.notification_label.destroy() if self.notification_label else None
            ),
        )

    def clear_screen(self):
        for widget in self.winfo_children():
            # Don't destroy the notification if it exists
            if widget != self.notification_label:
                widget.destroy()

    # ==========================================
    # SCREENS
    # ==========================================
    def show_login_screen(self):
        self.clear_screen()
        bg_frame = ctk.CTkFrame(self)
        bg_frame.pack(fill="both", expand=True)

        frame = ctk.CTkFrame(bg_frame, width=400, height=500, corner_radius=15)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(frame, text="", image=self.logo_image).pack(pady=(40, 10))
        ctk.CTkLabel(
            frame, text="COURSE REGISTRATION", font=("Roboto", 20, "bold")
        ).pack(pady=10)

        tabview = ctk.CTkTabview(frame, width=340, height=300)
        tabview.pack(pady=20)
        tabview.add("Login")
        tabview.add("Register")

        # Login
        self.entry_login_matric = ctk.CTkEntry(
            tabview.tab("Login"), placeholder_text="Matric Number"
        )
        self.entry_login_matric.pack(pady=30, padx=30, fill="x")
        ctk.CTkButton(
            tabview.tab("Login"),
            text="Access Dashboard",
            height=40,
            command=self.handle_login,
        ).pack(pady=10, padx=30, fill="x")

        # Register
        self.entry_reg_name = ctk.CTkEntry(
            tabview.tab("Register"), placeholder_text="Full Name"
        )
        self.entry_reg_name.pack(pady=(30, 10), padx=30, fill="x")
        self.entry_reg_matric = ctk.CTkEntry(
            tabview.tab("Register"), placeholder_text="Matric Number"
        )
        self.entry_reg_matric.pack(pady=10, padx=30, fill="x")
        ctk.CTkButton(
            tabview.tab("Register"),
            text="Create Account",
            fg_color="#27ae60",
            hover_color="#2ecc71",
            height=40,
            command=self.handle_register,
        ).pack(pady=15, padx=30, fill="x")

    def show_dashboard(self):
        self.clear_screen()

        # Main Grid Layout: 2 Columns (Sidebar fixed, Content flexible)
        self.grid_columnconfigure(0, weight=0, minsize=250)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # === Sidebar ===
        sidebar = ctk.CTkFrame(self, width=250, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)

        ctk.CTkLabel(sidebar, text="", image=self.logo_image).pack(pady=(40, 10))
        ctk.CTkLabel(
            sidebar,
            text=f"Welcome,\n{self.current_student['name'].split()[0]}",
            font=("Roboto", 20, "bold"),
        ).pack(pady=10)
        ctk.CTkLabel(
            sidebar, text=self.current_student["matric"], text_color="gray"
        ).pack()

        self.credit_label = ctk.CTkLabel(
            sidebar,
            text=f"Credits: {self.current_student['total_credits']}/{MAX_CREDITS}",
            font=("Roboto", 16, "bold"),
            text_color="#3B8ED0",
        )
        self.credit_label.pack(pady=40)

        ctk.CTkButton(
            sidebar,
            text="Log Out",
            fg_color="transparent",
            border_width=2,
            text_color="gray",
            hover_color="#333333",
            command=self.logout,
        ).pack(side="bottom", pady=40, padx=30, fill="x")

        # === Main Content ===
        main_view = ctk.CTkTabview(self)
        main_view.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        main_view.add("Course Selection")
        main_view.add("My Timetable")

        # Save reference to timetable tab for refreshing later
        self.timetable_tab_frame = main_view.tab("My Timetable")

        self.setup_course_tab(main_view.tab("Course Selection"))
        self.setup_timetable_tab(self.timetable_tab_frame)

    # ==========================================
    # LOGIC HANDLERS
    # ==========================================
    def handle_login(self):
        matric = self.entry_login_matric.get().strip().upper()
        for student in self.students:
            if student["matric"] == matric:
                self.current_student = student
                self.show_dashboard()
                self.show_toast(f"Welcome back, {student['name']}!")
                return
        self.show_toast("Student not found. Please register.", is_error=True)

    def handle_register(self):
        name = self.entry_reg_name.get().strip().title()
        matric = self.entry_reg_matric.get().strip().upper()
        if not name or not matric:
            self.show_toast("Please fill in all fields.", is_error=True)
            return
        if any(s["matric"] == matric for s in self.students):
            self.show_toast("Matric number already registered.", is_error=True)
            return

        new_student = {
            "name": name,
            "matric": matric,
            "registered_courses": [],
            "total_credits": 0,
        }
        self.students.append(new_student)
        self.save_data()
        self.show_toast("Registration successful! Please Login.")
        self.entry_reg_name.delete(0, "end")
        self.entry_reg_matric.delete(0, "end")

    def logout(self):
        self.current_student = None
        self.save_data()
        self.show_login_screen()

    def check_clash(self, new_course):
        for slot in new_course["slots"]:
            new_day, new_time = slot
            n_start = int(new_time.split("-")[0].split(":")[0])
            n_end = int(new_time.split("-")[1].split(":")[0])

            for registered in self.current_student["registered_courses"]:
                for reg_slot in registered["slots"]:
                    reg_day, reg_time = reg_slot
                    if new_day != reg_day:
                        continue
                    r_start = int(reg_time.split("-")[0].split(":")[0])
                    r_end = int(reg_time.split("-")[1].split(":")[0])

                    # Overlap logic
                    if max(n_start, r_start) < min(n_end, r_end):
                        return f"Clash with {registered['code']} ({new_day} {new_time})"
        return None

    def add_course_action(self, course):
        if any(
            c["code"] == course["code"]
            for c in self.current_student["registered_courses"]
        ):
            self.show_toast("Already registered for this course.", is_error=True)
            return
        if self.current_student["total_credits"] + course["credit"] > MAX_CREDITS:
            self.show_toast(f"Cannot exceed {MAX_CREDITS} credits.", is_error=True)
            return
        clash = self.check_clash(course)
        if clash:
            self.show_toast(clash, is_error=True)
            return

        self.current_student["registered_courses"].append(course)
        self.current_student["total_credits"] += course["credit"]
        self.save_data()
        self.refresh_ui()
        self.show_toast(f"Added {course['code']} successfully.")

    def drop_course_action(self, course):
        self.current_student["registered_courses"] = [
            c
            for c in self.current_student["registered_courses"]
            if c["code"] != course["code"]
        ]
        self.current_student["total_credits"] -= course["credit"]
        self.save_data()
        self.refresh_ui()
        self.show_toast(f"Dropped {course['code']}.", is_error=True)

    def refresh_ui(self):
        """Updates the UI elements when data changes"""
        if self.current_student:
            # 1. Update Credits Label
            self.credit_label.configure(
                text=f"Credits: {self.current_student['total_credits']}/{MAX_CREDITS}"
            )
            # 2. Refresh Course Lists
            self.populate_course_lists()

            # 3. FIX: Refresh Timetable immediately!
            # Clear existing widgets in the timetable tab
            for widget in self.timetable_tab_frame.winfo_children():
                widget.destroy()
            # Re-run setup to draw updated blocks
            self.setup_timetable_tab(self.timetable_tab_frame)

    # ==========================================
    # COURSE SELECTION TAB
    # ==========================================
    def setup_course_tab(self, parent):
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_columnconfigure(1, weight=1)
        parent.grid_rowconfigure(1, weight=1)  # Row 1 has the lists

        # --- Left Side: Available ---
        frame_avail = ctk.CTkFrame(parent, fg_color="transparent")
        frame_avail.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=(0, 10))

        # Search Bar
        self.search_var = ctk.StringVar()
        self.search_var.trace("w", self.filter_courses)
        search_entry = ctk.CTkEntry(
            frame_avail,
            placeholder_text="Search Course Code/Name...",
            textvariable=self.search_var,
            height=35,
        )
        search_entry.pack(fill="x", pady=(0, 10))

        self.scroll_avail = ctk.CTkScrollableFrame(frame_avail)
        self.scroll_avail.pack(fill="both", expand=True)

        # --- Right Side: Registered ---
        frame_reg = ctk.CTkFrame(parent, fg_color="transparent")
        frame_reg.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=(10, 0))

        ctk.CTkLabel(
            frame_reg, text="My Registered Courses", font=("Roboto", 18, "bold")
        ).pack(pady=(0, 10), anchor="w")
        self.scroll_reg = ctk.CTkScrollableFrame(frame_reg)
        self.scroll_reg.pack(fill="both", expand=True)

        self.populate_course_lists()

    def filter_courses(self, *args):
        self.populate_course_lists(filter_text=self.search_var.get())

    def populate_course_lists(self, filter_text=""):
        # Clear existing
        for w in self.scroll_avail.winfo_children():
            w.destroy()
        for w in self.scroll_reg.winfo_children():
            w.destroy()

        registered_codes = {
            c["code"] for c in self.current_student["registered_courses"]
        }

        # Available List (Filtered)
        for course in self.courses_available:
            if course["code"] not in registered_codes:
                if (
                    filter_text.lower() in course["code"].lower()
                    or filter_text.lower() in course["name"].lower()
                ):
                    self.create_course_card(
                        self.scroll_avail, course, is_registered=False
                    )

        # Registered List
        for course in self.current_student["registered_courses"]:
            self.create_course_card(self.scroll_reg, course, is_registered=True)

    def create_course_card(self, parent, course, is_registered):
        card = ctk.CTkFrame(
            parent,
            corner_radius=8,
            fg_color="#2b2b2b",
            border_color="#333",
            border_width=1,
        )
        card.pack(fill="x", pady=5, padx=5)  # Fill X is crucial for sizing

        # Left Info
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(side="left", padx=10, pady=10, fill="both", expand=True)

        ctk.CTkLabel(info_frame, text=course["code"], font=("Roboto", 14, "bold")).pack(
            anchor="w"
        )
        ctk.CTkLabel(info_frame, text=course["name"], font=("Roboto", 12)).pack(
            anchor="w"
        )

        slot_str = ", ".join([f"{d[:3]} {t}" for d, t in course["slots"]])
        ctk.CTkLabel(
            info_frame,
            text=f"Cr: {course['credit']} | {slot_str}",
            font=("Roboto", 11),
            text_color="#aaa",
        ).pack(anchor="w")

        # Action Button
        btn_text = "Drop" if is_registered else "Add"
        btn_color = "#c0392b" if is_registered else "#2980b9"
        cmd = lambda c=course: (
            self.drop_course_action(c) if is_registered else self.add_course_action(c)
        )

        ctk.CTkButton(
            card, text=btn_text, width=70, height=30, fg_color=btn_color, command=cmd
        ).pack(side="right", padx=10)

    # ==========================================
    # TIMETABLE TAB
    # ==========================================
    def setup_timetable_tab(self, parent):
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        hours = range(8, 18)  # 8am to 5pm

        container = ctk.CTkScrollableFrame(parent)
        container.pack(fill="both", expand=True, padx=0, pady=0)

        # Configure container grid
        container.grid_columnconfigure(0, weight=0, minsize=80)  # Day label column
        for i in range(len(hours)):
            container.grid_columnconfigure(
                i + 1, weight=1, minsize=100
            )  # Hour columns stretch

        # Headers (Time)
        for col, h in enumerate(hours):
            ctk.CTkLabel(
                container,
                text=f"{h:02d}:00",
                font=("Roboto", 12, "bold"),
                text_color="gray",
            ).grid(row=0, column=col + 1, pady=10)

        # Draw Grid & Days
        for r, day in enumerate(days, start=1):
            # Day Label
            ctk.CTkLabel(container, text=day, font=("Roboto", 13, "bold")).grid(
                row=r, column=0, pady=20, padx=10
            )

            # Empty cells (Background grid)
            for c in range(len(hours)):
                frame = ctk.CTkFrame(
                    container,
                    height=60,
                    fg_color="#1a1a1a",
                    border_color="#2b2b2b",
                    border_width=1,
                    corner_radius=0,
                )
                frame.grid(row=r, column=c + 1, sticky="nsew", padx=1, pady=1)

        # Place Course Blocks
        for i, course in enumerate(self.current_student["registered_courses"]):
            color = COURSE_COLORS[i % len(COURSE_COLORS)]

            for slot in course["slots"]:
                day, time_range = slot
                if day not in days:
                    continue

                day_idx = days.index(day) + 1
                start_h = int(time_range.split("-")[0].split(":")[0])
                end_h = int(time_range.split("-")[1].split(":")[0])
                duration = end_h - start_h

                if start_h >= 8 and end_h <= 18:
                    col_idx = (start_h - 8) + 1

                    # Course Block
                    block = ctk.CTkFrame(container, fg_color=color, corner_radius=6)
                    block.grid(
                        row=day_idx,
                        column=col_idx,
                        columnspan=duration,
                        sticky="nsew",
                        padx=2,
                        pady=2,
                    )

                    # Content inside block
                    content = ctk.CTkLabel(
                        block,
                        text=f"{course['code']}\n{course['location']}",
                        font=("Roboto", 11, "bold"),
                        text_color="white",
                    )
                    content.place(relx=0.5, rely=0.5, anchor="center")


if __name__ == "__main__":
    app = GROUP2App()
    app.mainloop()
