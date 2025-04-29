import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

# --- BAZA YARATISH ---
conn = sqlite3.connect("foydalanuvchilar.db")
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        fullname TEXT,
        experience INTEGER,
        salary REAL
    )
''')
conn.commit()


# --- LOGIN OYNASI ---
def show_login():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Login", font=("Arial", 16)).pack(pady=10)
    tk.Label(root, text="Username").pack()
    username_entry = tk.Entry(root)
    username_entry.pack()

    tk.Label(root, text="Password").pack()
    password_entry = tk.Entry(root, show="*")
    password_entry.pack()

    def login():
        username = username_entry.get()
        password = password_entry.get()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        if user:
            messagebox.showinfo("Success", "Login successful!")
            show_calculator(user)
        else:
            messagebox.showerror("Error", "Invalid credentials")

    def register():
        show_register()

    tk.Button(root, text="Login", command=login).pack(pady=5)
    tk.Button(root, text="Register", command=register).pack()


# --- RO‘YXATDAN O‘TISH OYNASI ---
def show_register():
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Register", font=("Arial", 16)).pack(pady=10)
    entries = {}
    for field in ["Full Name", "Username", "Password", "Experience (years)", "Salary"]:
        tk.Label(root, text=field).pack()
        entry = tk.Entry(root, show="*" if field == "Password" else None)
        entry.pack()
        entries[field] = entry

    def register_user():
        try:
            cursor.execute(
                "INSERT INTO users (fullname, username, password, experience, salary) VALUES (?, ?, ?, ?, ?)", (
                    entries["Full Name"].get(),
                    entries["Username"].get(),
                    entries["Password"].get(),
                    int(entries["Experience (years)"].get()),
                    float(entries["Salary"].get())
                ))
            conn.commit()
            messagebox.showinfo("Success", "User registered successfully!")
            show_login()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists")

    tk.Button(root, text="Register", command=register_user).pack(pady=10)
    tk.Button(root, text="Back to Login", command=show_login).pack()


# --- PENSIYA KALKULYATORI ---
def show_calculator(user):
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text=f"Welcome, {user[3]}", font=("Arial", 16)).pack(pady=10)

    tk.Label(root, text=f"Experience: {user[4]} years").pack()
    tk.Label(root, text=f"Salary: ${user[5]}").pack()

    pension = calculate_pension(user[4], user[5])
    tk.Label(root, text=f"Estimated Pension: ${pension:.2f}", font=("Arial", 14), fg="green").pack(pady=10)

    tk.Button(root, text="Logout", command=show_login).pack(pady=5)


def calculate_pension(experience, salary):
    # Oddiy formula: pensiya = tajriba * oylik * 0.01
    return experience * salary * 0.01


# --- DASTURNI BOSHLASH ---
root = tk.Tk()
root.title("Pensiya va Nafaqa Hisoblagich")
root.geometry("300x350")
show_login()
root.mainloop()
