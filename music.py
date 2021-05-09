import pygame
import os
from tkinter.filedialog import askdirectory
from tkinter import *
from tkinter import messagebox
import functools
from tkinter import ttk
from mutagen.id3 import ID3
from mutagen.mp3 import MP3
from PIL import Image, ImageTk
import threading
import time



root = Tk()

listofsongs = []
songname = ""
index = 0
v = StringVar()
songlabel =Label(root, textvariable=v, width=50, font='Arial 10 italic', bg='thistle')
songlabel.pack(side=BOTTOM, fill=X)
leftframe = Frame(root, bg='thistle')
leftframe.pack( pady=10, padx=10)
rightframe = Frame(root, bg='thistle')
rightframe.pack()
topframe = Frame(rightframe, bg='thistle')
topframe.pack()
listbox = Listbox(leftframe, bg='antique white', bd=0)
listbox.grid(row=1,column=0)
scrollbar=Scrollbar(leftframe,width=20)
scrollbar.grid(row=1,column=1,)
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)
middleframe = Frame(rightframe, bg='thistle')
middleframe.pack(pady=10, padx=30)


def nextsong():
    global index
    index += 1
    pygame.mixer_music.load(listofsongs[index])
    pygame.mixer.music.play()
    updatelabel()


def prevsong():
    global index
    index -= 1
    pygame.mixer_music.load(listofsongs[index])
    pygame.mixer.music.play()
    updatelabel()


def stopmusic():
    pygame.mixer.music.stop()
    v.set('''Please play me i love singing :(
     ''')


pause =TRUE
def pause_music():
    global pause
    if pause:

        pygame.mixer_music.pause()
        v.set("You paused me,But why?")
        pausebutton.configure(image=playbutt)
        pause = FALSE

    else:

        pygame.mixer_music.unpause()
        v.set(listofsongs[index])
        pausebutton.configure(image=pausebutt)
        pause = TRUE

def play_music():
    global pause
    global index
    selected_song = listbox.curselection()
    res = functools.reduce(lambda sub, ele: sub * 10 + ele, selected_song)
    index = res
    if pause==FALSE:
        pygame.mixer_music.load(listofsongs[index])
        pausebutton.configure(image=pausebutt)
        pause = TRUE

        pygame.mixer_music.play()
        v.set(listofsongs[index])
    else:
        pygame.mixer_music.load(listofsongs[index])
        pygame.mixer_music.play()
        v.set(listofsongs[index])


def updatelabel():
    global index
    global songname
    v.set(listofsongs[index])
    return songname


def choose():
    directory = askdirectory()
    os.chdir(directory)
    for file in os.listdir(directory):
        if file.endswith(".mp3"):
            listofsongs.append(file)
            realdir = os.path.realpath(file)
    pygame.mixer.init()
    pygame.mixer_music.load(listofsongs[0])
    pygame.mixer.music.play()
    updatelabel()


def set_vol(val):
    volume = float(val) / 100  # we do this because the below function takes value only from 0-1.
    pygame.mixer.init()
    pygame.mixer_music.set_volume(volume)


def rewind_music():
    pygame.mixer_music.load(listofsongs[index])
    pygame.mixer_music.play()


root.configure(background="thistle")
root.title("My Music Player")
root.iconbitmap(r'melody.ico')



previousbutt = PhotoImage(file=r'previous.png')
previousbutton = Button(middleframe, text="<| Previous", command=prevsong, image=previousbutt,bg="thistle")
pausebutt = PhotoImage(file=r'pause-button.png')
pausebutton = Button(middleframe, image=pausebutt, command=pause_music, bd=0, bg='thistle')
playbutt = PhotoImage(file=r'play-button.png')
nextbutt = PhotoImage(file=r'next.png')
nextbutton = Button(middleframe, text="|> Next", command=nextsong, image=nextbutt, bg='thistle')
rewindbutton = PhotoImage(file=r'rewind.png')
rewind = Button(middleframe, image=rewindbutton, command=rewind_music, bg='thistle')

bottomframe = Frame(rightframe, bg='thistle')
bottomframe.pack()

select = Button(leftframe, text="SELECT", command=play_music, bg='thistle', bd=0)
select.grid(row=2,column=0)

scale = Scale(bottomframe, orient=HORIZONTAL, comman=set_vol)
scale.set(70)
pygame.mixer.init()
pygame.mixer_music.set_volume(70)
scale.grid(row=1, column=1, pady=15, padx=30)

choose()

listofsongs.reverse()
for items in listofsongs:
    listbox.insert(0, items)
listofsongs.reverse()

previousbutton.grid(row=1, column=0, padx=15)
pausebutton.grid(row=1, column=1, padx=15)
nextbutton.grid(row=1, column=2, padx=15)
rewind.grid(row=1, column=3,padx=15)

def on_closing():
    messagebox.showinfo('CLOSE', "DO YOU SSLY WANNA LEAVE")
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
