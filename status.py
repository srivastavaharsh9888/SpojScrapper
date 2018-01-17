from Tkinter import *
import sqlite3
import ttk
import tkMessageBox
import bs4
import urllib2
import urllib
status=Tk()
conn=sqlite3.connect('problems.sqlite')
cur=conn.cursor()
cur.execute('create table if not exists student(enroll varchar(20) primary key,username varchar(25) UNIQUE)')
#Label(status,text="Status of Students",font="('Verdana',20,'bold')")
names=["Username"]
global treewidth
global prob_link
prob_link=[]
tree = ttk.Treeview(status)
for check in cur.execute('select Link from prob').fetchall():
            prob_link.append(check[0])
def remove():
    ids=tree.selection()
    if len(ids)==0:
        tkMessageBox.showerror("error","Please select user")
    else:
        for row in ids: 
            #print row
            cur.execute('delete from student where enroll=(?)',(row,))
            tree.delete(row)
            conn.commit()

def checking(solved_list,calling,enrol):
    if calling=='start':
        name="http://www.spoj.com/users/"+enrol[1]
        print name
        try:
        	code=urllib.urlopen(name,"lxml")
        except:
        	 tkMessageBox.showerror("Error","Check you internet connection.")
        	 status.destroy()
        	 return 
        source=code.read()
        start=source.find("List of solved classical problems:")
        end=source.find("TODO list of classical problems:")
        solved=source[start:end]
        bs=bs4.BeautifulSoup(solved,"lxml")
        list_of_solved=[]
        for row in bs.find_all('a'):
            if row.text!='':
            	list_of_solved.append(row.text)
            	#print row.text
        for answer in list_of_solved:
            if answer in names:
                tree.set(enrol[0],answer,"yes")
        print list_of_solved
    if calling=='call':
        for answer in solved_list:
            if answer in names:
                tree.set(enrol,answer,"yes")

    
def start():
    global treewidth
    qur=cur.execute('select Link from prob').fetchall()
    print (qur)
    for row in qur:
        names.append(row[0])
    tree.bind("<<TreeviewSelect>>")
    tree.column("#0",width=90,anchor='center')
    tree.heading("#0",text="Enroll_No")
    tree["columns"]=names
    for row in names:
        tree.column(row,width=80,anchor='center')
        tree.heading(row,text=row)
    i=0
    for enroll in cur.execute("select enroll,username from student where username!='' order by enroll").fetchall():
        if i%2==0: 
            tree.insert('','end',enroll[0],text=enroll[0],tags=('even'))
        else:
            tree.insert('','end',enroll[0],text=enroll[0])
        tree.set(enroll[0],"Username",enroll[1])
        checking([],'start',enroll)
        i=i+1
    tree.tag_configure('even',background="#A9A9A9")
    tree.place(x=10,y=0)
    treewidth=(len(names)*80)+100
    vsb = ttk.Scrollbar(status, orient="vertical", command=tree.yview)
    vsb.place(x=treewidth,y=0,height=220)
    tree.configure(yscrollcommand=vsb.set)

    
def adduser():
    new=Tk()
    new.title("Add User")
    new.geometry("%dx%d+%d+%d"%(480,150,(new.winfo_screenwidth()/2)-240,(new.winfo_screenheight()/2)-50))
    Label(new,text="Enter a Enrollment Number of Student\n",font=("Helvetica",10,"bold","italic")).place(x=20,y=20)
    Label(new,text="Enter the username of the student\n",font=("Helvetica",10,"bold","italic")).place(x=20,y=60)
    enroll=Entry(new)
    global username
    global prob_link
    username=""
    enroll.place(x=280,y=20)
    name=Entry(new)
    name.place(x=280,y=60)  
    def call(source):
        try:
            global username
            cur.execute('insert into student values(?,?)',(enroll.get(),name.get()))
            start=source.find("List of solved classical problems:")
            end=source.find("TODO list of classical problems:")
            solved=source[start:end]
            bs=bs4.BeautifulSoup(solved,"lxml")
            list_of_solved=[]
            for row in bs.find_all('a'):
                if row.text!='':
                    list_of_solved.append(row.text)
            #print list_of_solved
            #print len(list_of_solved)
            if (cur.execute("select count(enroll) from student").fetchone()[0])%2==1:
                tree.insert('','end',enroll.get(),text=enroll.get(),tags=('even'))
            else:
                tree.insert('','end',enroll.get(),text=enroll.get())
            tree.set(enroll.get(),"Username",name.get())
            checking(list_of_solved,'call',enroll.get())
            tkMessageBox.showinfo("Information","Username inserted")
            conn.commit()
            new.destroy()
        except sqlite3.IntegrityError:
            tkMessageBox.showerror("Error","Sorry this student already exist")
            name.delete(0,'end')
            enroll.delete(0,'end')

            
    def check():
        global username
        username="http://www.spoj.com/users/"+name.get()
        
   #==============================================================checking for internet connection===================================================================================     
##        def internet_on():
##            for timeout in [1,5,10,15,20,30]:
##                try:
##                    response=urllib2.urlopen('http://www.google.com',timeout=timeout)
##                    return True
##                except urllib2.URLError as err:
##                    return False
##                    new.destroy()
##                    return 
##            return False
            
#        if internet_on()==False:
#            tkMessageBox.showerror("Error","Sorry you are not connected to internet. Connect to internet to use #this software.")
#           new.destroy()
#            return
    #===============================================================================================================================================================================
        try:
            code=urllib.urlopen(username,"lxml")
        except:
            tkMessageBox.showerror("Error","Wrong username inserted")
            name.delete(0,'end')
            return
        
        source=code.read()
        bs=bs4.BeautifulSoup(source,"lxml")
        row=bs.find('h4')
        print username
       # print row.text.find(name.get())
        try:
            #print row.text.find(name.get())
            if row.text.find(name.get())==-1:
                tkMessageBox.showerror("Error","No Such username exists")
                name.delete(0,'end')
                return
            else:
                call(source)
        except:    
            tkMessageBox.showerror("Error","Check you internet connection or you have entered wrong username.")
            name.delete(0,'end')
            return

    Button(new,text="ADD",font=("Verdana", 12 ,"bold","italic"),relief=RAISED,command=check).place(x=200,y=100)
    new.mainloop()

Button(status,text="Add User",relief='groove',font=("Verdana" ,10, "bold"),command=adduser).place(x=100,y=235)
Button(status,text="Remove User",relief='groove',font=("Verdana" ,10, "bold"),command=remove).place(x=250,y=235)
start()
status.geometry('%dx%d+%d+%d'%(treewidth+20,285,200,200))
status.mainloop()



#Filling database with enrollment of first year
'''def database():
    for i in range(1,100):
        enrol='171B'
        if i<=9:
            enrol=enrol+'00'
        if i>=10 and i<=99:
            enrol=enrol+'0'
        enrol=enrol+str(i)
        print i

database()'''
#cur.execute("insert into values("","","")



#http://www.spoj.com/problems/AND/
