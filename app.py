import tkinter as tk
from tkinter import *
import os
import threading
import sys,signal
from PyPDF2 import PdfFileWriter, PdfFileReader
import re
from fpdf import FPDF
import shutil
import glob
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from reportlab.pdfgen import *
from reportlab.lib import *
#Master Key Generator Ceaser cipher


def Master_Key(coursecode,examtype):

    
    final1="".join(chr(ord(i)+5) for i in coursecode)
    final2="".join(chr(ord(i)+5) for i in examtype)
    
    return final1+final2



src="D:\\pythonscriptsprojrct"
des="D:\\pythonscriptsprojrct"
pid=os.getpid()
#Keylogger
from pynput.keyboard import Listener

    #function that logs the records
def write_to_file(key):
    
    letter = str(key)
    letter = letter.replace("'", "")

    if letter=="Key.space":
        letter=" "
    elif letter=="Key.backspace":
        letter=""
    elif bool(re.search('Key.',letter)):
       letter=' '+ letter[4:]

    
 
    with open("log.txt", 'a') as f:
        f.write(letter)
        
    #function that starts the keylogger

def keyLogger():
    
    with Listener(on_press=write_to_file) as l:
           l.join()


#On exam starts
def exam_starts():
    if openFile["state"]=="normal":
        openFile["state"]="disabled"
        logger_thread=threading.Thread(target=keyLogger)
        logger_thread.start()


#On exam ends
def Exam_ends():
    #convert logged text file to protected file
    # ###################################
    # Content
    fileName = 'Studentactivity.pdf'
    documentTitle = 'Studentactivity'
    title = 'Report of '+reg.get()
    textLines = []
    fd=open('log.txt','r')
    f=fd.read()
    fd.close()
    if len(f)>=20:
        for i in range(len(f)//20):
            textLines.append(f[i*20:i*20 + 20])
    else:
        for i in f:
            textLines.append(i)
    textLines.append(f[(len(f)//20)*20:])
    # ###################################
    # 0) Create document 
    from reportlab.pdfgen import canvas 

    pdf = canvas.Canvas(fileName)
    pdf.setTitle(documentTitle)
    # ###################################
    # Register a new font
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.pdfbase import pdfmetrics

    pdfmetrics.registerFont(
        TTFont('abc', 'SakBunderan.ttf')
    )
    pdf.setFont('abc', 36)
    pdf.drawCentredString(300, 770, title)
    # 3) Draw a line
    pdf.line(30, 710, 550, 710)
    # ###################################
    # 4) Text object :: for large amounts of text
    from reportlab.lib import colors

    text = pdf.beginText(40, 680)
    text.setFont("Courier", 18)
    text.setFillColor(colors.red)
    for line in textLines:
        text.textLine(line)
    pdf.drawText(text)

    pdf.save()
    if os.path.exists("log.txt"):
          os.remove("log.txt")
    files=os.listdir(src)
    files2=os.listdir(des)
    os.chdir(src)
    
    pdf_writer=PdfFileWriter()
    pdf=PdfFileReader("Studentactivity.pdf")
    for i in range(pdf.numPages):
        pdf_writer.addPage(pdf.getPage(i))
    passw=Master_Key(Course_code.get().lower(),Exam_type.get().lower())
    pdf_writer.encrypt(passw)
    print(Master_Key(Course_code.get().lower(),Exam_type.get().lower()))
    with open("student_activity.pdf","wb") as f:
        pdf_writer.write(f)
        f.close()
    while os.path.exists("Studentactivity.pdf"):
        os.remove("Studentactivity.pdf")
    os.chdir(des)
    del_files=glob.glob("Studentactivity.pdf")
    for i in del_files:
        os.unlink(i)
    os.chdir(src)
    sender_email=Stud_email.get()
    sender_password=Stud_password.get()
    rec_email=teacher.get()
    subject=reg.get()+"Student activity"

    msg=MIMEMultipart()
    msg['From']=sender_email
    msg['To']=rec_email
    msg['Subject']=subject

    body="This is the activity of student "+reg.get()
    msg.attach(MIMEText(body,'plain'))

    filename="student_activity.pdf"
    attachment=open(filename,'rb')

    part=MIMEBase('application','octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition',"attachment; filename= "+filename)

    msg.attach(part)
    text=msg.as_string()

    server=smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(sender_email,sender_password)
    server.sendmail(sender_email,rec_email,text)
    server.quit()
    os.kill(pid,signal.SIGTERM)
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

Stud_email = Entry(frame,width=20)
Stud_email.place(x=200,y=60)

Stud_email_tag= Label(frame,bg="cyan",text="Email")
Stud_email_tag.place(x=40,y=60)

Stud_password = Entry(frame,width=20,show='*')
Stud_password.place(x=200,y=80)

Stud_password_tag= Label(frame,bg="cyan",text="Password")
Stud_password_tag.place(x=40,y=80)

teacher = Entry(frame,width=20)
teacher.place(x=200,y=100)

teacher_tag= Label(frame,bg="cyan",text="Teachers email")
teacher_tag.place(x=40,y=100)

reg= Entry(frame,width=20)
reg.place(x=200,y=120)

reg_tag= Label(frame,bg="cyan",text="regno")
reg_tag.place(x=40,y=120)
openFile=tk.Button(root, text="Start your exam",padx=10,pady=5,fg="white",bg="#263D42",command=exam_starts)
openFile.pack()

EndExam=tk.Button(root, text="End Exam",padx=10,pady=5,fg="white",bg="#263D42",command=Exam_ends)
EndExam.pack()
root.mainloop()