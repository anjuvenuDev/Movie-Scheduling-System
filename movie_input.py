import tkinter as tk
from tkinter import messagebox
import mysql.connector as sq

class movie_input(tk.Frame):
    def __init__(self, master, username):
        super().__init__(master)
        self.master = master
        self.username = username
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.master.title("NGA Movie Input Page")

        # Header Label
        header_label = tk.Label(self, text="NGA MOVIE INPUT PAGE", font=("Century Gothic", 24, "bold"), pady=20, fg="black")
        header_label.pack()

        # Labels and entries
        tk.Label(self, text="Movie Type:", font=("Helvetica", 14), fg="black").pack(anchor=tk.CENTER)
        self.movie_type_entry = tk.Entry(self, font=("Helvetica", 14))
        self.movie_type_entry.pack(anchor=tk.CENTER)

        tk.Label(self, text="Movie Name:", font=("Helvetica", 14), fg="black").pack(anchor=tk.CENTER)
        self.movie_name_entry = tk.Entry(self, font=("Helvetica", 14))
        self.movie_name_entry.pack(anchor=tk.CENTER)

        tk.Label(self, text="Cast Info:", font=("Helvetica", 14), fg="black").pack(anchor=tk.CENTER)
        self.cast_info_entry = tk.Entry(self, font=("Helvetica", 14))
        self.cast_info_entry.pack(anchor=tk.CENTER)

        tk.Label(self, text="Cast Weightage (0-1):", font=("Helvetica", 14), fg="black").pack(anchor=tk.CENTER)
        self.cast_weightage_entry = tk.Entry(self, font=("Helvetica", 14))
        self.cast_weightage_entry.pack(anchor=tk.CENTER)

        tk.Label(self, text="Genre:", font=("Helvetica", 14), fg="black").pack(anchor=tk.CENTER)
        self.selected_genre = tk.StringVar()
        genre_buttons_frame = tk.Frame(self)
        genre_buttons_frame.pack(anchor=tk.CENTER)
        for genre in ["Action", "Horror", "Drama", "Thriller", "Comedy", "Documentary", "Romance", "Others"]:
            tk.Radiobutton(genre_buttons_frame, text=genre, variable=self.selected_genre, value=genre.lower(), font=("Helvetica", 14), fg="black").pack(side=tk.LEFT)

        tk.Label(self, text="Demand Score (1-10):", font=("Helvetica", 14), fg="black").pack(anchor=tk.CENTER)
        self.demand_score_entry = tk.Entry(self, font=("Helvetica", 14))
        self.demand_score_entry.pack(anchor=tk.CENTER)

        tk.Label(self, text="Unbooked Seats (0-1600) on Weekday:", font=("Helvetica", 14), fg="black").pack(anchor=tk.CENTER)
        self.unbooked_day_entry = tk.Entry(self, font=("Helvetica", 14))
        self.unbooked_day_entry.pack(anchor=tk.CENTER)

        tk.Label(self, text="Unbooked Seats (0-1600) on Weekend:", font=("Helvetica", 14), fg="black").pack(anchor=tk.CENTER)
        self.unbooked_end_entry = tk.Entry(self, font=("Helvetica", 14))
        self.unbooked_end_entry.pack(anchor=tk.CENTER)

        # Submit Button
        submit_button = tk.Button(self, text="Submit", command=self.submit_movie, font=("Helvetica", 14), bg="#4CAF50", fg="white")
        submit_button.pack(pady=10)
        prev_button = tk.Button(self, text="HOME PAGE", command=self.homepage, font=("Helvetica", 14), bg="#4CAF50", fg="white")
        prev_button.pack(pady=10)

    def homepage(self):
        self.master.show_main_window(self.username)

    def submit_movie(self):
        try:
            q1 = 'select ID from emp_db where UNAME=%s'
            self.master.cur.execute(q1, (self.username,))
            id = self.master.cur.fetchone()
            id = id[0]
            tname = 't' + str(id)
            q = 'insert into {} values (%s, %s, %s, %s, %s, %s, %s, %s)'.format(tname)

            movie_type = self.movie_type_entry.get().lower()
            name = self.movie_name_entry.get()
            cast_info = self.cast_info_entry.get()
            genre = self.selected_genre.get()

            try:
                cast_weightage = float(self.cast_weightage_entry.get())
                if not (0 <= cast_weightage <= 1):
                    raise ValueError("Cast weightage must be between 0 and 1.")
            except ValueError as e:
                messagebox.showerror("Error", f"Invalid cast weightage: {e}")
                return

            if movie_type == 'new':
                demand_score = 10
                unbooked_seats_day = 0
                unbooked_seats_end = 0
            else:
                try:
                    demand_score = float(self.demand_score_entry.get())
                    if not (1 <= demand_score <= 10):
                        raise ValueError("Demand score must be between 1 and 10.")
                except ValueError as e:
                    messagebox.showerror("Error", f"Invalid demand score: {e}")
                    return

                try:
                    unbooked_seats_day = int(self.unbooked_day_entry.get())
                    if not (0 <= unbooked_seats_day <= 1600):
                        raise ValueError("Unbooked seats on weekday must be between 0 and 1600.")
                except ValueError as e:
                    messagebox.showerror("Error", f"Invalid unbooked seats on weekday: {e}")
                    return

                try:
                    unbooked_seats_end = int(self.unbooked_end_entry.get())
                    if not (0 <= unbooked_seats_end <= 1600):
                        raise ValueError("Unbooked seats on weekend must be between 0 and 1600.")
                except ValueError as e:
                    messagebox.showerror("Error", f"Invalid unbooked seats on weekend: {e}")
                    return

            genre_list = ["action", "horror", "drama", "thriller", "comedy", "documentary", "romance", "others"]
            if movie_type not in ['new', 'existing'] or genre.lower() not in genre_list:
                messagebox.showerror("Error", "Invalid movie type or genre.")
                return

            if not all([movie_type, name, cast_info, genre]):
                messagebox.showerror("Error", "Please fill in all the required fields.")
                return

            query = 'select * from {} where name = %s'.format(tname)
            self.master.cur.execute(query, (name,))
            name2 = self.master.cur.fetchone()
            if name2 is not None:
                messagebox.showerror("Error", "Movie already exists")
                self.master.show_main_window(self.username)
                return

            val = (movie_type, name, cast_info, cast_weightage, genre, demand_score, unbooked_seats_day, unbooked_seats_end)
            self.master.cur.execute(q, val)
            self.master.con.commit()
            messagebox.showinfo("Success", "Movie submitted successfully!")
            self.master.show_main_window(self.username)
        except sq.Error as e:
            messagebox.showerror("Database Error", f"Error executing SQL query: {e}")
