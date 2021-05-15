import tkinter as tk
from tkinter import *
def master_key(coursecode,examtype):

    
    final1="".join(chr(ord(i)+5) for i in coursecode)
    final2="".join(chr(ord(i)+5) for i in examtype)
    
    return final1+final2
def Exam_ends():
    
    Master_key = Label(frame,width=20,text=master_key(Course_code.get(),Exam_type.get()))
    Master_key.place(x=200,y=60)
#App
root=tk.Tk()

canvas=tk.Canvas(root,width=700,height=700,bg="#245F13")
canvas.pack()

frame=tk.Frame(root,bg="cyan")
frame.place(relwidth=0.8,relheight=0.8,relx=0.1,rely=0.1)

Course_code = Entry(frame,width=20)
Course_code.place(x=200,y=20)

Course_tag= Label(frame,bg="cyan",text="Course Code")
Course_tag.place(x=40,y=20)

Exam_type = Entry(frame,width=20)
Exam_type.place(x=200,y=40)

Exam_type_tag= Label(frame,bg="cyan",text="Examination")
Exam_type_tag.place(x=40,y=40)





EndExam=tk.Button(root, text="End Exam",padx=10,pady=5,fg="white",bg="#263D42",command=Exam_ends)
EndExam.pack()
root.mainloop()