import tkinter as tk
from tkinter import messagebox
import mysql.connector as sq
from tkinter import ttk, Canvas, Scrollbar, NS

class rec_movie(tk.Frame):
    def __init__(self, master, username):
        super().__init__(master)
        self.master = master
        self.username=username
        self.pack()
        self.rec_schedule()
    
    def rec_schedule(self):
        self.master.title("NGA Recommended Schedule Page")

        # Header Label
        header_label = tk.Label(self, text="YOUR RECOMMENDED MOVIE SCHEDULE", font=("Century Gothic", 24, "bold"), pady=20, fg="black")
        header_label.pack()

        cur=self.master.cur
        con=self.master.con
        avail_screens=16

        q1 = 'select ID from emp_db where UNAME=%s'
        cur.execute(q1, (self.username,))
        id = cur.fetchone()  # Fetch ID properly
        id=id[0]
        tname = 't' + str(id)
        tinfo = 'tinfo' + str(id)
        trec='trec'+str(id)
        print(tname, tinfo)
        tot_demand=0
        dlist=[]
        q2 = 'select name, unbooked_seats_day, unbooked_seats_end, demand_score, cast_weightage from {} where type=%s'.format(tname)
        cur.execute(q2, ('new', ))
        rows = cur.fetchall()
        print(rows)
        for i in rows:
            booking_rate_day = (1600 - i[1]) / 16
            booking_rate_end = (1600 - i[2]) / 16
            
            if booking_rate_end >= 90:
                avail_screens -= 1
                cur.execute('replace into {}(name, avail_screens) values(%s, %s)'.format(trec), (i[0], avail_screens))
                con.commit()
            elif 75 <= booking_rate_end and 30 < booking_rate_day <= 50:
                avail_screens /= 2
                cur.execute('replace into {}(name, avail_screens) values(%s, %s)'.format(trec), (i[0], avail_screens))
                con.commit()
            elif 50 <= booking_rate_end and booking_rate_day <= 30:
                avail_screens /= 3
                cur.execute('replace into {}(name, avail_screens) values(%s, %s)'.format(trec), (i[0], avail_screens))
                con.commit()
            else:
                avail_screens=1
            
            demand=i[3]*i[4]
            tot_demand+=demand
            dlist.append(demand)
        print(dlist)
        q1='select * from {}'.format(trec)
        cur.execute(q1)
        minfo=cur.fetchall()
        print(minfo)
        j=0
        for i in minfo:
            if tot_demand==0:
                priority=0
            else:
                priority=dlist[j]/tot_demand
            j+=1
            #print(priority)
            allot_screens=priority*i[1]
            print(allot_screens)
            if allot_screens==0:
                q1= 'delete from {} where name=%s'.format(trec)
                cur.execute(q1, (i[0],))
                con.commit()
                print("DELETEDDDD")
            else:
                cur.execute('replace into {}(name, avail_screens) values(%s, %s)'.format(trec), (i[0], allot_screens))
                con.commit()
        
        print("Your personalised weekly schedule")
        hp_time_slot_day=['5:00 am-8:00 am','2:00 pm-5:00 pm','9:00 pm-12:00 pm']
        lp1_time_slot_day=['8:00 am-11:00 am', '11:30 am-1:30 pm', '5:30 pm-8:30 pm']
        lp2_time_slot_day=['8:30 am-11:30 am', '12:00 am-2:00 pm', '2:30 pm-6:30 pm']
        hp_time_slot_end=['5:00 am-8:00 am','9:00 am-12:pm','2:00 pm-5:00 pm','5:30 pm-8:30 pm','9:00 pm-12:00 pm']
        lp_time_slot_end=['4:30 am-7:30 am','8:00 am-11:00 am', '11:30 am-1:30 pm', '5:00 pm-8:00 pm', '8:30 pm-11:30pm']
        q1 = 'select ID from emp_db where UNAME=%s'
        cur.execute(q1, (self.username,))
        id = cur.fetchone()  
        id=id[0]
        tname = 't' + str(id)
        trec = 'trec' + str(id)
        q1='select * from {}'.format(trec)
        cur.execute(q1)
        rows=cur.fetchall()
        mlist=[]
        print(rows)
        for i in rows:
            mlist.append(i[1])
        if mlist==[]:
            max1=0
            max2=0
        else:
            max1=max(mlist)
            mlist.remove(max1)
            if mlist==[]:
                max2=0
            else:
                max2=max(mlist)
        print(max1, max2)
        count=0
        for i in rows:
            if count==2:
                break
            if i[1] in [max1, max2]:
                cur.execute('update {} set avail_screens = %s where name = %s'.format(trec), (i[1]+1, i[0]))
                con.commit()
                count+=1
        cur.execute(q1)
        rows=cur.fetchall()
        for i in rows:
            if i[1]>=12:
                cur.execute('update {} set ts1_wday = %s, ts2_wday = %s, ts3_wday = %s where name = %s'.format(trec), (hp_time_slot_day[0], hp_time_slot_day[1], hp_time_slot_day[2], i[0]))
                con.commit()
                cur.execute('update {} set ts1_wend = %s, ts2_wend = %s, ts3_wend = %s, ts4_wend = %s, ts5_wend = %s where name = %s'.format(trec), (hp_time_slot_end[0], hp_time_slot_end[1], hp_time_slot_end[2], hp_time_slot_end[3], hp_time_slot_end[4], i[0]))
                con.commit()
            elif 6<i[1]<=12:
                cur.execute('update {} set ts1_wday = %s, ts2_wday = %s, ts3_wday = %s where name = %s'.format(trec), (lp1_time_slot_day[0], lp1_time_slot_day[1], lp1_time_slot_day[2], i[0]))
                con.commit()
                cur.execute('update {} set ts1_wend = %s, ts2_wend = %s, ts3_wend = %s, ts4_wend = %s, ts5_wend = %s where name = %s'.format(trec), (lp_time_slot_end[0], lp_time_slot_end[1], lp_time_slot_end[2], lp_time_slot_end[3], lp_time_slot_end[4], i[0]))
                con.commit()
            else:
                cur.execute('update {} set ts1_wday = %s, ts2_wday = %s, ts3_wday = %s where name = %s'.format(trec), (lp2_time_slot_day[0], lp2_time_slot_day[1], lp2_time_slot_day[2], i[0]))
                con.commit()
                cur.execute('update {} set ts1_wend = %s, ts2_wend = %s, ts3_wend = %s, ts4_wend = %s, ts5_wend = %s where name = %s'.format(trec), (lp_time_slot_end[0], lp_time_slot_end[1], lp_time_slot_end[2], lp_time_slot_end[3], lp_time_slot_end[4], i[0]))
                con.commit()
        
        prev_button = tk.Button(self, text="PREV PAGE", command=self.prev, font=("Helvetica", 14), bg="#4CAF50", fg="white")
        prev_button.pack(pady=10)  

        show_button = tk.Button(self, text="SHOW RECOMMENDED SCHEDULE", command=self.create_widgets, font=("Helvetica", 14), bg="#4CAF50", fg="white")
        show_button.pack(pady=10) 

        home_button = tk.Button(self, text="HOME PAGE", command=self.homepage, font=("Helvetica", 14), bg="#4CAF50", fg="white")
        home_button.pack(pady=10) 
        
    def create_widgets(self):
        self.master.title("Recommended Schedule Page")
        tree = ttk.Treeview(self, column=("MOVIE NAME", "MOVIE TYPE", "CAST INFORMATION", "AVAILABLE SCREENS", "WEEKDAY SLOT 1", "WEEKDAY SLOT 2", "WEEKDAY SLOT 3", "WEEKEND SLOT 1", "WEEKEND SLOT 2", "WEEKEND SLOT 3", "WEEKEND SLOT 4", "WEEKEND SLOT 5"), show='headings')
        tree.column("#1", anchor=tk.CENTER)
        tree.heading("#1", text=" MOVIE NAME")
        tree.column("#2", anchor=tk.CENTER)
        tree.heading("#2", text="MOVIE TYPE")
        tree.column("#3", anchor=tk.CENTER)
        tree.heading("#3", text="CAST INFORMATION")
        tree.column("#4", anchor=tk.CENTER)
        tree.heading("#4", text="AVAILABLE SCREENS")
        tree.column("#5", anchor=tk.CENTER)
        tree.heading("#5", text="WEEKDAY SLOT 1")
        tree.column("#6", anchor=tk.CENTER)
        tree.heading("#6", text="WEEKDAY SLOT 2")
        tree.column("#7", anchor=tk.CENTER)
        tree.heading("#7", text="WEEKDAY SLOT 3")
        tree.column("#8", anchor=tk.CENTER)
        tree.heading("#8", text="WEEKEND SLOT 1")
        tree.column("#9", anchor=tk.CENTER)
        tree.heading("#9", text="WEEKEND SLOT 2")
        tree.column("#10", anchor=tk.CENTER)
        tree.heading("#10", text="WEEKEND SLOT 3")
        tree.column("#11", anchor=tk.CENTER)
        tree.heading("#11", text="WEEKEND SLOT 4")
        tree.column("#12", anchor=tk.CENTER)
        tree.heading("#12", text="WEEKEND SLOT 5")

        cur=self.master.cur
        q1 = 'select ID from emp_db where UNAME=%s'
        cur.execute(q1, (self.username,))
        id = cur.fetchone()  
        id=id[0]
        tname = 't' + str(id)
        tinfo = 'trec' + str(id)
        rows1=[]
        cur.execute("select name, avail_screens, ts1_wday, ts2_wday, ts3_wday, ts1_wend, ts2_wend, ts3_wend, ts4_wend, ts5_wend from {}".format(tinfo))    
        rows2 =cur.fetchall()
        for i in rows2:
            cur.execute("SELECT name, type, cast_info FROM {} where name=%s".format(tname), (i[0], ))
            rows1.append(cur.fetchone())
        if rows1==() or rows1==[]:
            messagebox.showerror("Error", "No movie exists")
            self.master.show_main_window(self.username)
            return
        for i in range(len(rows1)):
            rows1[i]+=rows2[i][1:]
        print(rows2)
        for row in rows1:
            print(row) 
            tree.insert('', 'end', text="1", values=row)
        sbar=ttk.Scrollbar(self, orient="horizontal", command=tree.xview)
        tree.configure(xscrollcommand=sbar.set)
        tree.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        sbar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def prev(self):
        self.master.show_movie_schedule(self.username)
    def homepage(self):
        self.master.show_main_window(self.username)