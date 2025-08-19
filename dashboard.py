from tkinter import *
from PIL import Image, ImageTk
import sqlite3
from tkinter import messagebox # Correctly imported for dialog boxes

# Import all other classes for direct instantiation
from course import CourseClass
from student import studentClass
from result import ResultClass

# IMPORTANT: ViewResultClass is intentionally NOT imported here at the top level
# to prevent circular import issues with report.py.
# It will be imported inside the view_results method when needed.

class RMS:
    def __init__(self, root):
        self.root = root
        self.root.title("Result Management System")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="#ecf0f1")

        # === Title Bar ===
        try:
            img = Image.open("images/logo.png")
            img = img.resize((50, 50), Image.Resampling.LANCZOS)
            self.logo_dash = ImageTk.PhotoImage(img)
        except FileNotFoundError:
            print(f"Error: logo.png not found at 'images/logo.png'. Please ensure it's in the 'images' folder.")
            self.logo_dash = None # Assign None to avoid program crash if image is missing

        title = Label(
            self.root,
            text="   Result Management System",
            compound=LEFT, # Image will be to the left of the text
            image=self.logo_dash, # Assign the PhotoImage
            font=("Segoe UI", 22, "bold"),
            bg="#34495e", # Dark blue/grey background
            fg="white", # White foreground text
            padx=10 # Padding on the left side
        )
        title.place(x=0, y=0, relwidth=1, height=60) # Place title bar across the top

        # === Menu Bar (Frame for navigation buttons) ===
        M_Frame = Frame(self.root, bg="white", bd=2, relief=FLAT)
        M_Frame.place(x=10, y=80, width=1325, height=60)

        menu_title = Label(M_Frame, text="Menu", font=("Segoe UI", 15, "bold"), bg="white", fg="#2c3e50")
        menu_title.place(x=10, y=15)

        # === Navigation Buttons ===
        # Common button styling can be applied if needed, but current specific styles are fine.
        btn_course = Button(M_Frame, text="Course", font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white", cursor="hand2", command=self.add_course)
        btn_course.place(x=150, y=10, width=150, height=40)

        btn_student = Button(M_Frame, text="Student", font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white", cursor="hand2", command=self.add_student)
        btn_student.place(x=310, y=10, width=150, height=40)

        btn_result = Button(M_Frame, text="Result", font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white", cursor="hand2", command=self.add_result)
        btn_result.place(x=470, y=10, width=150, height=40)

        btn_view = Button(M_Frame, text="View Student Results", font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white", cursor="hand2", command=self.view_results)
        btn_view.place(x=630, y=10, width=200, height=40)

        btn_logout = Button(M_Frame, text="Logout", font=("goudy old style", 15, "bold"), bg="#e74c3c", fg="white", cursor="hand2", command=self.logout) # FIX: Added command
        btn_logout.place(x=840, y=10, width=100, height=40)

        btn_exit = Button(M_Frame, text="Exit", font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white", cursor="hand2", command=self.root.destroy)
        btn_exit.place(x=950, y=10, width=100, height=40)

        # === Dashboard Image (Main content area image) ===
        try:
            dashboard_img = Image.open("images/dashboard.png")
            dashboard_img = dashboard_img.resize((600, 300), Image.Resampling.LANCZOS)
            self.dashboard_photo = ImageTk.PhotoImage(dashboard_img)
            Label(self.root, image=self.dashboard_photo, bd=0, bg="#ecf0f1").place(x=700, y=150)
        except FileNotFoundError:
            print(f"Error: dashboard.png not found at 'images/dashboard.png'. Please ensure it's in the 'images' folder.")
            # Can place a placeholder label here if image is critical
            Label(self.root, text="[Dashboard Image Missing]", font=("Arial", 12), bg="lightgray", fg="red").place(x=700, y=150, width=600, height=300)

        # === Info Cards (Dynamic Counts) ===
        # These labels are now instance variables to allow dynamic updates
        self.lbl_courses_count = Label(self.root, text="Total Courses\n[0]", # Initial count is 0
              font=("Segoe UI", 20, "bold"),
              bg="#27ae60", # Green
              fg="white",
              relief=FLAT,
              justify=CENTER
        )
        self.lbl_courses_count.place(x=700, y=470, width=180, height=100)

        self.lbl_students_count = Label(self.root, text="Total Students\n[0]", # Initial count is 0
              font=("Segoe UI", 20, "bold"),
              bg="#f39c12", # Orange
              fg="white",
              relief=FLAT,
              justify=CENTER
        )
        self.lbl_students_count.place(x=890, y=470, width=180, height=100)

        self.lbl_results_count = Label(self.root, text="Total Results\n[0]", # Initial count is 0
              font=("Segoe UI", 20, "bold"),
              bg="#2980b9", # Blue
              fg="white",
              relief=FLAT,
              justify=CENTER
        )
        self.lbl_results_count.place(x=1080, y=470, width=180, height=100)

        self.update_counts() # Call to populate counts on startup

        # === Footer ===
        footer = Label(
            self.root,
            text="© 2025 Student Result Management System | Developed by Abhiram S",
            font=("Segoe UI", 10),
            bg="#34495e", # Dark blue/grey, same as title
            fg="white",
            pady=5
        )
        footer.pack(side=BOTTOM, fill=X) # Packs at the bottom, expands horizontally

    # === Method to open Course Window ===
    def add_course(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = CourseClass(self.new_win, self) # Pass parent RMS instance
        self.new_win.focus_set() # Focus on the new window
        self.new_win.grab_set() # Make it modal (blocks interaction with main window)

    # === Method to open Student Window ===
    def add_student(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = studentClass(self.new_win, self) # Pass parent RMS instance
        self.new_win.focus_set()
        self.new_win.grab_set()

    # === Method to open Result Window (Add Result) ===
    def add_result(self):
        self.new_win = Toplevel(self.root)
        self.new_obj = ResultClass(self.new_win, self) # Pass parent RMS instance
        self.new_win.focus_set()
        self.new_win.grab_set()

    # === Method to open View Student Results Window ===
    def view_results(self):
        # IMPORTANT: Import ViewResultClass here to avoid circular import issues
        from report import ViewResultClass # <--- Correctly imported HERE
        self.new_win = Toplevel(self.root)
        self.new_obj = ViewResultClass(self.new_win, self) # Pass parent RMS instance
        self.new_win.focus_set()
        self.new_win.grab_set()

    # === Method to fetch and update counts dynamically ===
    def update_counts(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT COUNT(*) FROM course")
            courses_count = cur.fetchone()[0]

            cur.execute("SELECT COUNT(*) FROM student")
            students_count = cur.fetchone()[0]

            cur.execute("SELECT COUNT(*) FROM result")
            results_count = cur.fetchone()[0]

            self.lbl_courses_count.config(text=f"Total Courses\n[{courses_count}]")
            self.lbl_students_count.config(text=f"Total Students\n[{students_count}]")
            self.lbl_results_count.config(text=f"Total Results\n[{results_count}]")

        except Exception as ex:
            # Print error for debugging. Avoid messagebox here as it's a background update.
            print(f"Error updating counts: {str(ex)}")
        finally:
            if con: # Ensure connection is closed even if an error occurs
                con.close()

    # === Logout Functionality ===
    def logout(self):
        confirm = messagebox.askyesno("Logout", "Are you sure you want to logout?", parent=self.root)
        if confirm:
            self.root.destroy() # Closes the current dashboard window
            # Optional: To re-open the login window after logout, uncomment the following lines.
            # Make sure login.py exists and the Login_System class is correctly defined.
            # from login import Login_System
            # root_login = Tk()
            # Login_System(root_login)
            # root_login.mainloop()

# === Main execution block for running the dashboard directly (for testing) ===
if __name__ == "__main__":
    root = Tk()
    obj = RMS(root)
    root.mainloop()