import tkinter as tk
from tkinter import messagebox
import mysql.connector as sq

class RegisterFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master

        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.master.title("Register Page")
        register_label = tk.Label(self, text="REGISTER PAGE", font=("Helvetica", 16))
        register_label.pack()

        # Create username entry
        username_label = tk.Label(self, text="Username:", font=("Helvetica", 12))
        username_label.pack()
        self.username_entry = tk.Entry(self, font=("Helvetica", 12))
        self.username_entry.pack()

        # Create password entry
        password_label = tk.Label(self, text="Password:", font=("Helvetica", 12))
        password_label.pack()
        self.password_entry = tk.Entry(self, show="*", font=("Helvetica", 12))
        self.password_entry.pack()

        register_button = tk.Button(self, text="Register", command=self.process_register, font=("Helvetica", 12), bg="#008CBA", fg="white", padx=10, pady=5, borderwidth=0)
        register_button.pack()

    def process_register(self):
        username = self.username_entry.get()
        pwd = self.password_entry.get()
        query = 'SELECT * FROM emp_db'
        try:
            self.master.cur.execute(query)
            rows = self.master.cur.fetchall()
            for row in rows:
                if row[1] == username:
                    messagebox.showerror("Error", "Username already exists!")
                    self.master.show_login()
                    return
            id = self.master.cur.rowcount + 1
            val = (id, username, pwd)
            q = 'INSERT INTO emp_db (ID, UNAME, PWD) VALUES (%s, %s, %s)'
            self.master.cur.execute(q, val)
            self.master.con.commit()
            table='t'+str(id)
            q='create table {}(type varchar(30), name varchar(30), cast_info varchar(30), cast_weightage float, genre varchar(30), demand_score float, unbooked_seats_day int, unbooked_seats_end int)'.format(table)
            self.master.cur.execute(q)
            self.master.con.commit()
            table='tinfo'+str(id)
            q='create table {}(name varchar(30) primary key, avail_screens int, ts1_wday varchar(30), ts2_wday varchar(30), ts3_wday varchar(30), ts1_wend varchar(30), ts2_wend varchar(30), ts3_wend varchar(30), ts4_wend varchar(30), ts5_wend varchar(30))'.format(table)
            self.master.cur.execute(q)
            self.master.con.commit()
            table='trec'+str(id)
            q='create table {}(name varchar(30) primary key, avail_screens int, ts1_wday varchar(30), ts2_wday varchar(30), ts3_wday varchar(30), ts1_wend varchar(30), ts2_wend varchar(30), ts3_wend varchar(30), ts4_wend varchar(30), ts5_wend varchar(30))'.format(table)
            self.master.cur.execute(q)
            self.master.con.commit()
            messagebox.showinfo("Success", "Registration was successful!")
            self.master.show_main_window(username)
        except sq.Error as e:
            messagebox.showerror("Database Error", f"Error executing SQL query: {e}")