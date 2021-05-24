from tkinter import *
import cv2
import face_recognition
import numpy as np
import os
import keyboard
from datetime import datetime
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import shutil

root = Tk()
root.title('Attendance System "AI" using Computer Vision')
root.geometry("626x345")


def main():
    path = "Student'sFaces"
    images = []
    classnames = []
    mylist = os.listdir(path)
    #print(mylist)
    for cl in mylist:
        curImg = cv2.imread(f'{path}/{cl}')
        images.append(curImg)
        classnames.append(os.path.splitext(cl)[0])


    #print(classnames)
    def findEncodings(images):
        encodeList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList

    def markAttendance(name):
        with open('Attendance.csv','r+')as f:
            Datalist = f.readlines()
            namelist = []
            for line in Datalist:
                entry = line.split(',')
                namelist.append(entry[0])
            if name not in namelist:
                now = datetime.now()
                dtstring = now.strftime('%H:%M:%S')
                date = now.date()
                f.writelines(f'\n{name},{dtstring},{date}')
                messagebox.showinfo('Done', 'Your attendance for this session has been recorded! Thank you!')



    encodelistknown = findEncodings(images)
    messagebox.showinfo('Information', "Encoding Completed!\nPress 'Esc' to Stop Capturing")
    #my_canvas.create_text(300,290, text = "Encoding Completed!\nPress Esc to Stop Capturing",font = ("Helvetica", 14), fill = "White")


    cap = cv2.VideoCapture(0)


    while True:
        success, img = cap.read()
        imgS = cv2.resize(img, (0,0),None,0.25,0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        facesCurframe = face_recognition.face_locations(imgS)
        encodeCurframe = face_recognition.face_encodings(imgS, facesCurframe)


        for encodeFace, faceloc in zip(encodeCurframe, facesCurframe):
            matches = face_recognition.compare_faces(encodelistknown,encodeFace)
            facedis = face_recognition.face_distance(encodelistknown, encodeFace)
            #print(facedis)
            matchindex = np.argmin(facedis)


            if matches[matchindex]:
                name = classnames[matchindex].upper()
                #print(name)
                y1,x2,y2,x1 = faceloc
                #print(faceloc)
                y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
                cv2.rectangle(img, (x1,y1),(x2,y2),(0,255,0),2)
                cv2.rectangle(img, (x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_DUPLEX,1,(255,255,255),2)
                markAttendance(name)


        cv2.imshow('Webcam',img)
        cv2.waitKey(1)


        if keyboard.is_pressed('esc'):
            cv2.destroyWindow('Webcam')
            break


def openNewWindow():

    def OpenImage():
        global path
        path = askopenfilename(filetypes = [('image','.jpg')])
        if path == '':
            messagebox.showerror('Error', 'No image selected')
        else:
            messagebox.showinfo('Success Message', 'Image has been added\nPath: '+path)
        #print(path)


    def Hint():
        messagebox.showinfo('Hint', "To add students you must give student's name\n"
                                    "and add image by pressing add image button.\n"
                                    "Remember! No field should be empty!\n"
                                    "You can also view attendance sheet by \n"
                                    "pressing 'Click to View Attendance Sheet'")

    def Save():

        if entry1.get() =='':
            messagebox.showerror("Error", "Name not found!")

        else:
            try:
                Original = path
                target = r"Student'sFaces/" + entry1.get() + ".jpg"
                shutil.copyfile(Original, target)
                messagebox.showinfo("Success Message","Save Successful")
            except:
                messagebox.showerror("Error", "Please add Image. Image not found!")


    def Open_Attendance_File():
        os.startfile('Attendance.csv')

    def remove():
        try:
            Original = r"Student'sFaces/" + entry2.get() + ".jpg"
            Target = r'Recycle bin/deleted '+entry2.get()+ '.jpg'
            shutil.move(Original,Target)
            messagebox.showinfo('Success', 'Remove Successful')
        except:
            messagebox.showerror('Error occured', 'File not found')


    newWindow = Toplevel(root)

    newWindow.title("Settings")

    # sets the geometry of toplevel
    newWindow.geometry("626x345")


    #Canvas
    my_canvas2 = Canvas(newWindow,width = 626, height = 337)
    my_canvas2.pack(fill="both", expand=True)
    my_canvas2.create_image(0, 0, image=Setting_BG, anchor="nw")

    Label_Add = Label(newWindow, text = "Add Students? Remember to Add Students Name!", fg="#40ED49", bg='#1C1C1C')
    Label_Add.config(font=("Courier", 12))
    my_canvas2.create_window(232, 15, window = Label_Add)

    Name_Label = Label(newWindow, text = "Enter Student's Name:", fg="#40ED49", bg='#1C1C1C')
    my_canvas2.create_window(70,40, window = Name_Label)

    entry1 = Entry(newWindow)
    my_canvas2.create_window(210, 40, window=entry1)

    Open_image_btn = Button(newWindow, text='Add image', fg='black', bg='#40ED49', command=OpenImage, borderwidth=0)
    my_canvas2.create_window(320, 40, window=Open_image_btn)

    Save_btn = Button(newWindow, text='Save', fg='black', bg='#40ED49', command=Save, borderwidth=0)
    my_canvas2.create_window(380, 40, window = Save_btn)

    Hint_btn = Button(newWindow, text='Hint', fg='red', bg='#40ED49', command=Hint, borderwidth=0)
    my_canvas2.create_window(422, 40, window = Hint_btn)

    View_Attendance = Label(newWindow, text="View Attendance Sheet?", fg="#40ED49", bg='#1C1C1C')
    my_canvas2.create_window(76, 71, window=View_Attendance)

    Open_Attendace_File_btn = Button(newWindow, text = 'Click to view Attendance Sheet', fg='black', bg='#40ED49', command = Open_Attendance_File, borderwidth = 0)
    my_canvas2.create_window(250,71, window = Open_Attendace_File_btn)

    entry2 = Entry(newWindow)
    my_canvas2.create_window(210, 101, window=entry2)

    Name_Label2 = Label(newWindow, text="Enter Student's Name:", fg="#40ED49", bg='#1C1C1C')
    my_canvas2.create_window(70, 101, window=Name_Label2)

    remove_Std_btn = Button(newWindow, text='Remove Student', fg='red', bg='#40ED49', command=remove, borderwidth=0)
    my_canvas2.create_window(337, 101, window=remove_Std_btn)



bg = PhotoImage(file = "Project BG.png")
Start_Button = PhotoImage(file = "B7.png")
Setting_Button = PhotoImage(file = "Settings Button.png")
Setting_BG = PhotoImage(file = "Setting BG.png")
my_canvas = Canvas(root, width = 626, height = 337)
my_canvas.pack(fill = "both", expand = True)

# Set image
my_canvas.create_image(0,0, image = bg, anchor = "nw")

#Button
Button1 = Button(root, image = Start_Button, command = main, borderwidth=0)
#Button2
Button2 = Button(root, image = Setting_Button, command = openNewWindow, borderwidth = 0)

Button_Window = my_canvas.create_window(500, 270, anchor = "nw", window = Button1)
Button_Window2 = my_canvas.create_window(20, 270, anchor = "nw", window = Button2)
root.mainloop()