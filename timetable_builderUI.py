import customtkinter as ctk
import json
import os
from PIL import Image, ImageDraw

# ==========================================
# CONFIGURATION & THEME
# ==========================================
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")
APP_NAME = "UTM AI: Student Scheduler"
MAX_CREDITS = 21

# Color palette for different courses in timetable
COURSE_COLORS = [
    "#2980b9",  # Blue
    "#27ae60",  # Green
    "#8e44ad",  # Purple
    "#c0392b",  # Red
    "#d35400",  # Orange
    "#16a085",  # Teal
    "#2c3e50",  # Dark Blue
    "#f39c12",  # Yellow-Orange
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
# MAIN APP CLASS
# ==========================================
class GROUP2App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(APP_NAME)
        self.geometry("1280x800")
        self.minsize(1000, 700)

        self.students = []
        self.courses_available = []
        self.current_student = None
        self.notification_label = None
        self.timetable_container = None  # To refresh timetable

        create_initial_data()
        self.load_data()
        self.logo_image = self.get_logo_image()

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.show_login_screen()

    def get_logo_image(self):
        try:
            img = Image.open("utm_logo.png")
            return ctk.CTkImage(light_image=img, dark_image=img, size=(180, 60))
        except Exception:
            print("Warning: 'utm_logo.png' not found. Using placeholder.")
            img = Image.new("RGB", (180, 60), color=(128, 0, 0))
            d = ImageDraw.Draw(img)
            d.text((40, 15), "UTM AI", fill="white", font_size=30)
            return ctk.CTkImage(light_image=img, dark_image=img, size=(180, 60))

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
    # NOTIFICATIONS
    # ==========================================
    def show_toast(self, message, is_error=False):
        if self.notification_label:
            self.notification_label.destroy()
        color = "#e74c3c" if is_error else "#27ae60"
        self.notification_label = ctk.CTkLabel(
            self,
            text=message,
            fg_color=color,
            text_color="white",
            corner_radius=8,
            height=40,
            font=("Roboto", 14, "bold"),
            padx=20,
        )
        self.notification_label.place(relx=0.5, rely=0.95, anchor="center")
        self.after(
            3000,
            lambda: (
                self.notification_label.destroy() if self.notification_label else None
            ),
        )

    def clear_screen(self):
        for widget in self.winfo_children():
            if widget != self.notification_label:
                widget.destroy()

    # ==========================================
    # SCREENS
    # ==========================================
    def show_login_screen(self):
        self.clear_screen()
        frame = ctk.CTkFrame(self, corner_radius=15)
        frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.35, relheight=0.65)

        ctk.CTkLabel(frame, text="", image=self.logo_image).pack(pady=(40, 20))
        ctk.CTkLabel(
            frame, text="COURSE REGISTRATION", font=("Roboto", 24, "bold")
        ).pack(pady=(0, 20))

        tabview = ctk.CTkTabview(frame, width=380, height=300)
        tabview.pack(pady=10)

        tabview.add("Login")
        tabview.add("Register")

        # Login
        self.entry_login_matric = ctk.CTkEntry(
            tabview.tab("Login"), placeholder_text="Matric Number", font=("Roboto", 14)
        )
        self.entry_login_matric.pack(pady=30, padx=40, fill="x")
        ctk.CTkButton(
            tabview.tab("Login"),
            text="Access Dashboard",
            height=40,
            command=self.handle_login,
        ).pack(pady=10, padx=40, fill="x")

        # Register
        self.entry_reg_name = ctk.CTkEntry(
            tabview.tab("Register"), placeholder_text="Full Name", font=("Roboto", 14)
        )
        self.entry_reg_name.pack(pady=(30, 10), padx=40, fill="x")
        self.entry_reg_matric = ctk.CTkEntry(
            tabview.tab("Register"),
            placeholder_text="Matric Number",
            font=("Roboto", 14),
        )
        self.entry_reg_matric.pack(pady=10, padx=40, fill="x")
        ctk.CTkButton(
            tabview.tab("Register"),
            text="Create Account",
            fg_color="#27ae60",
            hover_color="#2ecc71",
            height=40,
            command=self.handle_register,
        ).pack(pady=15, padx=40, fill="x")

    def show_dashboard(self):
        self.clear_screen()

        # Sidebar
        sidebar = ctk.CTkFrame(self, width=260, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)

        ctk.CTkLabel(sidebar, text="", image=self.logo_image).pack(pady=(40, 20))
        ctk.CTkLabel(
            sidebar,
            text=f"Welcome,\n{self.current_student['name'].split()[0]}",
            font=("Roboto", 22, "bold"),
        ).pack(pady=10)
        ctk.CTkLabel(
            sidebar,
            text=self.current_student["matric"],
            text_color="#aaaaaa",
            font=("Roboto", 14),
        ).pack()

        self.credit_label = ctk.CTkLabel(
            sidebar,
            text=f"Credits: {self.current_student['total_credits']}/{MAX_CREDITS}",
            font=("Roboto", 18, "bold"),
            text_color="#3498db",
        )
        self.credit_label.pack(pady=50)

        ctk.CTkButton(
            sidebar,
            text="Log Out",
            fg_color="transparent",
            border_width=2,
            text_color="#95a5a6",
            hover_color="#2c3e50",
            command=self.logout,
            height=40,
        ).pack(side="bottom", pady=40, padx=40, fill="x")

        # Main Content
        main_view = ctk.CTkTabview(self)
        main_view.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        main_view.add("Course Selection")
        main_view.add("My Timetable")

        self.setup_course_tab(main_view.tab("Course Selection"))
        self.setup_timetable_tab(main_view.tab("My Timetable"))

    # ==========================================
    # LOGIC
    # ==========================================
    def handle_login(self):
        matric = self.entry_login_matric.get().strip().upper()
        for student in self.students:
            if student["matric"] == matric:
                self.current_student = student
                self.show_dashboard()
                self.show_toast(f"Welcome back, {student['name'].split()[0]}!")
                return
        self.show_toast("Student not found. Please register.", is_error=True)

    def handle_register(self):
        name = self.entry_reg_name.get().strip().title()
        matric = self.entry_reg_matric.get().strip().upper()
        if not name or not matric:
            self.show_toast("Please fill all fields.", is_error=True)
            return
        if any(s["matric"] == matric for s in self.students):
            self.show_toast("Matric number already exists.", is_error=True)
            return

        new_student = {
            "name": name,
            "matric": matric,
            "registered_courses": [],
            "total_credits": 0,
        }
        self.students.append(new_student)
        self.save_data()
        self.show_toast("Registration successful! You can now login.")
        self.entry_reg_name.delete(0, "end")
        self.entry_reg_matric.delete(0, "end")

    def logout(self):
        self.current_student = None
        self.save_data()
        self.show_login_screen()

    def check_clash(self, new_course):
        for n_slot in new_course["slots"]:
            n_day, n_time = n_slot
            n_start = int(n_time.split("-")[0].split(":")[0])
            n_end = int(n_time.split("-")[1].split(":")[0])

            for reg_course in self.current_student["registered_courses"]:
                for r_slot in reg_course["slots"]:
                    r_day, r_time = r_slot
                    if n_day != r_day:
                        continue
                    r_start = int(r_time.split("-")[0].split(":")[0])
                    r_end = int(r_time.split("-")[1].split(":")[0])
                    if max(n_start, r_start) < min(n_end, r_end):
                        return f"Clash with {reg_course['code']} on {n_day} {n_time}"
        return None

    def add_course_action(self, course):
        if any(
            c["code"] == course["code"]
            for c in self.current_student["registered_courses"]
        ):
            self.show_toast("Already registered for this course.", is_error=True)
            return
        if self.current_student["total_credits"] + course["credit"] > MAX_CREDITS:
            self.show_toast(f"Exceeds {MAX_CREDITS} credit limit.", is_error=True)
            return
        clash = self.check_clash(course)
        if clash:
            self.show_toast(clash, is_error=True)
            return

        self.current_student["registered_courses"].append(course)
        self.current_student["total_credits"] += course["credit"]
        self.save_data()
        self.refresh_ui()
        self.show_toast(f"Added {course['code']} successfully!")

    def drop_course_action(self, course):
        self.current_student["registered_courses"] = [
            c
            for c in self.current_student["registered_courses"]
            if c["code"] != course["code"]
        ]
        self.current_student["total_credits"] -= course["credit"]
        self.save_data()
        self.refresh_ui()
        self.show_toast(f"Dropped {course['code']}.")

    def refresh_ui(self):
        if not self.current_student:
            return
        self.credit_label.configure(
            text=f"Credits: {self.current_student['total_credits']}/{MAX_CREDITS}"
        )
        self.populate_course_lists()
        # Refresh timetable
        if self.timetable_container:
            for widget in self.timetable_container.winfo_children():
                widget.destroy()
            self.draw_timetable_grid(self.timetable_container)

    # ==========================================
    # COURSE SELECTION TAB
    # ==========================================
    def setup_course_tab(self, parent):
        parent.grid_columnconfigure((0, 1), weight=1)
        parent.grid_rowconfigure(0, weight=1)

        # Left: Available
        left = ctk.CTkFrame(parent)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        ctk.CTkLabel(left, text="Available Courses", font=("Roboto", 18, "bold")).pack(
            pady=(10, 5), anchor="w", padx=20
        )

        self.search_var = ctk.StringVar()
        self.search_var.trace("w", lambda *args: self.populate_course_lists())
        ctk.CTkEntry(
            left,
            placeholder_text="Search by code or name...",
            textvariable=self.search_var,
            height=35,
        ).pack(fill="x", padx=20, pady=(0, 10))

        self.scroll_avail = ctk.CTkScrollableFrame(left)
        self.scroll_avail.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Right: Registered
        right = ctk.CTkFrame(parent)
        right.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        ctk.CTkLabel(
            right, text="My Registered Courses", font=("Roboto", 18, "bold")
        ).pack(pady=(10, 5), anchor="w", padx=20)
        self.scroll_reg = ctk.CTkScrollableFrame(right)
        self.scroll_reg.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.populate_course_lists()

    def populate_course_lists(self):
        search = self.search_var.get().lower()
        for w in self.scroll_avail.winfo_children() + self.scroll_reg.winfo_children():
            w.destroy()

        registered_codes = {
            c["code"] for c in self.current_student["registered_courses"]
        }

        for course in self.courses_available:
            if course["code"] in registered_codes:
                continue
            if (
                search
                and search not in course["code"].lower()
                and search not in course["name"].lower()
            ):
                continue
            self.create_course_card(self.scroll_avail, course, False)

        for course in self.current_student["registered_courses"]:
            self.create_course_card(self.scroll_reg, course, True)

    def create_course_card(self, parent, course, is_registered):
        card = ctk.CTkFrame(parent, corner_radius=10, fg_color="#2f2f2f")
        card.pack(fill="x", pady=6, padx=10)

        info = ctk.CTkFrame(card, fg_color="transparent")
        info.pack(side="left", padx=15, pady=12, fill="both", expand=True)

        ctk.CTkLabel(
            info, text=course["code"], font=("Roboto", 15, "bold"), anchor="w"
        ).pack(anchor="w")
        ctk.CTkLabel(info, text=course["name"], font=("Roboto", 13), anchor="w").pack(
            anchor="w"
        )
        slots = ", ".join(f"{d[:3]} {t}" for d, t in course["slots"])
        ctk.CTkLabel(
            info,
            text=f"{course['credit']} credits • {slots}",
            text_color="#bbbbbb",
            anchor="w",
        ).pack(anchor="w", pady=(5, 0))

        btn_text = "Drop" if is_registered else "Add"
        btn_color = "#c0392b" if is_registered else "#2980b9"
        ctk.CTkButton(
            card,
            text=btn_text,
            width=80,
            fg_color=btn_color,
            hover_color=("#a93226" if is_registered else "#2471a3"),
            command=lambda c=course: (
                self.drop_course_action(c)
                if is_registered
                else self.add_course_action(c)
            ),
        ).pack(side="right", padx=15, pady=15)

    # ==========================================
    # TIMETABLE TAB
    # ==========================================
    def setup_timetable_tab(self, parent):
        self.timetable_container = ctk.CTkScrollableFrame(parent)
        self.timetable_container.pack(fill="both", expand=True, padx=20, pady=20)
        self.draw_timetable_grid(self.timetable_container)

    def draw_timetable_grid(self, container):
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        hours = list(range(8, 18))  # 08:00 to 17:00

        # Configure grid
        container.grid_columnconfigure(0, minsize=100)
        for i in range(len(hours)):
            container.grid_columnconfigure(i + 1, weight=1, minsize=120)

        # Time headers
        for col, h in enumerate(hours):
            ctk.CTkLabel(
                container, text=f"{h:02d}:00", font=("Roboto", 12, "bold")
            ).grid(row=0, column=col + 1, pady=10)

        # Day labels + empty cells
        for r, day in enumerate(days, start=1):
            ctk.CTkLabel(
                container, text=day, font=("Roboto", 14, "bold"), width=12
            ).grid(row=r, column=0, padx=10, pady=25)
            for c in range(len(hours)):
                cell = ctk.CTkFrame(
                    container, fg_color="#1e1e1e", corner_radius=6, height=70
                )
                cell.grid(row=r, column=c + 1, padx=2, pady=2, sticky="nsew")
                cell.grid_propagate(False)

        # Place course blocks with unique colors
        for idx, course in enumerate(self.current_student["registered_courses"]):
            color = COURSE_COLORS[idx % len(COURSE_COLORS)]
            for slot in course["slots"]:
                day_name, time_range = slot
                if day_name not in days:
                    continue
                day_row = days.index(day_name) + 1
                start_str, end_str = time_range.split("-")
                start_h = int(start_str.split(":")[0])
                end_h = int(end_str.split(":")[0])
                duration = end_h - start_h
                col_start = (start_h - 8) + 1

                if start_h < 8 or end_h > 18:
                    continue

                block = ctk.CTkFrame(container, fg_color=color, corner_radius=10)
                block.grid(
                    row=day_row,
                    column=col_start,
                    columnspan=duration,
                    sticky="nsew",
                    padx=3,
                    pady=6,
                )

                text = f"{course['code']}\n{course['name'][:20]}{'...' if len(course['name']) > 20 else ''}\n{course['location']}"
                ctk.CTkLabel(
                    block,
                    text=text,
                    font=("Roboto", 11, "bold"),
                    text_color="white",
                    justify="center",
                    wraplength=110,
                ).place(relx=0.5, rely=0.5, anchor="center")


if __name__ == "__main__":
    app = GROUP2App()
    app.mainloop()
