import tkinter as tk
from tkinter import messagebox
import mysql.connector as sq
from login_frame import LoginFrame
from register_frame import RegisterFrame
from main_window import MainWindow
from movie_input import movie_input
from movie_update import movie_update
from movie_delete import movie_delete
from movie_display import movie_display
from rec_movie import rec_movie

class MovieSchedulingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Movie Scheduling System")
        self.geometry("800x600")

        # Establish database connection
        try:
            self.con = sq.connect(user='root', password='Adianju@01', host='localhost', database="try")
            self.cur = self.con.cursor()
        except sq.Error as e:
            messagebox.showerror("Database Error", f"Error connecting to the database: {e}")
            self.destroy()

        self.current_frame = None
        self.show_login()

    def show_login(self):
        self.switch_frame(LoginFrame)

    def show_register(self):
        self.switch_frame(RegisterFrame)

    def show_main_window(self, username):
        self.switch_frame(MainWindow, username)

    def show_movie_input(self, username):
        self.switch_frame(movie_input, username)

    def show_movie_schedule(self, username):
        self.switch_frame(movie_display, username)

    def show_rec_movie(self, username):
        self.switch_frame(rec_movie, username)

    def show_movie_update(self, username):
        self.switch_frame(movie_update, username)

    def show_movie_delete(self, username):
        self.switch_frame(movie_delete, username)

    def switch_frame(self, frame_class, *args):
        new_frame = frame_class(self, *args)
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = new_frame
        self.current_frame.pack()

    def close_connection(self):
        self.cur.close()
        self.con.close()

if __name__ == "__main__":
    app = MovieSchedulingApp()
    app.mainloop()

