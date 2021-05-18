#imports
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from bs4 import BeautifulSoup as bs
import requests
from requests.sessions import session
import urllib3
from urllib.request import unquote
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)        
import os


url='https://ourvle.mona.uwi.edu/login/index.php?authldap_skipntlmsso=1'
nametype='view.php?id'
nametype1='?'

# Create window object
app=Tk()
app.configure(bg='white')

#username
username_label=Label(app, text='Username', font=('bold',14),bg='white')
username_label.grid(row=0,column=0,sticky=W)

username_text= StringVar()
username_entry=Entry(app, textvariable=username_text)
username_entry.grid(row=0,column=1)

#password 
password_label=Label(app, text='Password', font=('bold',14),bg='white')
password_label.grid(row=0,column=2,sticky=W)

password_text= StringVar()
password_entry=Entry(app, textvariable=password_text)
password_entry.grid(row=0,column=3)

#course url
course_label=Label(app, text='Course Url', font=('bold',14),bg='white')
course_label.grid(row=1,column=0,sticky=W)

course_text= StringVar()
course_entry=Entry(app, textvariable=course_text)
course_entry.grid(row=1,column=1)

#Folder name
folder_label=Label(app, text='Folder Name', font=('bold',14),bg='white')
folder_label.grid(row=1,column=2,sticky=W)

folder_text= StringVar()
folder_entry=Entry(app, textvariable=folder_text)
folder_entry.grid(row=1,column=3,sticky=W)

#textarea
# text_list=Listbox(app,height=8,width=50,borderwidth=0, highlightthickness=0)
text_list=Listbox(app,height=8,width=70)
text_list.grid(row=3,column=0,columnspan=3,rowspan=10,pady=10,padx=10)


#file directory button
def directory_button():
    # Allow user to select a directory and store it in global var
    # called folder_path
    global folder_path
    filename = filedialog.askdirectory()
    folder_path.set(filename)
    print(filename)

folder_path = StringVar()
button2 = Button(text="Choose Folder Directory",highlightthickness=0, cursor="hand2", command=directory_button, bg='white',activebackground='grey')
button2.grid(row=2, column=1)

#clear all button
def clear_text():
    username_entry.delete(0,END)
    password_entry.delete(0,END)
    course_entry.delete(0,END)
    folder_entry.delete(0,END)
    text_list.delete(0,END)
    
clear_btn = Button(text="Clear Inputs",highlightthickness=0, command=clear_text,cursor="hand2", bg='white',activebackground='grey')
clear_btn.grid(row=2, column=2,pady=20)


#course content download func
def courses(course_url,folder,f_path,u_name,u_pass):
    
    session_variable =requests.session()

    payload={
        'username':u_name,
        'password':u_pass
    }
    response=session_variable.post(url,data=payload,verify=False) 

    directory = f_path+'/'+folder
    local=directory+'/'
    lst=[]
    parselink=bs(session_variable.get(course_url).text , 'html.parser')
    for check in parselink.find_all('li', attrs={'class','modtype_resource'}):
        lst.append(check)
    
    if not os.path.exists(directory):
        if len(lst)>0:
            os.makedirs(directory)
            for data2 in parselink.find_all('li', attrs={'class','modtype_resource'}):
                for data in data2.find_all('a'):
                    links=data.get('href')  
                    contenturl=(session_variable.get(links,stream=True,verify=False))
                    pdffiles=unquote(contenturl.url)
                    filenames=pdffiles.rsplit('/', 1)[1]
                    if nametype1 in filenames:
                        filenames=filenames.rsplit('?', 1)[0]
                    if not nametype in pdffiles:
                        print(filenames)
                        with open(local+filenames,'wb') as f:
                            f.write(contenturl.content)
        else:
            print('Error in Input Field')
    else:
        print("Folder Already Exists")

#download button
def download_content():
    if username_entry.get() != '' and course_entry.get() != '' and folder_entry.get() != '' and folder_path.get() != '' and password_entry.get() !='':
        username='Username        '+username_entry.get()
        course_e='Course Url        '+course_entry.get()
        folder_e='Folder Name    '+folder_entry.get()
        file_path='File Path           '+ folder_path.get()+'/'+folder_entry.get()
        text_list.insert(1,username) 
        text_list.insert(2,course_e)
        text_list.insert(3,folder_e)
        text_list.insert(4,file_path)
        text_list.insert(5,'Downloading Content....')
        try:
            messagebox.showinfo("Message", "Trying to retrive content. Please wait!")   
            courses(course_entry.get(),folder_entry.get(),folder_path.get(),username_entry.get(),password_entry.get())
            clear_text()
            text_list.insert(0,'Download Successful!') 
        except:
            messagebox.showinfo("Message", "Unfortunately the program ran into an error.Please try again!")   
            text_list.insert(0,'Program ran into an Error')
    else:
        text_list.insert(6,'Please Fill Out All Fields')
    
d_btn = Button(text="Download Content",highlightthickness=0, command=download_content,cursor="hand2", bg='white',activebackground='grey')
d_btn.grid(row=2, column=3,pady=20)




app.title('Notes Downloader')
app.geometry('800x350')

#Start program
app.mainloop()
