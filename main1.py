from operator import mod
from tkinter import *
from tkinter import filedialog
import tkinter.ttk as ttk # combobox, progressbar
import time 
# 함수
def btncmd():
    print("!!!")

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

p_var2 = DoubleVar()
def btncmd2():
    for i in range(1, 101):
        time.sleep(0.01)

        p_var2.set(i)
        progressbar.update()
        print(p_var2.get())

#### 메인
root = Tk()

# 화면 설정
width, height = 500, 360 # 창 크기 값 설정
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width / 2) - (width / 2)
y = (screen_height / 2) - (height / 2)

root.geometry(f'{width}x{height}+{int(x)}+{int(y)}') # 창 크기 설정
root.resizable(False, False) # 크기 조정 가능 여부

root.title('폴더 내 사진 이미지 이름 변경 프로그램!') # 창 제목 설정


# 컴포넌트 설정
photo = PhotoImage(file="./img.png")
label1 = Label(root, text="1. 폴더를 선택하세요")
label2 = Label(root, image = photo)
label3 = Label(root, text="2. 이름을 수정하세요")

btn1 = Button(root, text="폴더 선택", command=btncmd)
btn2 = Button(root, text="적용하기", command=btncmd2)

# progressbar = ttk.Progressbar(root, maximum=100, length=150, variable=p_var2, mode="determinate")
progressbar = ttk.Progressbar(root, maximum=100, length=150, variable=p_var2)

file_frame = Frame(root)
btn_active_dir = Button(file_frame, text ="폴더 선택", width = 12, padx = 5, pady= 5, command=folder_select)

# 컴포넌트 배치
label2.pack()

label1.pack()
btn1.pack()

label3.pack()
btn2.pack()

# progressbar.start(10)
progressbar.pack()

file_frame.pack(fill="x", padx = 5, pady= 5)
btn_active_dir.pack( padx = 5, pady= 5)

root.mainloop()

'''
- 폴더를 선택하세요
- 변환하기

- 옛날 순으로 정렬하기
- 폴더이름 + 숫자 형식으로 이름 바꾸기

- 적용하지 않을 파일을 체크해제 하세요 ?
- 파일 형식으로 분류하기 ?

'''