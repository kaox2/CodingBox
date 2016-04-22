# -*- coding: utf-8 -*-
import os, sys, codecs, platform
from tkinter import *
from io import open
import tkinter.messagebox
import tkinter.filedialog

current_file = None
DIR = os.getcwd() + "/../src/"
os.chdir(DIR)

def isEmptyDir(dir):
    if not os.listdir(dir):
        return True
    else:
        return False

def rClicked(e):
    try:
        def rClicked_Copy(e,apnd=0):
            e.widget.event_generate('<Control-c>')
        def rClicked_Cut(e):
            e.widget.event_generate('<Control-x>')
        def rClicked_Paste(e):
            e.widget.event_generate('<Control-v>')
        def rClicked_Undo(e):
            e.widget.event_generate('<Control-z>')

        e.widget.focus()

        menulist=[
                (' Copy', lambda e=e: rClicked_Copy(e)),
                (' Cut', lambda e=e: rClicked_Cut(e)),
                (' Paste', lambda e=e: rClicked_Paste(e)),
                (' Undo', lambda e=e: rClicked_Undo(e)),
                ]

        rmenu = Menu(None, tearoff=0, takefocus=0)
        for (txt, cmd) in menulist:
            rmenu.add_command(label=txt, command=cmd)
        rmenu.tk_popup(e.x_root+40, e.y_root+10, entry="0")

    except TclError:
        print ('rClicked Error!!')
    return "break"

def mouseWheel(event):
    os = platform.system()
    if os == 'Linux':
        if event.num == 4:
            if (event.x_root > 600) & (items_h > 570):
                canvas.yview_scroll(-1, "units")
        elif event.num == 5:
            if (event.x_root > 600) & (items_h > 570):
                canvas.yview_scroll(1, "units")
    elif os == 'Windows':
        if (event.x_root > 600) & (items_h > 570):
            canvas.yview_scroll((-1)*int((event.delta/120)), "units")

def showFile(_dirname):
    global canvas, items_h
    os.chdir(_dirname)
    for child in subButtonFrame2.winfo_children():
        child.destroy()

    BS = Scrollbar(subButtonFrame2, orient=VERTICAL)
    BS.pack(fill='y', side='right', expand='false')
    canvas = Canvas(subButtonFrame2, relief=SUNKEN, bd=0, bg='Gainsboro')
    canvas.config(yscrollcommand=BS.set, highlightthickness=0, yscrollincrement=50)
    canvas.pack(side='left', fill='both', expand=1)
    BS.config(command=canvas.yview)
    canvas.xview('moveto', 0)
    canvas.yview('moveto', 0)


    innerSubButtonFrame2 = Frame(canvas)
    canvas.create_window(0, 0, window=innerSubButtonFrame2, anchor=NW)

    items_h = 0
    for filename in sorted(os.listdir(".")):
        if os.path.isfile(filename):
            _filename = os.getcwd() + os.sep + filename
            filename = Button(innerSubButtonFrame2, height=1, width=30, anchor=W, text=filename, bg="Honeydew", relief=FLAT, command=lambda widget=_filename: showCode(widget))
            filename.pack(fill='both', expand=1) 
        elif os.path.isdir(filename):
            if isEmptyDir(filename):
                continue
            _filename = os.getcwd() + os.sep + filename
            filename = Button(innerSubButtonFrame2, height=1, width=30, anchor=W, text=filename+'>', bg="AliceBlue", relief=FLAT, command=lambda widget=_filename: showFile(widget))
            filename.pack(fill='both', expand=1) 
        items_h = items_h + 30   #FIXME 
    canvas.config(scrollregion="0 0 200 %d" % items_h)
    os.chdir(DIR)

def showCode(_filename):
    global current_file
    current_file = _filename
    T1.delete('1.0',END)
    """
    (W),UnicodeDecodeError: 'cp950' codec can't decode byte 0xbf 
    in position 2: illegal multibyte sequence, need to force 
    open as utf8 on Chinese Traditional System.
    another saying:
        to filter BOM 
        ==============
        print (data[:3])
            print (codecs.BOM_UTF8)
            if data[:3] == codecs.BOM_UTF8:
            data = data[3:]
    """
    data = open( _filename,'r', encoding='utf8').read()
    T1.insert(INSERT, data)

