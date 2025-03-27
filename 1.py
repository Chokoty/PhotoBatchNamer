from tkinter import filedialog
from tkinter import *

root = Tk()
root.title("Downloader")
root.geometry("540x300+100+100")
root.resizable(False, False)

def ask():
	root.file = filedialog.askopenfile(
	initialdir='path', 
	title='select file', 
	filetypes=(('png files', '*.png'), 
		('all files', '*.*')))

	txt.configure(text="pwd: " + root.file.name)

lbl = Label(root, text="pwd")
lbl.pack()

txt = Label(root, text=" ")
txt.pack()

btn = Button(root, text="ask",command=ask)
btn.pack()

root.mainloop()

