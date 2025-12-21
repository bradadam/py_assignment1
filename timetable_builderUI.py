import customtkinter as ctk
import json
import os
import re
from PIL import Image, ImageDraw

# ==========================================
# CONFIGURATION & THEME - Light and Friendly!
# ==========================================
ctk.set_appearance_mode("Light")  # Bright, clean background
ctk.set_default_color_theme("green")  # Soft, friendly green accents

APP_NAME = "UTM AI: Student Scheduler"
MAX_CREDITS = 21
MIN_CREDITS = 12

# Soft pastel colors for course blocks – perfect for light mode
COURSE_COLORS = [
    "#A7C7E7",  # Soft Sky Blue
    "#B5EAD7",  # Mint Green
    "#E0BBE4",  # Lavender Purple
    "#FFC3A0",  # Peach Orange
    "#C7CEEA",  # Periwinkle
    "#FFDAC1",  # Light Coral
    "#E2F0CB",  # Pale Lime
    "#D4A5A5",  # Dusty Rose
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
        self.students = []
        self.courses_available = []
        self.current_student = None
        self.notification_label = None
        self.timetable_container = None
        self.min_credit_warning = None
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
            img = Image.new(
                "RGB", (180, 60), color=(200, 240, 220)
            )  # Very soft mint background
            d = ImageDraw.Draw(img)
            d.text((25, 15), "UTM AI", fill="#2E8B57", font_size=28)  # Sea green text
            return ctk.CTkImage(light_image=img, dark_image=img, size=(180, 60))

    def load_data(self):
        try:
            with open("students.json", "r") as f:
                self.students = json.load(f)
            with open("courses.json", "r") as f:
                self.courses_available = json.load(f)
        except:
            self.students, self.courses_available = [], []

    def save_data(self):
        with open("students.json", "w") as f:
            json.dump(self.students, f, indent=4)

    def show_toast(self, message, is_error=False):
        if self.notification_label:
            self.notification_label.destroy()
        color = "#e74c3c" if is_error else "#27ae60"  # Red for error, green for success
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
    # VALIDATION FUNCTIONS
    # ==========================================
    def validate_name(self, name):
        name = name.strip()
        if len(name) < 4:
            self.show_toast("Name too short (minimum 4 characters).", is_error=True)
            return False
        if len(name.split()) < 2:
            self.show_toast(
                "Please enter at least two words (e.g., First Last).", is_error=True
            )
            return False
        if any(char.isdigit() for char in name):
            self.show_toast("Name cannot contain numbers.", is_error=True)
            return False
        if not re.match(r"^[a-zA-Z\s\-\']+$", name):
            self.show_toast(
                "Invalid characters in name. Only letters, spaces, hyphens, and apostrophes allowed.",
                is_error=True,
            )
            return False
        return name.title()

    def validate_matric(self, matric_raw):
        matric = matric_raw.strip().upper()
        if len(matric) != 9:
            self.show_toast("Matric must be exactly 9 characters.", is_error=True)
            return False
        if not matric.startswith("A25AI"):
            self.show_toast("Matric must start with 'A25AI'.", is_error=True)
            return False
        if not matric[5:].isdigit():
            self.show_toast("Last 4 digits must be numeric.", is_error=True)
            return False
        if any(s["matric"] == matric for s in self.students):
            self.show_toast("This matric number is already registered.", is_error=True)
            return False
        return matric

    # ==========================================
    # SCREENS
    # ==========================================
    def show_login_screen(self):
        self.clear_screen()
        frame = ctk.CTkFrame(self, corner_radius=15)
        frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.35, relheight=0.65)
        ctk.CTkLabel(frame, text="", image=self.logo_image).pack(pady=(40, 20))

        tabview = ctk.CTkTabview(frame, width=380, height=300)
        tabview.pack(pady=10)
        tabview.add("Login")
        tabview.add("Register")

        # Login
        self.entry_login_matric = ctk.CTkEntry(
            tabview.tab("Login"), placeholder_text="Matric Number (e.g. A25AI1234)"
        )
        self.entry_login_matric.pack(pady=30, padx=40, fill="x")
        ctk.CTkButton(
            tabview.tab("Login"), text="Access Dashboard", command=self.handle_login
        ).pack(pady=10, padx=40, fill="x")

        # Register
        self.entry_reg_name = ctk.CTkEntry(
            tabview.tab("Register"), placeholder_text="Full Name (e.g. Ali Bin Abu)"
        )
        self.entry_reg_name.pack(pady=(30, 10), padx=40, fill="x")
        self.entry_reg_matric = ctk.CTkEntry(
            tabview.tab("Register"), placeholder_text="Matric Number (A25AIxxxx)"
        )
        self.entry_reg_matric.pack(pady=10, padx=40, fill="x")
        ctk.CTkButton(
            tabview.tab("Register"),
            text="Create Account",
            fg_color="#27ae60",
            command=self.handle_register,
        ).pack(pady=15, padx=40, fill="x")

    def show_dashboard(self):
        self.clear_screen()
        sidebar = ctk.CTkFrame(self, width=260, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)

        ctk.CTkLabel(sidebar, text="", image=self.logo_image).pack(pady=(40, 20))
        ctk.CTkLabel(
            sidebar,
            text=f"Welcome,\n{self.current_student['name'].split()[0]}",
            font=("Roboto", 22, "bold"),
        ).pack(pady=10)

        self.credit_label = ctk.CTkLabel(
            sidebar,
            text=f"Credits: {self.current_student['total_credits']}/{MAX_CREDITS}",
            font=("Roboto", 18, "bold"),
            text_color="#2E8B57",  # Friendly sea green
        )
        self.credit_label.pack(pady=20)

        self.min_credit_warning = ctk.CTkLabel(
            sidebar,
            text="MINIMUM 12 CREDITS REQUIRED.",
            text_color="#E67E22",
            font=("Roboto", 14, "bold"),
        )
        if self.current_student["total_credits"] < MIN_CREDITS:
            self.min_credit_warning.pack(pady=(0, 20))
        else:
            self.min_credit_warning.pack_forget()

        ctk.CTkButton(
            sidebar,
            text="Log Out",
            text_color="#FFFFFF",
            fg_color="#8A8888",
            border_width=2,
            command=self.logout,
        ).pack(side="bottom", pady=40, padx=40, fill="x")

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
        student = next((s for s in self.students if s["matric"] == matric), None)
        if student:
            self.current_student = student
            self.show_dashboard()
            self.show_toast(f"Welcome back, {student['name'].split()[0]}!")
        else:
            self.show_toast("Student not found. Please register first.", is_error=True)

    def handle_register(self):
        raw_name = self.entry_reg_name.get()
        raw_matric = self.entry_reg_matric.get()

        if not raw_name or not raw_matric:
            self.show_toast("Please fill in all fields.", is_error=True)
            return

        name = self.validate_name(raw_name)
        if not name:
            return

        matric = self.validate_matric(raw_matric)
        if not matric:
            return

        new_student = {
            "name": name,
            "matric": matric,
            "registered_courses": [],
            "total_credits": 0,
        }
        self.students.append(new_student)
        self.save_data()
        self.current_student = new_student
        self.show_dashboard()
        self.show_toast("Account created! Add at least 12 credits.", is_error=False)

    def logout(self):
        if self.current_student["total_credits"] < MIN_CREDITS:
            self.show_toast(
                f"Cannot log out! Minimum {MIN_CREDITS} credits required.",
                is_error=True,
            )
            return
        self.current_student = None
        self.save_data()
        self.show_login_screen()

    def detect_clash(self, new_course):
        for n_slot in new_course["slots"]:
            n_day, n_time = n_slot
            n_start_str, n_end_str = n_time.split("-")
            n_start = int(n_start_str.split(":")[0])
            n_end = int(n_end_str.split(":")[0])

            for reg_course in self.current_student["registered_courses"]:
                for r_slot in reg_course["slots"]:
                    r_day, r_time = r_slot
                    if n_day != r_day:
                        continue
                    r_start_str, r_end_str = r_time.split("-")
                    r_start = int(r_start_str.split(":")[0])
                    r_end = int(r_end_str.split(":")[0])

                    if max(n_start, r_start) < min(n_end, r_end):
                        return f"CLASH: {reg_course['code']} ({n_day} {r_time})"
        return None

    def add_course_action(self, course):
        if self.current_student["total_credits"] + course["credit"] > MAX_CREDITS:
            self.show_toast(f"Exceeds {MAX_CREDITS} credit limit.", is_error=True)
            return
        clash = self.detect_clash(course)
        if clash:
            self.show_toast(clash, is_error=True)
            return
        self.current_student["registered_courses"].append(course)
        self.current_student["total_credits"] += course["credit"]
        self.save_data()
        self.refresh_ui()
        self.show_toast(f"Added {course['code']}", is_error=False)

    def drop_course_action(self, course):
        new_credits = self.current_student["total_credits"] - course["credit"]
        if new_credits < MIN_CREDITS:
            self.show_toast(
                f"Cannot drop! Would fall below {MIN_CREDITS} credits.", is_error=True
            )
            return
        self.current_student["registered_courses"] = [
            c
            for c in self.current_student["registered_courses"]
            if c["code"] != course["code"]
        ]
        self.current_student["total_credits"] = new_credits
        self.save_data()
        self.refresh_ui()
        self.show_toast(f"Dropped {course['code']}", is_error=False)

    def refresh_ui(self):
        if not self.current_student:
            return
        self.credit_label.configure(
            text=f"Credits: {self.current_student['total_credits']}/{MAX_CREDITS}"
        )
        if self.current_student["total_credits"] < MIN_CREDITS:
            self.min_credit_warning.pack(pady=(0, 20))
        else:
            self.min_credit_warning.pack_forget()

        self.populate_course_lists()
        if self.timetable_container:
            for w in self.timetable_container.winfo_children():
                w.destroy()
            self.draw_timetable_grid(self.timetable_container)

    # ==========================================
    # UI GENERATION
    # ==========================================
    def setup_course_tab(self, parent):
        parent.grid_columnconfigure((0, 1), weight=1)
        parent.grid_rowconfigure(0, weight=1)

        left = ctk.CTkFrame(parent)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        ctk.CTkLabel(left, text="Available Courses", font=("Roboto", 18, "bold")).pack(
            pady=10, padx=20, anchor="w"
        )
        self.search_var = ctk.StringVar()
        self.search_var.trace("w", lambda *args: self.populate_course_lists())
        ctk.CTkEntry(
            left, placeholder_text="Search...", textvariable=self.search_var
        ).pack(fill="x", padx=20, pady=5)
        self.scroll_avail = ctk.CTkScrollableFrame(left)
        self.scroll_avail.pack(fill="both", expand=True, padx=20, pady=10)

        right = ctk.CTkFrame(parent)
        right.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        ctk.CTkLabel(right, text="My Registration", font=("Roboto", 18, "bold")).pack(
            pady=10, padx=20, anchor="w"
        )
        self.scroll_reg = ctk.CTkScrollableFrame(right)
        self.scroll_reg.pack(fill="both", expand=True, padx=20, pady=10)

        self.populate_course_lists()

    def populate_course_lists(self):
        search = self.search_var.get().lower()
        for w in self.scroll_avail.winfo_children() + self.scroll_reg.winfo_children():
            w.destroy()
        reg_codes = {c["code"] for c in self.current_student["registered_courses"]}
        for c in self.courses_available:
            if c["code"] not in reg_codes and (
                not search or search in c["code"].lower() or search in c["name"].lower()
            ):
                self.create_course_card(self.scroll_avail, c, False)
        for c in self.current_student["registered_courses"]:
            self.create_course_card(self.scroll_reg, c, True)

    def create_course_card(self, parent, course, is_registered):
        card = ctk.CTkFrame(
            parent, corner_radius=10, fg_color="#f8f9fa"
        )  # Very light gray for cards
        card.pack(fill="x", pady=5, padx=5)
        info = ctk.CTkFrame(card, fg_color="transparent")
        info.pack(side="left", padx=10, pady=10, fill="both", expand=True)
        ctk.CTkLabel(info, text=course["code"], font=("Roboto", 14, "bold")).pack(
            anchor="w"
        )
        ctk.CTkLabel(
            info, text=f"{course['name']} ({course['credit']} Cr)", font=("Roboto", 12)
        ).pack(anchor="w")
        btn = ctk.CTkButton(
            card,
            text="Drop" if is_registered else "Add",
            width=60,
            fg_color="#e74c3c" if is_registered else "#27ae60",
            command=lambda c=course: (
                self.drop_course_action(c)
                if is_registered
                else self.add_course_action(c)
            ),
        )
        btn.pack(side="right", padx=10)

    def setup_timetable_tab(self, parent):
        self.timetable_container = ctk.CTkScrollableFrame(parent)
        self.timetable_container.pack(fill="both", expand=True, padx=10, pady=10)
        self.draw_timetable_grid(self.timetable_container)

    def draw_timetable_grid(self, container):
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        hours = list(range(8, 18))

        for i, h in enumerate(hours):
            ctk.CTkLabel(
                container, text=f"{h:02d}:00", font=("Roboto", 11, "bold")
            ).grid(row=0, column=i + 1, padx=5)

        for r, day in enumerate(days, start=1):
            ctk.CTkLabel(container, text=day, font=("Roboto", 12, "bold")).grid(
                row=r, column=0, padx=10, pady=20
            )
            for c in range(len(hours)):
                ctk.CTkFrame(container, fg_color="#f0f0f0", width=100, height=60).grid(
                    row=r, column=c + 1, padx=1, pady=1
                )

        for idx, course in enumerate(self.current_student["registered_courses"]):
            color = COURSE_COLORS[idx % len(COURSE_COLORS)]
            for slot in course["slots"]:
                day, time_range = slot
                if day not in days:
                    continue
                start_h = int(time_range.split("-")[0].split(":")[0])
                end_h = int(time_range.split("-")[1].split(":")[0])
                block = ctk.CTkFrame(container, fg_color=color, corner_radius=8)
                block.grid(
                    row=days.index(day) + 1,
                    column=(start_h - 8) + 1,
                    columnspan=(end_h - start_h),
                    sticky="nsew",
                    padx=2,
                    pady=5,
                )
                ctk.CTkLabel(
                    block,
                    text=f"{course['code']}\n{course['location']}",
                    font=("Roboto", 10, "bold"),
                    text_color="#333333",
                ).place(relx=0.5, rely=0.5, anchor="center")


if __name__ == "__main__":
    app = GROUP2App()
    app.mainloop()