def saveFile():
    global current_file
    if (current_file):
        if tkinter.messagebox.askokcancel("Save", "Confirm save YES / NO ?"):
            file = open(current_file, 'w', encoding='utf8')
            data = T1.get('1.0', END+'-1c')
            file.write(data)
            current_file = None
            file.close()

def newFile():
    global current_file
    T1.delete('1.0',END)
    file = tkinter.filedialog.asksaveasfile(parent=uno,mode='w+b',title='Select a file')
    if file != None:
        current_file = file.name
        file.close()


def ShowSearch():
    global canvas, items_h
    for child in subButtonFrame2.winfo_children():
        child.destroy()
    BS = Scrollbar(subButtonFrame2, orient=VERTICAL)
    BS.pack(fill='y', side='right', expand='false')
    canvas = Canvas(subButtonFrame2, relief=SUNKEN, bd=0, bg='Gainsboro')
    canvas.config(yscrollcommand=BS.set, highlightthickness=0, yscrollincrement=50)
    canvas.pack(side='left', fill='both', expand=1)
    BS.config(command=canvas.yview)
    canvas.xview('moveto', 0)
    canvas.yview('moveto', 0)
    innerSubButtonFrame2 = Frame(canvas)
    canvas.create_window(0, 0, window=innerSubButtonFrame2, anchor=NW)

    items_h = 0
    for dirPath, dirNames, fileNames in os.walk(DIR):
        for f in fileNames:
            for line in open(os.path.join(dirPath, f), 'r', encoding='utf8'):
                if E1.get() in line:
                    _filename = os.path.join(dirPath, f)
                    f = Button(innerSubButtonFrame2, height=1, width=30, anchor=W, text=f, bg="Honeydew", relief=FLAT, command=lambda widget=_filename: showCode(widget))
                    f.pack(fill='both', expand=1) 
                    items_h = items_h + 30   #FIXME 
                    break;
    canvas.config(scrollregion="0 0 200 %d" % items_h)
    os.chdir(DIR)

# MAIN
uno = Tk()
uno.geometry('800x640+100+100')
uno.configure(background='OldLace')

uno.bind('<MouseWheel>', mouseWheel)
uno.bind('<Button-4>', mouseWheel)
uno.bind('<Button-5>', mouseWheel)

# FRAME1: search bar #XXX, on going
L1 = Label(uno, bg="OldLace", text="Search patten:")
L1.place(x=0, y=0, height=40, width=100)

E1 = Entry(uno, bg="OldLace", bd=5)
E1.place(x=100, y=0, height=40, width=600)
E1.bind('<Return>', (lambda event: ShowSearch()))

B0 = Button(uno, text="Search", bg="OldLace", relief=RAISED, borderwidth=2, command=ShowSearch)
B0.place(x=700, y=0, height=40, width=100)

B1 = Button(uno, text="Save", bg="OldLace", relief=GROOVE, borderwidth=2, command=saveFile)
B1.place(x=0, y=600, height=40, width=100)

B1 = Button(uno, text="New", bg="OldLace", relief=GROOVE, borderwidth=2, command=newFile)
B1.place(x=700, y=600, height=40, width=100)

# FRAME2:  text
T1 = Text(uno, bg="Snow", bd=3, undo=True)
T1.place(x=0, y=40, height=560, width=500)
T1.bind('<Button-3>', rClicked)

TS1 = Scrollbar(uno)
TS1.config(command=T1.yview)
T1.config(yscrollcommand=TS1.set)
TS1.place(x=500, y=40, height=560, width=20)

# FRAME3: button
subButtonFrame1 = Frame(uno, bg='Gainsboro')
subButtonFrame1.place(x=520, y=40, height=560, width=80)

subButtonFrame2 = Frame(uno, bg='Gainsboro')
subButtonFrame2.place(x=600, y=40, height=560, width=200)

for dirname in os.listdir("."):
    if os.path.isdir(dirname):
        dirname = Button(subButtonFrame1, text=dirname, bg="PowderBlue", relief=FLAT, command=lambda widget=dirname: showFile(widget))
        dirname.pack(fill='both') 

uno.mainloop()
