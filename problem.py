from Tkinter import *
import os,subprocess
root=Tk()

def centre_screen(Tk,w=300,h=300):
	wit=root.winfo_screenwidth()
	hit=root.winfo_screenheight()
	root.geometry('%dx%d+%d+%d' % (w,h,wit/2-w/2,hit/2-h/2))


def problem():
	direc='python ' + os.getcwd()+'/problem1.py'
	subprocess.call(direc,shell=True)
def status():
	direc='python ' + os.getcwd()+'/status.py'
	subprocess.call(direc,shell=True)
Label(root,text="Evaluation",bg="blue",fg="white",font="Verdana 12 bold").pack(fill=X)
Button(root,text="PROBLEM",relief=RAISED,font=("Verdana" ,12, "bold"),command=problem).place(x=35,y=55,height=40)
Button(root,text="STATUS",relief=RAISED,font=("Verdana" ,12, "bold"),command=status).place(x=165,y=55,height=40)
centre_screen(root,300,150)
root.mainloop()









