from tkinter import *
from PIL import Image, ImageTk # Corrected to consistent PIL import
from tkinter import ttk, messagebox
import sqlite3

class ResultClass:
    # --- CHANGE 1: Accept parent_rms instance ---
    def __init__(self, root, parent_rms=None): # parent_rms is now an optional argument
        self.root = root
        self.parent_rms = parent_rms # Store the reference
        self.root.title("Student Result Management System")
        self.root.geometry("1200x480+80+170")
        self.root.config(bg="white")
        self.root.focus_force()

        # --- All Variables ---
        self.var_select_student_roll = StringVar() # For the combobox to select student
        self.var_name = StringVar()
        self.var_course = StringVar()
        self.var_marks_ob = StringVar()
        self.var_full_marks = StringVar()

        # --- Title ---
        title = Label(self.root, text="Add Student Result", font=("goudy old style", 20, "bold"), bg="#0b5377", fg="white").place(x=10, y=15, width=1180, height=50)

        # --- Result Frame ---
        self.result_Frame = LabelFrame(self.root, text="Result Details", font=("goudy old style", 15, "bold"), bg="white")
        self.result_Frame.place(x=10, y=70, width=500, height=300)

        # --- Row 1: Select Student ---
        lbl_select_student = Label(self.result_Frame, text="Select Student", font=("goudy old style", 15, "bold"), bg="white").place(x=10, y=10)
        self.txt_select_student = ttk.Combobox(self.result_Frame, textvariable=self.var_select_student_roll, font=("goudy old style", 15), state='readonly', justify=CENTER)
        self.txt_select_student.place(x=150, y=10, width=150)
        self.txt_select_student.set("Select")
        self.txt_select_student.bind("<<ComboboxSelected>>", self.fetch_student_details)

        btn_search = Button(self.result_Frame, text="Search", font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white", cursor="hand2", command=self.fetch_student_details)
        btn_search.place(x=310, y=10, width=100)

        # --- Row 2: Name ---
        lbl_name = Label(self.result_Frame, text="Name", font=("goudy old style", 15, "bold"), bg="white").place(x=10, y=60)
        txt_name = Entry(self.result_Frame, textvariable=self.var_name, font=("goudy old style", 15), bg="lightyellow", state='readonly')
        txt_name.place(x=150, y=60, width=300)

        # --- Row 3: Course ---
        lbl_course = Label(self.result_Frame, text="Course", font=("goudy old style", 15, "bold"), bg="white").place(x=10, y=110)
        txt_course = Entry(self.result_Frame, textvariable=self.var_course, font=("goudy old style", 15), bg="lightyellow", state='readonly')
        txt_course.place(x=150, y=110, width=300)

        # --- Row 4: Marks Obtained ---
        lbl_marks_ob = Label(self.result_Frame, text="Marks Obtained", font=("goudy old style", 15, "bold"), bg="white").place(x=10, y=160)
        txt_marks_ob = Entry(self.result_Frame, textvariable=self.var_marks_ob, font=("goudy old style", 15), bg="lightyellow")
        txt_marks_ob.place(x=150, y=160, width=300)

        # --- Row 5: Full Marks ---
        lbl_full_marks = Label(self.result_Frame, text="Full Marks", font=("goudy old style", 15, "bold"), bg="white").place(x=10, y=210)
        txt_full_marks = Entry(self.result_Frame, textvariable=self.var_full_marks, font=("goudy old style", 15), bg="lightyellow")
        txt_full_marks.place(x=150, y=210, width=300)

        # --- Submit & Clear Buttons ---
        btn_submit = Button(self.root, text="Submit", font=("goudy old style", 15, "bold"), bg="#2196f3", fg="white", cursor="hand2", command=self.submit_result)
        btn_submit.place(x=170, y=390, width=120, height=35)
        btn_clear = Button(self.root, text="Clear", font=("goudy old style", 15, "bold"), bg="#607d8b", fg="white", cursor="hand2", command=self.clear_fields)
        btn_clear.place(x=300, y=390, width=120, height=35)

        # --- Image ---
        # --- CHANGE 2: Image path correction if 'logo.png' isn't meant here, use 'results.png' ---
        try:
            self.img_results = Image.open("images/logo_pg.png") # Changed from logo.png
            self.img_results = self.img_results.resize((500, 300), Image.Resampling.LANCZOS)
            self.img_results = ImageTk.PhotoImage(self.img_results)
            self.lbl_results_img = Label(self.root, image=self.img_results)
            self.lbl_results_img.place(x=600, y=100, width=500, height=300)
        except FileNotFoundError:
            print("Error: results.png not found. Ensure it's in the 'images' folder.")
            # Fallback for missing image
            Label(self.root, text="[Results Image Placeholder]", font=("Arial", 12), bg="lightgray", fg="red").place(x=600, y=100, width=500, height=300)


        # --- Footer ---
        lbl_footer = Label(self.root, text="SRMS:Student Result Management System Contact Us for any Technical Issue: 98xxxxxx01",
                           font=("goudy old style", 10, "bold"), bg="#0b5377", fg="white")
        lbl_footer.pack(side=BOTTOM, fill=X)


        # Call function to populate student dropdown on start
        self.fetch_student_rolls()

    # --- Methods ---

    def fetch_student_rolls(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT roll FROM student")
            rolls = cur.fetchall()
            self.student_rolls = [roll[0] for roll in rolls]
            self.txt_select_student['values'] = self.student_rolls
        except Exception as ex:
            messagebox.showerror("Error", f"Error fetching student rolls: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def fetch_student_details(self, event=None):
        selected_roll = self.var_select_student_roll.get()
        if selected_roll == "Select" or selected_roll == "":
            self.var_name.set("")
            self.var_course.set("")
            return

        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT name, course FROM student WHERE roll=?", (selected_roll,))
            student_data = cur.fetchone()
            if student_data:
                self.var_name.set(student_data[0])
                self.var_course.set(student_data[1])
            else:
                self.var_name.set("")
                self.var_course.set("")
                messagebox.showerror("Error", "Student not found with this Roll No.", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error fetching student details: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def submit_result(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            if self.var_select_student_roll.get() == "Select" or self.var_marks_ob.get() == "" or self.var_full_marks.get() == "":
                messagebox.showerror("Error", "All fields are required", parent=self.root)
                return

            try:
                marks_ob = int(self.var_marks_ob.get())
                full_marks = int(self.var_full_marks.get())
                if marks_ob < 0 or full_marks <= 0 or marks_ob > full_marks:
                    messagebox.showerror("Error", "Invalid Marks or Full Marks", parent=self.root)
                    return
            except ValueError:
                messagebox.showerror("Error", "Marks Obtained and Full Marks must be numbers", parent=self.root)
                return

            status = "Pass" if (marks_ob / full_marks) * 100 >= 40 else "Fail"

            cur.execute("SELECT * FROM result WHERE roll=? AND course=?", (self.var_select_student_roll.get(), self.var_course.get()))
            row = cur.fetchone()
            if row is not None:
                messagebox.showerror("Error", "Result for this student and course already exists. Use 'Update' if you want to modify.", parent=self.root)
            else:
                cur.execute("INSERT INTO result (roll, name, course, marks_ob, full_marks, status) VALUES(?,?,?,?,?,?)",
                            (self.var_select_student_roll.get(),
                             self.var_name.get(),
                             self.var_course.get(),
                             marks_ob,
                             full_marks,
                             status
                            ))
                con.commit()
                messagebox.showinfo("Success", "Result Added Successfully", parent=self.root)
                self.clear_fields()
                # --- CHANGE 3: Call update_counts on parent RMS ---
                if self.parent_rms:
                    self.parent_rms.update_counts()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def clear_fields(self):
        self.var_select_student_roll.set("Select")
        self.var_name.set("")
        self.var_course.set("")
        self.var_marks_ob.set("")
        self.var_full_marks.set("")
        self.fetch_student_rolls() # Re-fetch rolls to ensure list is fresh (e.g., if new students added)

# --- For standalone testing ---
if __name__ == "__main__":
    root = Tk()
    # Pass None for parent_rms when testing standalone
    obj = ResultClass(root, None) # <--- CHANGE 4: Pass None here for standalone
    root.mainloop()