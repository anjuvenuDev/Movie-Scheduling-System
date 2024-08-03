import tkinter as tk
from tkinter import messagebox
import mysql.connector as sq

class LoginFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.master.title("Login System")
        self.canvas = tk.Canvas(self, width=6000, height=4000)
        self.canvas.pack()

        bg_image = tk.PhotoImage(file="movie-screen.png")
        bg_label = tk.Label(self.canvas, image=bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        bg_label.image = bg_image

        title_label = tk.Label(self.canvas, text="MOVIE SCHEDULING SYSTEM - SIGN IN PAGE", font=("Century Gothic bold", 18))
        self.canvas.create_window(660, 50, anchor="center", window=title_label)

        username_label = tk.Label(self.canvas, text="Username:", bg="white", font=("Helvetica", 15))
        self.canvas.create_window(525, 200, anchor="center", window=username_label)
        self.username_entry = tk.Entry(self.canvas, font=("Helvetica", 12), bg="#EEE8CD")
        self.canvas.create_window(725, 200, anchor="center", window=self.username_entry)

        password_label = tk.Label(self.canvas, text="Password:", bg="white", font=("Helvetica", 15))
        self.canvas.create_window(525, 250, anchor="center", window=password_label)
        self.password_entry = tk.Entry(self.canvas, show="*", font=("Helvetica", 12), bg="#EEE8CD")
        self.canvas.create_window(725, 250, anchor="center", window=self.password_entry)

        login_button = tk.Button(self.canvas, text="Login", command=self.process_login, font=("Helvetica", 15), bg="#4CAF50", fg="white", padx=10, pady=5, borderwidth=0)
        self.canvas.create_window(540, 500, anchor="nw", window=login_button)

        register_button = tk.Button(self.canvas, text="Register", command=self.master.show_register, font=("Helvetica", 15), bg="#008CBA", fg="white", padx=10, pady=5, borderwidth=0)
        self.canvas.create_window(670, 500, anchor="nw", window=register_button)

    def process_login(self):
        username = self.username_entry.get()
        pwd = self.password_entry.get()
        query = 'SELECT * FROM emp_db'
        try:
            self.master.cur.execute(query)
            rows = self.master.cur.fetchall()
            for row in rows:
                if row[1] == username and row[2] == pwd:
                    messagebox.showinfo("Success", "Login was successful!")
                    self.master.show_main_window(username)
                    return
            messagebox.showerror("Error", "Invalid credentials!")
        except sq.Error as e:
            messagebox.showerror("Database Error", f"Error executing SQL query: {e}")
