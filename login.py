# login.py
from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3
import os

# Assuming your main RMS dashboard class is in dashboard.py
from dashboard import RMS 
# --- ADD THIS IMPORT ---
from register import RegisterClass # Import the new RegisterClass

class Login_System:
    def __init__(self, root):
        self.root = root
        self.root.title("Login System")
        self.root.geometry("1000x500+200+100")
        self.root.resizable(False, False)
        self.root.config(bg="#f0f0f0")

        # --- Variables ---
        self.var_email = StringVar()
        self.var_password = StringVar()

        # --- Main Background Frames ---
        self.blue_bg_frame = Frame(self.root, bg="#2196F3")
        self.blue_bg_frame.place(x=0, y=0, width=500, height=500)

        self.dark_blue_bg_frame = Frame(self.root, bg="#1976D2")
        self.dark_blue_bg_frame.place(x=500, y=0, width=500, height=500)

        # --- Left Panel: WebCode Clock ---
        self.clock_frame = Frame(self.root, bg="#263238", bd=5, relief=FLAT)
        self.clock_frame.place(x=100, y=70, width=300, height=350)

        Label(self.clock_frame, text="Clock", font=("Segoe UI", 20, "bold"), bg="#263238", fg="white").pack(pady=10)

        try:
            clock_img_path = "images/clock.png"
            if os.path.exists(clock_img_path):
                self.clock_img = Image.open(clock_img_path)
                self.clock_img = self.clock_img.resize((200, 200), Image.Resampling.LANCZOS)
                self.clock_photo = ImageTk.PhotoImage(self.clock_img)
                Label(self.clock_frame, image=self.clock_photo, bg="#263238").pack(pady=20)
            else:
                Label(self.clock_frame, text="[Clock Image Placeholder]", font=("Arial", 12), bg="#263238", fg="gray").pack(pady=20)
                print(f"Warning: '{clock_img_path}' not found for clock display.")
        except Exception as e:
            Label(self.clock_frame, text="[Clock Image Error]", font=("Arial", 12), bg="#263238", fg="red").pack(pady=20)
            print(f"Error loading clock image: {e}")

        # --- Right Panel: Login Form ---
        self.login_frame = Frame(self.root, bg="white", bd=5, relief=FLAT)
        self.login_frame.place(x=450, y=50, width=500, height=400)

        Label(self.login_frame, text="LOGIN HERE", font=("Segoe UI", 25, "bold"), bg="white", fg="#03A9F4").pack(pady=20)

        Label(self.login_frame, text="EMAIL ADDRESS", font=("Segoe UI", 15, "bold"), bg="white", fg="gray").place(x=50, y=100)
        self.txt_email = Entry(self.login_frame, textvariable=self.var_email, font=("Segoe UI", 14), bg="lightyellow")
        self.txt_email.place(x=50, y=140, width=400)

        Label(self.login_frame, text="PASSWORD", font=("Segoe UI", 15, "bold"), bg="white", fg="gray").place(x=50, y=190)
        self.txt_password = Entry(self.login_frame, textvariable=self.var_password, font=("Segoe UI", 14), bg="lightyellow", show="*")
        self.txt_password.place(x=50, y=230, width=400)

        # Register and Forgot Password Links/Buttons
        # --- CHANGE MADE HERE: Command for Register button ---
        btn_register = Button(self.login_frame, text="Register new Account?", font=("Segoe UI", 10), bd=0, bg="white", fg="#03A9F4", cursor="hand2", command=self.register_account)
        btn_register.place(x=50, y=270)

        btn_forgot = Button(self.login_frame, text="Forgot Password?", font=("Segoe UI", 10), bd=0, bg="white", fg="#FFC107", cursor="hand2", command=self.forgot_password)
        btn_forgot.place(x=340, y=270)

        btn_login = Button(self.login_frame, text="Login", font=("Segoe UI", 18, "bold"), bg="#03A9F4", fg="white", cursor="hand2", command=self.login)
        btn_login.place(x=50, y=320, width=400, height=45)

    # --- Methods ---

    def register_account(self):
        # --- CHANGE MADE HERE: Open the RegisterClass window ---
        self.reg_win = Toplevel(self.root)
        self.new_reg_obj = RegisterClass(self.reg_win)
        self.reg_win.focus_set()
        self.reg_win.grab_set() # Make it modal

    def forgot_password(self):
        messagebox.showinfo("Forgot Password", "Open forgot password recovery form/window.", parent=self.root)

    def login(self):
        email = self.var_email.get()
        password = self.var_password.get()

        if email == "" or password == "":
            messagebox.showerror("Error", "All fields are required!", parent=self.root)
            return

        con = sqlite3.connect(database="rms.db")
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM user WHERE email=? AND password=?", (email, password))
            row = cur.fetchone()
            if row is None:
                messagebox.showerror("Error", "Invalid Email or Password!", parent=self.root)
            else:
                messagebox.showinfo("Success", "Login Successful!", parent=self.root)
                self.root.destroy()

                root_rms = Tk()
                obj = RMS(root_rms)
                root_rms.mainloop()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to: {str(ex)}", parent=self.root)
        finally:
            con.close()

if __name__ == "__main__":
    root = Tk()
    obj = Login_System(root)
    root.mainloop()