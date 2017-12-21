import smtplib
import imaplib
import Tkinter, tkFileDialog
from Tkinter import *
import ttk
import email as daftarEmail
import datetime
import tkMessageBox
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import Image, ImageTk

global T
global email
global T1
global passwd
global server
global attach
email = ""
passwd = ""
server = ""
attach = ""
def storeUser():
    global email
    global passwd
    global server
    email = T.get()
    passwd = T1.get()
    haha=''
    print email
    print passwd
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    try:
        haha = server.login(email, passwd)
    except:
        tkMessageBox.showinfo("Error", "Username dan/atau Pass salah.")
        # print 'ERROR'


    if haha!='':
        tkMessageBox.showinfo("Login Success", "Login Berhasil.")
        tab1.destroy()
        inbox()
        return email, server, passwd

def inbox():
    global email
    global passwd
    global server
    M = imaplib.IMAP4_SSL('imap.gmail.com')
    print email + passwd
    M.login(email, passwd)
    rv, data = M.select("INBOX")
    if rv == 'OK':
        print "Processing mailbox...\n"
        process_mailbox(M)  # ... do something with emails, see below ...
        M.close()

def attachment():
    global attach
    attach = tkFileDialog.askopenfilename(parent=tab2, title='Choose a file')
    tkMessageBox.showinfo("Success", "File siap dikirim.")
    return attach
        # print "I got %d bytes from this file." % len(data)

def send():
    global email
    global server
    global subject
    global attach

    pesan = T3.get('1.0',END)
    alamat = T2.get()
    subject = T5.get()
    hihi=0

    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = alamat
    msg['Subject'] = subject

    body = pesan
    msg.attach(MIMEText(body, 'plain'))

    filename = attach
    if filename:
        attachment = open(filename, 'rb')
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= " + filename)
        msg.attach(part)



    text = msg.as_string()

    # message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    # """ % (email, ", ".join(alamat), subject, pesan)
    try:
        server.sendmail(email, alamat, text)

    except:
        tkMessageBox.showinfo("Error", "Email Penerima Salah.")
        hihi=1

    if hihi==0:
        tkMessageBox.showinfo("Success", "Email Terkirim")
        attach=''

    return attach

def process_mailbox(M):
    rv, data = M.search(None, "ALL")
    if rv != 'OK':
        print "No messages found!"
        return
    # full = daftarEmail.message_from_string(data[0][1])
    emailena = len(data[0].split()) - 7
    print emailena
    roww = 0
    for num in range(len(data[0].split()),emailena,-1):

        rv, data = M.fetch(num, '(RFC822)')
        if rv != 'OK':
            print "ERROR getting message", num
            return

        msg = daftarEmail.message_from_string(data[0][1])

        # print msg
        sender = Tkinter.Label(tab3, text='FROM:\t' + msg['From'], font=("arial", 10, "bold"))
        sender.grid(sticky=W)
        date = Tkinter.Label(tab3, text='DATE:\t' + msg['Date'], font=("arial", 6, "bold"))
        date.grid(sticky=W)
        # enter = Tkinter.label
        content = Tkinter.Label(tab3, text='SUBJECT:\t' + msg['Subject'] + '\n', font=("arial", 8, "bold"))
        content.grid(sticky=W)
        # msg.as_string()
        # str(msg)
        # print(str(msg))

        # content2 = Tkinter.Label(tab3, text=str(msg) + '\n', font=("arial", 8, "bold"))
        # content2.grid(sticky=W)


        ttk.Separator(tab3, orient='horizontal').grid(columnspan=2, sticky='ew')
        print 'Message %s: %s' % (num, msg['Subject'])
        print 'Raw Date:', msg['Date']
        date_tuple = daftarEmail.utils.parsedate_tz(msg['Date'])
        roww +=1
        if date_tuple:
            local_date = datetime.datetime.fromtimestamp(
                daftarEmail.utils.mktime_tz(date_tuple))
            print "Local Date:", \
                local_date.strftime("%a, %d %b %Y %H:%M:%S")



master= Tk()
master.title('Email Application')
master.geometry('500x500')
tabControl = ttk.Notebook(master)
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tab4 = ttk.Frame(tabControl)
tabControl.add(tab1, text='Login Email')
tabControl.add(tab2, text='Send Email')
tabControl.add(tab3, text='Inbox Email')
tabControl.add(tab4, text='About')

#TAB 1
loginTitle= Tkinter.Label(tab1,text="\n\n\n\nLOGIN EMAIL",font=("verdana",20,"bold")).pack()
tklabel= Tkinter.Label(tab1,text="\nMasukan Email",font=("arial",14,"bold")).pack()
T = Entry(tab1,width=30)
T.pack()
tklabel1= Tkinter.Label(tab1,text="Masukan Password",font=("arial",14,"bold")).pack()
T1 = Entry(tab1,show='*',width=30)
T1.pack()
kosongan= Tkinter.Label(tab1,text="",font=("arial",14,"bold")).pack()
work = Tkinter.Button(tab1,text = 'Login', bg='#2ecc71',command=storeUser,width=5,height=1).pack()

#TAB 2
loginTitle= Tkinter.Label(tab2,text="\nKirim Email Baru\n",font=("verdana",20,"bold")).pack()
tklabel2= Tkinter.Label(tab2,text="Alamat Email Tujuan",font=("arial",14,"bold")).pack()
T2 = Entry(tab2,width=30)
T2.pack()
tklabel5= Tkinter.Label(tab2,text="Subject",font=("arial",14,"bold")).pack()
T5 = Entry(tab2,width=30)
T5.pack()
kosongan= Tkinter.Label(tab2,text="",font=("arial",5,"bold")).pack()
tklabel3= Tkinter.Label(tab2,text="Masukan Pesan",font=("arial",14,"bold")).pack()
T3 = Text(tab2,width=40,height=10)
T3.pack()
work2 = Tkinter.Button(tab2,text = 'Attachment',bg='#2ecc71', command=attachment,width=5,height=1).pack()
work2 = Tkinter.Button(tab2,text = 'Kirim',bg='#2ecc71', command=send,width=5,height=1).pack()
# kosongan= Tkinter.Label(tab2,text="",font=("arial",14,"bold")).pack()

#TAB ABOUT
loginTitle= Tkinter.Label(tab4,text="\nABOUT\n",font=("verdana",20,"bold")).pack()
img = ImageTk.PhotoImage(Image.open('tc.jpg'))
# panel = Tkinter.Label(tab4, image = img).pack()

tklabel5= Tkinter.Label(tab4,text="Faturrahman M\t\t(05111540000027)",font=("arial",14,"bold")).pack()
tklabel5= Tkinter.Label(tab4,text="Julian Enggarrio PP\t(05111540000082)",font=("arial",14,"bold")).pack()
tklabel5= Tkinter.Label(tab4,text="Ariya Wildan Devanto\t(05111540000123)",font=("arial",14,"bold")).pack()
tklabel5= Tkinter.Label(tab4,text="Arya Wiranata\t\t(05111540000163)",font=("arial",14,"bold")).pack()

tabControl.pack(expand=1, fill="both")
master.mainloop()

formadd = "ariyadevanto@gmail.com"
toaddd  = "wiranata.arya@gmail.com"
message ="Hi i using pyhton"
password = "ariyawildandevanto"

server.quit()

#---------------------------------------------------------------------------------------#
