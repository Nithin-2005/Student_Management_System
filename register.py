# register.py
from tkinter import *
from tkinter import ttk, messagebox
import sqlite3

class RegisterClass:
    def __init__(self, root):
        self.root = root
        self.root.title("Register New Account")
        self.root.geometry("450x350+450+200") # Smaller window for registration
        self.root.resizable(False, False)
        self.root.config(bg="white")
        self.root.focus_force()
        self.root.grab_set() # Make this window modal

        # --- Variables ---
        self.var_email = StringVar()
        self.var_password = StringVar()
        self.var_confirm_password = StringVar()

        # --- Registration Form ---
        register_frame = Frame(self.root, bg="white", bd=2, relief=FLAT)
        register_frame.place(x=20, y=20, width=410, height=300)

        Label(register_frame, text="REGISTER ACCOUNT", font=("Segoe UI", 20, "bold"), bg="white", fg="#03A9F4").pack(pady=15)

        # Email
        Label(register_frame, text="Email Address", font=("Segoe UI", 12), bg="white").place(x=30, y=70)
        Entry(register_frame, textvariable=self.var_email, font=("Segoe UI", 11), bg="lightyellow").place(x=30, y=100, width=350)

        # Password
        Label(register_frame, text="Password", font=("Segoe UI", 12), bg="white").place(x=30, y=140)
        Entry(register_frame, textvariable=self.var_password, font=("Segoe UI", 11), bg="lightyellow", show="*").place(x=30, y=170, width=350)

        # Confirm Password
        Label(register_frame, text="Confirm Password", font=("Segoe UI", 12), bg="white").place(x=30, y=210)
        Entry(register_frame, textvariable=self.var_confirm_password, font=("Segoe UI", 11), bg="lightyellow", show="*").place(x=30, y=240, width=350)

        # Register Button
        btn_register = Button(register_frame, text="Register", font=("Segoe UI", 14, "bold"), bg="#2ecc71", fg="white", cursor="hand2", command=self.register_user)
        btn_register.place(x=30, y=275, width=350, height=35)

    def register_user(self):
        email = self.var_email.get()
        password = self.var_password.get()
        confirm_password = self.var_confirm_password.get()

        if email == "" or password == "" or confirm_password == "":
            messagebox.showerror("Error", "All fields are required!", parent=self.root)
            return

        if password != confirm_password:
            messagebox.showerror("Error", "Password and Confirm Password do not match!", parent=self.root)
            return

        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM user WHERE email=?", (email,))
            row = cur.fetchone()
            if row is not None:
                messagebox.showerror("Error", "This Email Address is already registered. Please use another one.", parent=self.root)
            else:
                cur.execute("INSERT INTO user (email, password) VALUES (?, ?)", (email, password))
                con.commit()
                messagebox.showinfo("Success", "Account Registered Successfully!", parent=self.root)
                self.root.destroy() # Close the registration window
        except Exception as ex:
            messagebox.showerror("Error", f"Error during registration: {str(ex)}", parent=self.root)
        finally:
            con.close()

# For standalone testing of register.py
if __name__ == "__main__":
    root = Tk()
    obj = RegisterClass(root)
    root.mainloop()