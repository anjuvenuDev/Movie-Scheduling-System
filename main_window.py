import tkinter as tk
from tkinter import messagebox
import mysql.connector as sq

class MainWindow(tk.Frame):
    def __init__(self, master, username):
        super().__init__(master)
        self.master = master
        self.username = username
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.master.title("NGA Movie Scheduling System")
        self.canvas = tk.Canvas(self, width=6000, height=4000)
        self.canvas.pack()

        # Load background image
        #self.bg_image = tk.PhotoImage(file="movie-screen.png")
        #self.canvas.create_image(0,0,anchor="center", image=self.bg_image)
        bg_image = tk.PhotoImage(file="untitled.png")
        bg_label = tk.Label(self.canvas, image=bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Use place() to cover the entire window
        bg_label.image = bg_image  # Keep a reference to avoid garbage collection

        # Title label at the center of the canvas
        title_label = tk.Label(self.canvas, text="WELCOME TO NGA MOVIE SCHEDULING SYSTEM, {}!".format(self.username.upper()), font=("Century Gothic", 20, "bold"), fg="#CDBE70", bg="#800000")            
        self.canvas.create_window(660, 50, anchor="center", window=title_label)

        button_style = {"font": ("Helvetica", 14), "width": 15, "pady": 10, "bg": "#4CAF50", "fg": "white"}

        input_button = tk.Button(self.canvas, text="Add Movie", command=lambda: self.master.show_movie_input(self.username), **button_style)
        self.canvas.create_window(650, 200, anchor="center", window=input_button)

        update_button = tk.Button(self.canvas, text="Update Movie", command=lambda: self.master.show_movie_update(self.username), **button_style)
        self.canvas.create_window(650, 300, anchor="center", window=update_button)

        delete_button = tk.Button(self.canvas, text="Delete Movie", command=lambda: self.master.show_movie_delete(self.username), **button_style)
        self.canvas.create_window(650, 400, anchor="center", window=delete_button)

        disp_schedule_button = tk.Button(self.canvas, command=lambda: self.master.show_movie_schedule(self.username), text="Display Schedule", **button_style)
        self.canvas.create_window(650, 500, anchor="center", window=disp_schedule_button)

        logout_button = tk.Button(self.canvas, text="Logout", command=self.logout, **button_style)
        self.canvas.create_window(650, 600, anchor="center", window=logout_button)

    def logout(self):
        self.master.show_login()