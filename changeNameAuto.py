import os
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import tkinter.ttk as ttk

print("프로그램 시작")  # 시작 확인

root = Tk()
root.title("폴더 내 이미지 이름 일괄변경 프로그램 v1.0 by chokoty")
root.geometry("500x360")
print("창 생성 완료")  # 창 생성 확인

# 전역 변수
dir_path = None
image_extensions = ['.jpg', '.png', '.gif', '.bmp']

def folder_select():
    global dir_path
    dir_path = filedialog.askdirectory(initialdir="/", title="폴더를 선택 해 주세요")
    print(f"선택된 폴더: {dir_path}")  # 폴더 선택 확인
    if dir_path == '':
        messagebox.showwarning("경고", "폴더를 선택하세요!")
    else:
        label_dir.config(text=dir_path)
        fill_listbox()

# 나머지 함수는 그대로 유지
def fill_listbox():
    listbox.delete(0, END)
    if dir_path:
        files = os.listdir(dir_path)
        for file in files:
            if os.path.splitext(file)[1].lower() in image_extensions:
                listbox.insert(END, file)

def change_names():
    print("이름 변경 시작")  # 함수 호출 확인
    if not dir_path:
        messagebox.showwarning("경고", "폴더를 먼저 선택하세요!")
        return
    prefix = entry_prefix.get()
    if not prefix:
        messagebox.showwarning("경고", "이름 접두사를 입력하세요!")
        return
    files = listbox.get(0, END)
    total = len(files)
    progress_var.set(0)
    for i, file in enumerate(files):
        old_path = os.path.join(dir_path, file)
        extension = os.path.splitext(file)[1]
        new_name = f"{prefix}_{i+1}{extension}"
        new_path = os.path.join(dir_path, new_name)
        os.rename(old_path, new_path)
        progress_var.set((i+1) / total * 100)
        root.update_idletasks()
    messagebox.showinfo("완료", "이름 변경이 완료되었습니다!")
    fill_listbox()

# UI 구성
label_dir = Label(root, text="폴더를 선택하세요")
label_dir.pack(pady=5)

btn_select = Button(root, text="폴더 선택", command=folder_select)
btn_select.pack(pady=5)

listbox = Listbox(root, selectmode="extended", height=10)
listbox.pack(fill="both", expand=True, padx=10, pady=5)

label_prefix = Label(root, text="이름 접두사:")
label_prefix.pack(pady=5)

entry_prefix = Entry(root)
entry_prefix.pack(pady=5)

btn_apply = Button(root, text="적용하기", command=change_names)
btn_apply.pack(pady=5)

progress_var = DoubleVar()
progressbar = ttk.Progressbar(root, maximum=100, variable=progress_var)
progressbar.pack(fill="x", padx=10, pady=5)

print("UI 구성 완료")  # UI 구성 확인
root.mainloop()
print("mainloop 실행")  # mainloop 진입 확인