

# 🎓 Student Management System

A complete multi-window desktop application built using **Python (Tkinter)** and **SQLite** to manage student registrations, course management, and result records with an intuitive graphical user interface.

---

## 📌 Features

- ✅ **User Authentication**
  - User registration with input validation
  - Secure login with password verification

- 🎓 **Student Admission Management**
  - Add, update, delete, and search student records
  - Each student is identified by a unique roll number

- 📘 **Course Management**
  - Add new courses with name, description, and fees
  - Edit, delete, and search courses
  - Prevents duplicate course entries with unique course names

- 📝 **Result Management**
  - Enter student marks
  - Automatically calculates percentage

- 📊 **Dashboard**
  - Display total number of students, courses, and results
  - Real-time updates after every operation

- 🖥️ **Multi-Window GUI**
  - Clean, modular, and intuitive interface
  - Seamless navigation between Login, Dashboard, Courses, Students, and Results windows

---

## 🛠️ Tech Stack

| Component          | Technology              |
|-------------------|--------------------------|
| Language           | Python 3.x               |
| GUI Framework      | Tkinter (built-in)       |
| Database           | SQLite3 (file-based DB)  |
| Platform           | Desktop (cross-platform) |

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Abhiram678/student-management-system.git
cd student-management-system
````

### 2. Run the Application

```bash
python login.py
```

> ✅ Make sure Python 3.x is installed and added to your system PATH.

> 🛡️ Optional: Create and activate a virtual environment before running.

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

---

## 📁 Folder Structure

```
student-management-system/
│
├── main.py                  # Application entry point
├── login.py                 # Login and registration functionality
├── dashboard.py             # Dashboard view after successful login
├── course.py                # Course management module
├── student.py               # Student admission and record module
├── result.py                # Result entry and view module
├── database.db              # SQLite database (auto-generated)
├── assets/                  # Images and icons (optional)
└── README.md                # Project documentation
```

---

## 🔧 Dependencies

Install dependencies using `pip` if additional libraries are used (e.g., Pillow for images):

```bash
pip install pillow
```

## 👨‍💻 Author

**Nithin Talasu**
GitHub: [Nithin2005](https://github.com/Nithin2005)

---




