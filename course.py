from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3

class CourseClass:
    # --- CHANGE 1: Accept parent_rms instance ---
    def __init__(self, root, parent_rms=None): # parent_rms is now an optional argument
        self.root = root
        self.parent_rms = parent_rms # Store the reference
        self.root.title("Result Management System")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="#ecf0f1")
        self.root.focus_force()

        # === Title ===
        title = Label(self.root, text="Manage Course Details", font=("Segoe UI", 22, "bold"), bg="#34495e", fg="white")
        title.place(x=10, y=15, width=1320, height=40)

        # === Variables ===
        self.var_course = StringVar()
        self.var_duration = StringVar()
        self.var_charges = StringVar()
        self.var_search = StringVar()
        self.selected_course_id = None  # To track selected row for update/delete

        # === Entry Fields ===
        Label(self.root, text="Course Name", font=("Segoe UI", 15, "bold"), bg="#ecf0f1").place(x=50, y=80)
        txt_courseName = Entry(self.root, textvariable=self.var_course, font=("Segoe UI", 14), bg="white")
        txt_courseName.place(x=200, y=80, width=300)

        Label(self.root, text="Duration", font=("Segoe UI", 15, "bold"), bg="#ecf0f1").place(x=50, y=130)
        txt_duration = Entry(self.root, textvariable=self.var_duration, font=("Segoe UI", 14), bg="white")
        txt_duration.place(x=200, y=130, width=300)

        Label(self.root, text="Charges", font=("Segoe UI", 15, "bold"), bg="#ecf0f1").place(x=50, y=180)
        txt_charges = Entry(self.root, textvariable=self.var_charges, font=("Segoe UI", 14), bg="white")
        txt_charges.place(x=200, y=180, width=300)

        Label(self.root, text="Description", font=("Segoe UI", 15, "bold"), bg="#ecf0f1").place(x=50, y=230)
        self.txt_description = Text(self.root, font=("Segoe UI", 14), bg="white")
        self.txt_description.place(x=200, y=230, width=500, height=100)

        # === Buttons ===
        self.btn_add = Button(self.root, text="Save", font=("Segoe UI", 15, "bold"), bg="#2ecc71", fg="white", command=self.add)
        self.btn_add.place(x=150, y=400, width=110, height=40)

        self.btn_update = Button(self.root, text="Update", font=("Segoe UI", 15, "bold"), bg="#3498db", fg="white", command=self.update)
        self.btn_update.place(x=280, y=400, width=110, height=40)

        self.btn_delete = Button(self.root, text="Delete", font=("Segoe UI", 15, "bold"), bg="#e74c3c", fg="white", command=self.delete)
        self.btn_delete.place(x=410, y=400, width=110, height=40)

        self.btn_clear = Button(self.root, text="Clear", font=("Segoe UI", 15, "bold"), bg="#f1c40f", fg="white", command=self.clear)
        self.btn_clear.place(x=540, y=400, width=110, height=40)

        # === Search Course Section ===
        Label(self.root, text="Search Course", font=("Segoe UI", 15, "bold"), bg="#ecf0f1").place(x=720, y=60)
        txt_search_course = Entry(self.root, textvariable=self.var_search, font=("Segoe UI", 14), bg="lightyellow")
        txt_search_course.place(x=880, y=60, width=200)

        btn_search = Button(self.root, text="Search", font=("Segoe UI", 15, "bold"), bg="#2980b9", fg="white", cursor="hand2", command=self.search_course)
        btn_search.place(x=1100, y=58, width=120, height=35)

        btn_show_all = Button(self.root, text="Show All", font=("Segoe UI", 15, "bold"), bg="#16a085", fg="white", cursor="hand2", command=self.show_data)
        btn_show_all.place(x=1230, y=58, width=100, height=35)

        # === Treeview Frame ===
        self.course_frame = Frame(self.root, bd=2, relief=RIDGE)
        self.course_frame.place(x=720, y=100, width=570, height=400)

        scrollx = Scrollbar(self.course_frame, orient=HORIZONTAL)
        scrolly = Scrollbar(self.course_frame, orient=VERTICAL)

        self.CourseTable = ttk.Treeview(
            self.course_frame,
            columns=("cid", "name", "duration", "charges", "description"),
            xscrollcommand=scrollx.set,
            yscrollcommand=scrolly.set
        )
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.CourseTable.xview)
        scrolly.config(command=self.CourseTable.yview)

        self.CourseTable.heading("cid", text="Course ID")
        self.CourseTable.heading("name", text="Course Name")
        self.CourseTable.heading("duration", text="Duration")
        self.CourseTable.heading("charges", text="Charges")
        self.CourseTable.heading("description", text="Description")
        self.CourseTable["show"] = "headings"

        self.CourseTable.column("cid", width=80)
        self.CourseTable.column("name", width=120)
        self.CourseTable.column("duration", width=100)
        self.CourseTable.column("charges", width=100)
        self.CourseTable.column("description", width=150)

        self.CourseTable.pack(fill=BOTH, expand=1)
        self.CourseTable.bind("<ButtonRelease-1>", self.get_data)

        self.create_table() # This will ensure the table exists
        self.show_data()

    def create_table(self):
        con = sqlite3.connect(database='rms.db')
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS course (
                cid INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                duration TEXT,
                charges TEXT,
                description TEXT
            )
        """)
        con.commit()
        con.close()

    def add(self):
        con = sqlite3.connect(database='rms.db')
        cur = con.cursor()
        try:
            if self.var_course.get() == "":
                messagebox.showerror("Error", "Course name should be required", parent=self.root)
            else:
                cur.execute("SELECT * FROM course WHERE name=?", (self.var_course.get(),))
                row = cur.fetchone()
                if row is not None:
                    messagebox.showerror("Error", "Course name already exists", parent=self.root)
                else:
                    cur.execute("INSERT INTO course (name, duration, charges, description) VALUES (?, ?, ?, ?)",
                        (
                            self.var_course.get(),
                            self.var_duration.get(),
                            self.var_charges.get(),
                            self.txt_description.get("1.0", END).strip()
                        )
                    )
                    con.commit()
                    messagebox.showinfo("Success", "Course added successfully", parent=self.root)
                    self.show_data()
                    self.clear()
                    # --- CHANGE 2: Call update_counts on parent RMS ---
                    if self.parent_rms: # Only call if parent_rms exists
                        self.parent_rms.update_counts()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    def get_data(self, event):
        selected = self.CourseTable.focus()
        content = self.CourseTable.item(selected)
        row = content['values']
        if row:
            self.selected_course_id = row[0]
            self.var_course.set(row[1])
            self.var_duration.set(row[2])
            self.var_charges.set(row[3])
            self.txt_description.delete("1.0", END)
            self.txt_description.insert(END, row[4])

    def update(self):
        if self.selected_course_id is None:
            messagebox.showerror("Error", "Please select a course to update", parent=self.root)
            return
        con = sqlite3.connect(database='rms.db')
        cur = con.cursor()
        try:
            # Check for duplicate name if name is changed to an existing one
            cur.execute("SELECT * FROM course WHERE name=? AND cid != ?", (self.var_course.get(), self.selected_course_id))
            row_duplicate = cur.fetchone()
            if row_duplicate is not None:
                messagebox.showerror("Error", "Course name already exists for another course", parent=self.root)
                return

            cur.execute("UPDATE course SET name=?, duration=?, charges=?, description=? WHERE cid=?",
                        (
                            self.var_course.get(),
                            self.var_duration.get(),
                            self.var_charges.get(),
                            self.txt_description.get("1.0", END).strip(),
                            self.selected_course_id
                        ))
            con.commit()
            messagebox.showinfo("Success", "Course updated successfully", parent=self.root)
            self.show_data()
            self.clear()
            # --- CHANGE 3: Call update_counts on parent RMS ---
            if self.parent_rms: # Only call if parent_rms exists
                self.parent_rms.update_counts()
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    def delete(self):
        # Using selected_course_id for deletion if available for more robust deletion
        if self.selected_course_id is None:
            messagebox.showwarning("Warning", "Please select a course from the list to delete.", parent=self.root)
            return

        confirm = messagebox.askyesno("Confirm Deletion", f"Do you really want to delete the course '{self.var_course.get()}' (ID: {self.selected_course_id})?", parent=self.root)
        if confirm:
            con = sqlite3.connect(database='rms.db')
            cur = con.cursor()
            try:
                # --- Using cid for deletion ---
                cur.execute("DELETE FROM course WHERE cid=?", (self.selected_course_id,))
                con.commit()
                messagebox.showinfo("Deleted", f"Course '{self.var_course.get()}' deleted successfully.", parent=self.root)
                self.show_data()
                self.clear()
                # --- CHANGE 4: Call update_counts on parent RMS ---
                if self.parent_rms: # Only call if parent_rms exists
                    self.parent_rms.update_counts()
            except Exception as ex:
                messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
            finally:
                con.close()

    def clear(self):
        self.var_course.set("")
        self.var_duration.set("")
        self.var_charges.set("")
        self.txt_description.delete("1.0", END)
        self.selected_course_id = None
        self.var_search.set("") # Clear search field as well

    def show_data(self):
        con = sqlite3.connect(database='rms.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM course")
            rows = cur.fetchall()
            self.CourseTable.delete(*self.CourseTable.get_children())
            for row in rows:
                self.CourseTable.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

    def search_course(self):
        if self.var_search.get() == "":
            messagebox.showerror("Error", "Please enter a course name to search.", parent=self.root)
            return

        con = sqlite3.connect(database='rms.db')
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM course WHERE name LIKE ?", ('%' + self.var_search.get() + '%',))
            rows = cur.fetchall()
            self.CourseTable.delete(*self.CourseTable.get_children())
            if rows:
                for row in rows:
                    self.CourseTable.insert('', END, values=row)
            else:
                messagebox.showinfo("Not Found", "No course found matching your search.", parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}", parent=self.root)
        finally:
            con.close()

# --- For standalone testing ---
if __name__ == "__main__":
    root = Tk()
    # When testing standalone, we don't have a parent RMS instance
    # So, pass None for parent_rms.
    obj = CourseClass(root, None) # <--- CHANGE 5: Pass None here for standalone
    root.mainloop()