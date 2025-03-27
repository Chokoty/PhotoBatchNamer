from asyncio import events
from tkinter import *

root = Tk()
root.title("사진일괄 자동변경 프로그램 v1.0")
root.geometry("640x640")

listbox = Listbox(root)
listbox.pack()

for i in [1,2,3,4,5]:
    listbox.insert(END, i)

btn1 = Button(root, text="기본버튼")
btn1.pack()

def event_for_listbox(event):
    print("hello")

listbox.bind('<<ListBoxSelect>>', event_for_listbox)


root.mainloop()