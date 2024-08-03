import tkinter as tk
from tkinter import messagebox
import mysql.connector as sq

class movie_delete(tk.Frame):
    def __init__(self, master, username):
        super().__init__(master)
        self.master = master
        self.username=username
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.master.title("NGA Movie Deletion Page")

        # Header Label
        header_label = tk.Label(self, text="NGA MOVIE DELETION PAGE", font=("Century Gothic", 24, "bold"), pady=20, fg="black")
        header_label.pack()

        q1 = 'SELECT ID FROM emp_db WHERE UNAME = %s'
        self.master.cur.execute(q1, (self.username,))
        user_id = self.master.cur.fetchone()
        
        if user_id:
            id = user_id[0]
            tname = f't{id}'
            self.master.cur.execute('SELECT name FROM {}'.format(tname))
            movies = self.master.cur.fetchall()
            
            '''if not movies:
                messagebox.showerror("Error", "No movie exists")
                self.master.show_main_window(self.username)
                return'''
           # else:
            for movie in movies:
                movie_button = tk.Button(self, text=movie[0], command=lambda m=movie[0]: self.delete_movie(m), font=("Helvetica", 14), bg="#4CAF50", fg="white")
                movie_button.pack(pady=10)
            prev_button = tk.Button(self, text="HOME PAGE", command=self.homepage, font=("Helvetica", 14), bg="#4CAF50", fg="white")
            prev_button.pack(pady=10)
            if not movies:
                messagebox.showerror("Error", "No movie exists")
                self.master.show_main_window(self.username)
                return 
        else:
            messagebox.showerror("Error", "User not found")
            self.master.show_main_window(self.username)
    
    def delete_movie(self, movie):
        self.movie=movie
        q1='select ID from emp_db where UNAME=%s'
        self.master.cur.execute(q1, (self.username, ))
        id=self.master.cur.fetchone()
        id=id[0]
        tname='t'+str(id)
        tinfo='tinfo'+str(id)
        trec='trec'+str(id)
        q='delete from {} where name = %s'.format(tname)
        self.master.cur.execute(q, (self.movie, ))
        self.master.con.commit()
        q='delete from {} where name = %s'.format(tinfo)
        self.master.cur.execute(q, (self.movie, ))
        self.master.con.commit()
        q='delete from {} where name = %s'.format(trec)
        self.master.cur.execute(q, (self.movie, ))
        self.master.con.commit()
        messagebox.showinfo(title="Success", message="Movie deleted successfully!")
        self.master.show_main_window(self.username)

    def homepage(self):
        self.master.show_main_window(self.username)