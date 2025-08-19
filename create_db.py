import sqlite3

def create_db():
    try:
        con = sqlite3.connect('rms.db')
        cur = con.cursor()

        # --- Create Course Table ---
        cur.execute("""
            CREATE TABLE IF NOT EXISTS course (
                cid INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE, -- Added UNIQUE constraint as discussed for CourseClass
                duration TEXT,
                charges TEXT,
                description TEXT
            )
        """)

        # --- Create Student Table ---
        cur.execute("""
            CREATE TABLE IF NOT EXISTS student (
                roll TEXT PRIMARY KEY,
                name TEXT,
                email TEXT,
                gender TEXT,
                dob TEXT,
                contact TEXT,
                admission TEXT,
                course TEXT,
                state TEXT,
                city TEXT,
                pin TEXT,
                address TEXT
            )
        """)

        # --- Create Result Table ---
        cur.execute("""
            CREATE TABLE IF NOT EXISTS result (
                rid INTEGER PRIMARY KEY AUTOINCREMENT,
                roll TEXT,             -- Student Roll No. (Foreign Key to student table)
                name TEXT,             -- Student Name
                course TEXT,           -- Course Name
                marks_ob INTEGER,      -- Marks Obtained
                full_marks INTEGER,    -- Full Marks
                status TEXT,           -- (e.g., "Pass", "Fail")
                FOREIGN KEY(roll) REFERENCES student(roll) ON DELETE CASCADE
            )
        """)

        # --- ADDED CHANGE: Create User Table (for login) ---
        cur.execute("""
            CREATE TABLE IF NOT EXISTS user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE,
                password TEXT
            )
        """)
        
        # Optional: Insert a default admin user if the user table is new and empty
        cur.execute("SELECT COUNT(*) FROM user")
        if cur.fetchone()[0] == 0:
            cur.execute("INSERT INTO user (email, password) VALUES (?, ?)", ('admin@example.com', 'admin123'))
            print("Default admin user 'admin@example.com' with password 'admin123' inserted.")


        con.commit()
        print("Database and tables created successfully.")

    except Exception as ex:
        print(f"Error creating database: {ex}")

    finally:
        if con:
            con.close()

if __name__ == "__main__":
    create_db()