from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import sqlite3

class studentClass:
    def __init__(self, root, parent_rms=None):
        self.root = root
        self.parent_rms = parent_rms
        self.root.title("Student Result Management System")
        self.root.geometry("1200x480+80+170")
        self.root.config(bg="white")
        self.root.focus_force()

        # --- All Variables ---
        self.var_roll_no = StringVar()
        self.var_name = StringVar()
        self.var_email = StringVar()
        self.var_gender = StringVar()
        self.var_dob = StringVar()
        self.var_contact = StringVar()
        self.var_adm_date = StringVar()
        self.var_select_course = StringVar()

        # --- FIX: Move these StringVar declarations here ---
        self.var_state = StringVar()
        self.var_city = StringVar()
        self.var_pin = StringVar()
        # --- End FIX ---

        self.var_search_by = StringVar()
        self.var_search_txt = StringVar()

        self.course_list = []
        self.fetch_course()

        # --- Title ---
        title=Label(self.root,text="Manage Student Details",font=("goudy old style",20,"bold"),bg="#033054",fg="white").place(x=0,y=0,relwidth=1,height=50)

        # --- Search Panel ---
        lbl_search_rollno = Label(self.root, text="Search | Roll No.", font=("goudy old style", 15, "bold"), bg="white").place(x=720, y=70)
        txt_search_rollno = Entry(self.root, textvariable=self.var_search_txt, font=("goudy old style", 15), bg="lightyellow")
        txt_search_rollno.place(x=870, y=70, width=180)
        btn_search = Button(self.root, text="Search", font=("goudy old style", 15, "bold"), bg="#033054", fg="white", cursor="hand2", command=self.search)
        btn_search.place(x=1060, y=70, width=120, height=30)

        # --- Content Frame (Student Details Input) ---
        self.C_Frame = LabelFrame(self.root, text="Student Details", font=("goudy old style", 15, "bold"), bg="white")
        self.C_Frame.place(x=20, y=100, width=650, height=360)

        # Row 1
        lbl_roll = Label(self.C_Frame, text="Roll No.", font=("goudy old style", 15, "bold"), bg="white").place(x=10, y=10)
        txt_roll = Entry(self.C_Frame, textvariable=self.var_roll_no, font=("goudy old style", 15), bg="lightyellow")
        txt_roll.place(x=120, y=10, width=200)

        lbl_dob = Label(self.C_Frame, text="D.O.B(dd-mm-yyyy)", font=("goudy old style", 15, "bold"), bg="white").place(x=340, y=10)
        txt_dob = Entry(self.C_Frame, textvariable=self.var_dob, font=("goudy old style", 15), bg="lightyellow")
        txt_dob.place(x=500, y=10, width=120)

        # Row 2
        lbl_name = Label(self.C_Frame, text="Name", font=("goudy old style", 15, "bold"), bg="white").place(x=10, y=50)
        txt_name = Entry(self.C_Frame, textvariable=self.var_name, font=("goudy old style", 15), bg="lightyellow")
        txt_name.place(x=120, y=50, width=200)

        lbl_contact = Label(self.C_Frame, text="Contact No.", font=("goudy old style", 15, "bold"), bg="white").place(x=340, y=50)
        txt_contact = Entry(self.C_Frame, textvariable=self.var_contact, font=("goudy old style", 15), bg="lightyellow")
        txt_contact.place(x=500, y=50, width=120)

        # Row 3
        lbl_email = Label(self.C_Frame, text="Email", font=("goudy old style", 15, "bold"), bg="white").place(x=10, y=90)
        txt_email = Entry(self.C_Frame, textvariable=self.var_email, font=("goudy old style", 15), bg="lightyellow")
        txt_email.place(x=120, y=90, width=200)

        lbl_select_course = Label(self.C_Frame, text="Select Course", font=("goudy old style", 15, "bold"), bg="white").place(x=340, y=90)
        self.txt_select_course = ttk.Combobox(self.C_Frame, textvariable=self.var_select_course, font=("goudy old style", 15), state='readonly', values=self.course_list)
        self.txt_select_course.place(x=500, y=90, width=120)
        self.txt_select_course.set("Select")

        # Row 4
        lbl_gender = Label(self.C_Frame, text="Gender", font=("goudy old style", 15, "bold"), bg="white").place(x=10, y=130)
        self.txt_gender = ttk.Combobox(self.C_Frame, textvariable=self.var_gender, font=("goudy old style", 15), state='readonly')
        self.txt_gender['values'] = ("Select", "Male", "Female", "Other")
        self.txt_gender.place(x=120, y=130, width=200)
        self.txt_gender.set("Select Gender")

        lbl_adm_date = Label(self.C_Frame, text="Admission Date", font=("goudy old style", 15, "bold"), bg="white").place(x=340, y=130)
        txt_adm_date = Entry(self.C_Frame, textvariable=self.var_adm_date, font=("goudy old style", 15), bg="lightyellow")
        txt_adm_date.place(x=500, y=130, width=120)

        # Row 5 (State, City, Pin Code)
        lbl_state = Label(self.C_Frame, text="State", font=("goudy old style", 15, "bold"), bg="white").place(x=10, y=170)
        txt_state = Entry(self.C_Frame, textvariable=self.var_state, font=("goudy old style", 15), bg="lightyellow")
        txt_state.place(x=120, y=170, width=100)

        lbl_city = Label(self.C_Frame, text="City", font=("goudy old style", 15, "bold"), bg="white").place(x=240, y=170)
        txt_city = Entry(self.C_Frame, textvariable=self.var_city, font=("goudy old style", 15), bg="lightyellow")
        txt_city.place(x=300, y=170, width=100)

        lbl_pin = Label(self.C_Frame, text="Pin Code", font=("goudy old style", 15, "bold"), bg="white").place(x=420, y=170)
        txt_pin = Entry(self.C_Frame, textvariable=self.var_pin, font=("goudy old style", 15), bg="lightyellow")
        txt_pin.place(x=500, y=170, width=120)

        # Row 6 (Address)
        lbl_address = Label(self.C_Frame, text="Address", font=("goudy old style", 15, "bold"), bg="white").place(x=10, y=210)
        self.txt_address = Text(self.C_Frame, font=("goudy old style", 15), bg="lightyellow")
        self.txt_address.place(x=120, y=210, width=500, height=70)

        # --- Action Buttons ---
        btn_add = Button(self.C_Frame, text="Save", font=("goudy old style", 15, "bold"), bg="#2196f3", fg="white", cursor="hand2", command=self.add_student)
        btn_add.place(x=120, y=300, width=110, height=35)
        btn_update = Button(self.C_Frame, text="Update", font=("goudy old style", 15, "bold"), bg="#4CAF50", fg="white", cursor="hand2", command=self.update_student)
        btn_update.place(x=240, y=300, width=110, height=35)
        btn_delete = Button(self.C_Frame, text="Delete", font=("goudy old style", 15, "bold"), bg="#f44336", fg="white", cursor="hand2", command=self.delete_student)
        btn_delete.place(x=360, y=300, width=110, height=35)
        btn_clear = Button(self.C_Frame, text="Clear", font=("goudy old style", 15, "bold"), bg="#607d8b", fg="white", cursor="hand2", command=self.clear_fields)
        btn_clear.place(x=480, y=300, width=110, height=35)

        # --- Student Details Table (Right Side) ---
        self.S_Frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        self.S_Frame.place(x=680, y=100, width=500, height=360)

        scrolly = Scrollbar(self.S_Frame, orient=VERTICAL)
        scrollx = Scrollbar(self.S_Frame, orient=HORIZONTAL)
        self.StudentTable = ttk.Treeview(self.S_Frame, columns=("roll", "name", "email", "gender", "dob", "contact", "admission", "course", "state", "city", "pin", "address"), xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.StudentTable.xview)
        scrolly.config(command=self.StudentTable.yview)

        self.StudentTable.heading("roll", text="Roll No.")
        self.StudentTable.heading("name", text="Name")
        self.StudentTable.heading("email", text="Email")
        self.StudentTable.heading("gender", text="Gender")
        self.StudentTable.heading("dob", text="D.O.B")
        self.StudentTable.heading("contact", text="Contact No.")
        self.StudentTable.heading("admission", text="Admission Date")
        self.StudentTable.heading("course", text="Course")
        self.StudentTable.heading("state", text="State")
        self.StudentTable.heading("city", text="City")
        self.StudentTable.heading("pin", text="Pin Code")
        self.StudentTable.heading("address", text="Address")

        self.StudentTable["show"] = 'headings'

        # Set column widths (adjust as needed based on your data)
        self.StudentTable.column("roll", width=80)
        self.StudentTable.column("name", width=120)
        self.StudentTable.column("email", width=150)
        self.StudentTable.column("gender", width=80)
        self.StudentTable.column("dob", width=100)
        self.StudentTable.column("contact", width=100)
        self.StudentTable.column("admission", width=120)
        self.StudentTable.column("course", width=100)
        self.StudentTable.column("state", width=80)
        self.StudentTable.column("city", width=80)
        self.StudentTable.column("pin", width=80)
        self.StudentTable.column("address", width=200)

        self.StudentTable.pack(fill=BOTH, expand=1)
        self.StudentTable.bind("<ButtonRelease-1>", self.get_data)

        # Initial display of data
        self.show_students()

    # --- New method to fetch course names ---
    def fetch_course(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT name FROM course")
            courses = cur.fetchall()
            self.course_list = [c[0] for c in courses]
            self.course_list.insert(0, "Select")
        except Exception as ex:
            messagebox.showerror("Error", f"Error fetching courses: {str(ex)}", parent=self.root)
        finally:
            con.close()

    # --- Database Operations ---

    def add_student(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            if self.var_roll_no.get() == "" or self.var_name.get() == "" or self.var_email.get() == "" or self.var_gender.get() == "Select Gender" or self.var_select_course.get() == "Select":
                messagebox.showerror("Error", "Roll No, Name, Email, Gender, and Course are required", parent=self.root)
            else:
                cur.execute("SELECT * FROM student WHERE roll=?", (self.var_roll_no.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "This Roll No. already exists, please try another one", parent=self.root)
                else:
                    cur.execute("INSERT INTO student (roll, name, email, gender, dob, contact, admission, course, state, city, pin, address) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                                (self.var_roll_no.get(),
                                 self.var_name.get(),
                                 self.var_email.get(),
                                 self.var_gender.get(),
                                 self.var_dob.get(),
                                 self.var_contact.get(),
                                 self.var_adm_date.get(),
                                 self.var_select_course.get(),
                                 self.var_state.get(),
                                 self.var_city.get(),
                                 self.var_pin.get(),
                                 self.txt_address.get("1.0",END)
                                ))
                    con.commit()
                    messagebox.showinfo("Success", "Student Added Successfully", parent=self.root)
                    self.show_students()
                    self.clear_fields()
                    if self.parent_rms:
                        self.parent_rms.update_counts()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def update_student(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            if self.var_roll_no.get() == "":
                messagebox.showerror("Error", "Roll No. is required for update", parent=self.root)
            else:
                cur.execute("SELECT * FROM student WHERE roll=?", (self.var_roll_no.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "This Roll No. does not exist", parent=self.root)
                else:
                    cur.execute("UPDATE student SET name=?, email=?, gender=?, dob=?, contact=?, admission=?, course=?, state=?, city=?, pin=?, address=? WHERE roll=?",
                                (self.var_name.get(),
                                 self.var_email.get(),
                                 self.var_gender.get(),
                                 self.var_dob.get(),
                                 self.var_contact.get(),
                                 self.var_adm_date.get(),
                                 self.var_select_course.get(),
                                 self.var_state.get(),
                                 self.var_city.get(),
                                 self.var_pin.get(),
                                 self.txt_address.get("1.0",END),
                                 self.var_roll_no.get()
                                ))
                    con.commit()
                    messagebox.showinfo("Success", "Student Updated Successfully", parent=self.root)
                    self.show_students()
                    if self.parent_rms:
                        self.parent_rms.update_counts()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def delete_student(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            if self.var_roll_no.get() == "":
                messagebox.showerror("Error", "Roll No. is required for deletion", parent=self.root)
            else:
                cur.execute("SELECT * FROM student WHERE roll=?", (self.var_roll_no.get(),))
                row = cur.fetchone()
                if row is None:
                    messagebox.showerror("Error", "This Roll No. does not exist", parent=self.root)
                else:
                    op = messagebox.askyesno("Confirm Delete", "Do you really want to delete this student?", parent=self.root)
                    if op:
                        cur.execute("DELETE FROM student WHERE roll=?", (self.var_roll_no.get(),))
                        con.commit()
                        messagebox.showinfo("Delete", "Student Deleted Successfully", parent=self.root)
                        self.clear_fields()
                        self.show_students()
                        if self.parent_rms:
                            self.parent_rms.update_counts()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def clear_fields(self):
        self.var_roll_no.set("")
        self.var_name.set("")
        self.var_email.set("")
        self.var_gender.set("Select Gender")
        self.var_dob.set("")
        self.var_contact.set("")
        self.var_adm_date.set("")
        self.var_select_course.set("Select")
        self.var_state.set("")
        self.var_city.set("")
        self.var_pin.set("")
        self.txt_address.delete("1.0", END)
        self.var_search_txt.set("")
        self.fetch_course()

    def show_students(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM student")
            rows = cur.fetchall()
            self.StudentTable.delete(*self.StudentTable.get_children())
            for row in rows:
                self.StudentTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def get_data(self, event):
        cursor_row = self.StudentTable.focus()
        content = self.StudentTable.item(cursor_row)
        row = content['values']
        if row:
            self.var_roll_no.set(row[0])
            self.var_name.set(row[1])
            self.var_email.set(row[2])
            self.var_gender.set(row[3])
            self.var_dob.set(row[4])
            self.var_contact.set(row[5])
            self.var_adm_date.set(row[6])
            self.var_select_course.set(row[7])
            self.var_state.set(row[8])
            self.var_city.set(row[9])
            self.var_pin.set(row[10])
            self.txt_address.delete("1.0", END)
            self.txt_address.insert(END, row[11])

    def search(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            if self.var_search_txt.get() == "":
                messagebox.showerror("Error", "Search input is required", parent=self.root)
            else:
                cur.execute("SELECT * FROM student WHERE roll LIKE '%" + self.var_search_txt.get() + "%'")
                rows = cur.fetchall()
                if len(rows) != 0:
                    self.StudentTable.delete(*self.StudentTable.get_children())
                    for row in rows:
                        self.StudentTable.insert('', END, values=row)
                else:
                    self.show_students()
                    messagebox.showinfo("Info", "No student found with the given Roll No.", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

if __name__ == "__main__":
    root=Tk()
    obj=studentClass(root, None)
    root.mainloop()
