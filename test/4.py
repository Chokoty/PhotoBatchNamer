import os
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

root = Tk()
root.title("폴더 선택 창")   # 타이틀 설정

file_frame = Frame(root)
file_frame.pack(fill="x", padx = 5, pady= 5)

root.geometry("640x480") # 가로 *세로 사이즈
root.resizable(False, False)    #가로 *세로 사이즈 변경 가능 유무

dir_path = None        #폴더 경로 담을 변수 생성
file_list = []        #파일 목록 담을 변수 생성

def folder_select():

	dir_path = filedialog.askdirectory(initialdir="/",\
					title = "폴더를 선택 해 주세요")
	#folder 변수에 선택 폴더 경로 넣기

	if dir_path == '':
		messagebox.showwarning("경고", "폴더를 선택 하세요")    #폴더 선택 안했을 때 메세지 출력
	else:
		res = os.listdir(dir_path) # 폴더에 있는 파일 리스트 넣기

		print(res)    #folder내 파일 목록 값 출력

		if len(res) == 0:
			messagebox.showwarning("경고", "폴더내 파일이 없습니다.")
		else:
			for file in res:
				print(dir_path + "/" + file) # 파일/폴더 목록 하나씩 출력하기

btn_active_dir = Button(file_frame, text ="폴더 선택", width = 12, padx = 5, pady= 5, command=folder_select)
btn_active_dir.pack( padx = 5, pady= 5)

root.mainloop()