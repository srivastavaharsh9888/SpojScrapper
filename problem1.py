from Tkinter import *
import ttk
import subprocess
import sqlite3
import tkMessageBox
import urllib
import bs4
conn=sqlite3.connect('problems.sqlite')
c=conn.cursor()
c.execute("create table if not exists prob (SNo INTEGER ,Link varchar(50) primary key)") 
prob=Tk()
trees=ttk.Treeview()

def remove():
    ids=trees.selection()
    if len(ids)==0:
        tkMessageBox.showerror("error","Please select row")
        return 
    for rows in ids:
        c.execute('delete from prob where SNo=(?)',(rows))
        trees.delete(rows)
        conn.commit()
    k=1
    for rows in c.execute('select * from prob').fetchall():
        c.execute('update prob set SNo=(?) where SNo=(?)',(k,rows[0]))
        conn.commit()
        k=k+1
    refresh()   
    #tree(c.execute('select count(*) from prob').fetchone()[0])

def tree(r):
    trees.config(height=r)
    trees.bind('<<TreeviewSelect>>')
    trees["columns"]=("ProblemLink")
    trees.column("ProblemLink",width=220,anchor='center')   
    trees.column("#0",width=50,anchor='center')
    trees.heading("#0",text="S.No")
    trees.heading("ProblemLink",text="Problem Link")
    for rows in c.execute('select * from prob').fetchall():
        if rows[0]%2==0:
            trees.insert('','end',rows[0],text=str(rows[0]),tags=('even'))
        else:           
            trees.insert('','end',rows[0],text=str(rows[0]),tags=('odd'))
        trees.set(rows[0],"ProblemLink",str(rows[1]))
    trees.tag_configure('even',background="#A9A9A9")
    trees.grid(row=0,column=0,columnspan=3,pady=10)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
def add():
    f=c.execute("select count(SNo) from prob").fetchone()[0]
    new=Tk()
    new.title("Add Link")
    new.geometry("%dx%d+%d+%d"%(300,100,(new.winfo_screenwidth()/2)-150,(new.winfo_screenheight()/2)-50))
    Label(new,text="Enter a valid spoj problem link-:\n").pack()    
    v=Entry(new)
    v.pack()    
    def call(code):
        try:    
            c.execute('insert into prob values(?,?)',(f+1,code))
            trees.config(height=f+1)
            if (f+1)%2==0:
                trees.insert('','end',f+1,text=str(f+1),tags=('even'))
            else:
                trees.insert('','end',f+1,text=str(f+1),tags=('odd'))
            trees.set(f+1,"ProblemLink",code)
            conn.commit()
            v.delete(0,'end')
            new.destroy()#nspn2790          
            if f==0:
                refresh()
            tkMessageBox.showinfo("Information","Link Inserted, refresh the page to see it")
        except sqlite3.IntegrityError:
            tkMessageBox.showerror("Error","Sorry this link already exist")
            v.delete(0,'end')
    def check():
        whole=""
        link=v.get()
        if "http://" not in v.get():
                link="http://"+v.get()
        print link
        try:
            source=urllib.urlopen(link,"lxml").read()
        except:
            tkMessageBox.showerror("Error","Sorry no such URL exists or check your internet connection")
            new.destroy()
            return
        code=bs4.BeautifulSoup(source,"lxml")
        leng=len(link)
        problemcode1=link.find('/problems/')
        if link[len(link)-1]=='/':
                        leng=leng-1
        for row in code.find_all('a',class_="btn btn-primary btn-lg"):
            if type(row.get('href'))==type('string'):
                                whole=whole+row.get('href')
        submit=whole.find('/submit/')
        print link[(problemcode1+10):leng]
        if submit==-1:
            tkMessageBox.showerror("error","Such question does not exist")
            v.delete(0,'end')
        else:
            if whole[(submit+8):(problemcode1+10+leng)]==link[(problemcode1+10):leng]: 
                tkMessageBox.showerror("error","Such question does not exist")
            call(link[(problemcode1+10):leng])
    Button(new,text="ADD",font="verdana 25 bold",command=check).pack()
    new.mainloop()

def refresh():
    prob.destroy()
    subprocess.call('python problem1.py')
            
r=c.execute("select count(SNo) from prob")
r=r.fetchone()[0]
if r==0:
    Label(prob,text="There are no problem link in the database please add them",font="('arial',20,'bold')").grid(row=0,column=0,columnspan=3) 
tree(r)
Button(prob,text="ADD",command=lambda:add(),font=("Verdana",12,"bold")).grid(row=1,column=0,padx=10,ipadx=8,pady=15)
Button(prob,text="REMOVE",command=remove,font=("Verdana",12,"bold")).grid(row=1,column=1,)
Button(prob,text="REFRESH",command=refresh,font=("Verdana",12,"bold")).grid(row=1,column=2,padx=10)
conn.commit()
prob.geometry("+%d+%d"%(350,350))
prob.mainloop()
