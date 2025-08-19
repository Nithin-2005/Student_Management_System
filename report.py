from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk # Keep this if you have any images in this module, otherwise remove
import sqlite3

class ViewResultClass:
    # --- Constructor: Accepts parent_rms from the dashboard ---
    def __init__(self, root, parent_rms=None): # parent_rms is the instance of your RMS class
        self.root = root
        self.parent_rms = parent_rms # Store the reference to the main dashboard
        self.root.title("View Student Results - Result Management System") # More specific title
        self.root.geometry("1350x700+0+0") # Match main window size for consistency, or adjust as needed
        self.root.config(bg="white")
        self.root.focus_force()

        # --- Variables ---
        self.var_search_roll = StringVar()
        self.selected_rid = None # To store the ID of the selected result for deletion

        # === Title ===
        title = Label(self.root, text="View Student Results", font=("goudy old style", 20, "bold"), bg="#0b5377", fg="white")
        title.place(x=0, y=15, relwidth=1, height=50)

        # --- Search Panel ---
        lbl_search_roll = Label(self.root, text="Search By | Roll No.", font=("goudy old style", 15, "bold"), bg="white")
        lbl_search_roll.place(x=400, y=80)
        txt_search_roll = Entry(self.root, textvariable=self.var_search_roll, font=("goudy old style", 15), bg="lightyellow")
        txt_search_roll.place(x=600, y=80, width=200)

        btn_search = Button(self.root, text="Search", font=("goudy old style", 15, "bold"), bg="#0b5377", fg="white", cursor="hand2", command=self.search_result)
        btn_search.place(x=810, y=80, width=100, height=30)
        btn_clear = Button(self.root, text="Clear", font=("goudy old style", 15, "bold"), bg="#607d8b", fg="white", cursor="hand2", command=self.clear_search)
        btn_clear.place(x=920, y=80, width=100, height=30)

        # --- Results Table ---
        self.result_Frame = Frame(self.root, bd=2, relief=RIDGE, bg="white")
        self.result_Frame.place(x=50, y=150, width=1250, height=400)

        scrolly = Scrollbar(self.result_Frame, orient=VERTICAL)
        scrollx = Scrollbar(self.result_Frame, orient=HORIZONTAL)

        self.ResultTable = ttk.Treeview(self.result_Frame, columns=("rid", "roll", "name", "course", "marks_ob", "full_marks", "percentage", "status"), xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)
        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.ResultTable.xview)
        scrolly.config(command=self.ResultTable.yview)

        # Set headings
        self.ResultTable.heading("rid", text="RID") # Hidden column, but useful for deletion
        self.ResultTable.heading("roll", text="Roll No.")
        self.ResultTable.heading("name", text="Name")
        self.ResultTable.heading("course", text="Course")
        self.ResultTable.heading("marks_ob", text="Marks Obtained")
        self.ResultTable.heading("full_marks", text="Total Marks")
        self.ResultTable.heading("percentage", text="Percentage")
        self.ResultTable.heading("status", text="Status") # Add status column from DB

        self.ResultTable["show"] = 'headings' # Only show headings

        # Set column widths
        self.ResultTable.column("rid", width=0, stretch=NO) # Hidden column
        self.ResultTable.column("roll", width=100, anchor=CENTER)
        self.ResultTable.column("name", width=150, anchor=W)
        self.ResultTable.column("course", width=150, anchor=W)
        self.ResultTable.column("marks_ob", width=120, anchor=CENTER)
        self.ResultTable.column("full_marks", width=120, anchor=CENTER)
        self.ResultTable.column("percentage", width=100, anchor=CENTER)
        self.ResultTable.column("status", width=100, anchor=CENTER)

        self.ResultTable.pack(fill=BOTH, expand=1)
        self.ResultTable.bind("<ButtonRelease-1>", self.get_data)

        # --- Delete Button ---
        btn_delete = Button(self.root, text="Delete", font=("goudy old style", 15, "bold"), bg="#f44336", fg="white", cursor="hand2", command=self.delete_result)
        btn_delete.place(x=600, y=570, width=150, height=40)

        # --- Footer ---
        footer = Label(
            self.root,
            text="SRMS:Student Result Management System Contact Us for any Technical Issue: 98xxxxxx01",
            font=("goudy old style", 10, "bold"),
            bg="#0b5377",
            fg="white"
        )
        footer.pack(side=BOTTOM, fill=X, pady=10)


        self.show_results() # Load results on startup

    # --- Methods ---

    def show_results(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT rid, roll, name, course, marks_ob, full_marks, status FROM result")
            rows = cur.fetchall()

            self.ResultTable.delete(*self.ResultTable.get_children())
            if len(rows) > 0:
                for row in rows:
                    marks_ob = row[4]
                    full_marks = row[5]
                    percentage = (marks_ob / full_marks * 100) if full_marks > 0 else 0
                    percentage_str = f"{percentage:.2f}%"

                    self.ResultTable.insert('', END, values=(row[0], row[1], row[2], row[3], row[4], row[5], percentage_str, row[6]))
            else:
                # Removed messagebox.showinfo here to avoid clutter on empty table,
                # the table itself being empty is usually clear enough.
                pass

        except Exception as ex:
            messagebox.showerror("Error", f"Error displaying results: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def search_result(self):
        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            if self.var_search_roll.get() == "":
                messagebox.showerror("Error", "Roll No. is required for search", parent=self.root)
                return

            cur.execute("SELECT rid, roll, name, course, marks_ob, full_marks, status FROM result WHERE roll LIKE '%" + self.var_search_roll.get() + "%'")
            rows = cur.fetchall()

            self.ResultTable.delete(*self.ResultTable.get_children())
            if len(rows) > 0:
                for row in rows:
                    marks_ob = row[4]
                    full_marks = row[5]
                    percentage = (marks_ob / full_marks * 100) if full_marks > 0 else 0
                    percentage_str = f"{percentage:.2f}%"
                    self.ResultTable.insert('', END, values=(row[0], row[1], row[2], row[3], row[4], row[5], percentage_str, row[6]))
            else:
                messagebox.showinfo("Info", "No result found for the given Roll No.", parent=self.root)
                self.show_results() # Show all results if search yields nothing

        except Exception as ex:
            messagebox.showerror("Error", f"Error during search: {str(ex)}", parent=self.root)
        finally:
            con.close()

    def clear_search(self):
        self.var_search_roll.set("")
        self.show_results() # Display all results again
        self.selected_rid = None # Clear selected ID on clear

    def get_data(self, event):
        cursor_row = self.ResultTable.focus()
        content = self.ResultTable.item(cursor_row)
        row = content['values']
        if row:
            self.selected_rid = row[0] # Store the RID of the selected row for deletion

    def delete_result(self):
        if self.selected_rid is None:
            messagebox.showerror("Error", "Please select a result from the table to delete", parent=self.root)
            return

        op = messagebox.askyesno("Confirm Delete", "Do you really want to delete the selected result?", parent=self.root)
        if op:
            con = sqlite3.connect(database="rms.db")
            cur = con.cursor()
            try:
                cur.execute("DELETE FROM result WHERE rid=?", (self.selected_rid,))
                con.commit()
                messagebox.showinfo("Delete", "Result Deleted Successfully", parent=self.root)
                self.clear_search() # Refresh display (clears search and shows all)
                self.selected_rid = None # Reset selected RID
                # --- Call update_counts on parent RMS ---
                if self.parent_rms: # Only call if parent_rms exists
                    self.parent_rms.update_counts()
            except Exception as ex:
                messagebox.showerror("Error", f"Error deleting result: {str(ex)}", parent=self.root)
            finally:
                con.close()

# --- For standalone testing ---
if __name__ == "__main__":
    root = Tk()
    # When testing standalone, we don't have a parent RMS instance
    # So, pass None for parent_rms.
    obj = ViewResultClass(root, None) # Pass None here for standalone
    root.mainloop()