# 폴더 내 이미지 이름 일괄변경 프로그램 by chokoty (v1.1)
import os
import time
from tkinter import *
from tkinter import filedialog, messagebox, ttk

root = Tk()
root.title("폴더 내 이미지 이름 일괄변경 프로그램 by chokoty (v1.1)")
root.geometry("700x500")

# 전역 변수
dir_path = None
image_extensions = ['.jpg', '.png', '.gif', '.bmp']
selected_files = []  # 선택된 파일 목록

# 폴더 선택 함수
def folder_select():
    global dir_path
    dir_path = filedialog.askdirectory(initialdir="/", title="폴더를 선택 해 주세요")
    if dir_path == '':
        messagebox.showwarning("경고", "폴더를 선택하세요!")
    else:
        label_dir.config(text=dir_path)
        fill_listbox()

# 리스트박스에 파일 나열 함수
def fill_listbox():
    listbox.delete(0, END)
    selected_files.clear()
    if dir_path:
        files = [f for f in os.listdir(dir_path) if os.path.splitext(f)[1].lower() in image_extensions]
        
        # 정렬 기준 적용
        sort_option = sort_var.get()
        if sort_option == "오래된순":
            files.sort(key=lambda x: os.path.getctime(os.path.join(dir_path, x)))
        elif sort_option == "최신순":
            files.sort(key=lambda x: os.path.getctime(os.path.join(dir_path, x)), reverse=True)
        elif sort_option == "크기순":
            files.sort(key=lambda x: os.path.getsize(os.path.join(dir_path, x)))
        elif sort_option == "이름순":
            files.sort()

        for file in files:
            size = os.path.getsize(os.path.join(dir_path, file)) / 1024  # KB 단위
            ctime = time.strftime("%Y-%m-%d", time.localtime(os.path.getctime(os.path.join(dir_path, file))))
            display_text = f"{file} | {size:.2f} KB | {ctime}"
            listbox.insert(END, display_text)
            selected_files.append(True)  # 기본적으로 모두 선택

# 파일 선택/해제 토글
def toggle_selection(event):
    selected = listbox.curselection()
    for idx in selected:
        selected_files[idx] = not selected_files[idx]
    update_listbox_display()

# 리스트박스 표시 업데이트
def update_listbox_display():
    listbox.delete(0, END)
    for i, file in enumerate([listbox.get(j) for j in range(listbox.size())]):
        prefix = "[✓] " if selected_files[i] else "[ ] "
        listbox.insert(END, prefix + file)

# 이름 변경 함수
def change_names():
    if not dir_path:
        messagebox.showwarning("경고", "폴더를 먼저 선택하세요!")
        return
    
    prefix = entry_prefix.get() if not folder_name_var.get() else os.path.basename(dir_path)
    if not prefix:
        messagebox.showwarning("경고", "이름 접두사를 입력하세요!")
        return
    
    files = [listbox.get(i).split(" | ")[0].replace("[✓] ", "").replace("[ ] ", "") for i in range(listbox.size())]
    total = sum(selected_files)
    if total == 0:
        messagebox.showwarning("경고", "변경할 파일을 선택하세요!")
        return
    
    progress_var.set(0)
    for i, (file, is_selected) in enumerate(zip(files, selected_files)):
        if is_selected:
            old_path = os.path.join(dir_path, file)
            extension = os.path.splitext(file)[1]
            new_name = f"{prefix}_{str(i+1).zfill(3)}{extension}"
            new_path = os.path.join(dir_path, new_name)
            os.rename(old_path, new_path)
            progress_var.set((i+1) / total * 100)
            root.update_idletasks()
    
    messagebox.showinfo("완료", "이름 변경이 완료되었습니다!")
    fill_listbox()

# 체크박스 상태에 따라 입력창 활성/비활성
def toggle_prefix_entry():
    if folder_name_var.get():
        entry_prefix.config(state="disabled")
    else:
        entry_prefix.config(state="normal")

# UI 구성
label_dir = Label(root, text="폴더를 선택하세요")
label_dir.pack(pady=5)

btn_select = Button(root, text="폴더 선택", command=folder_select)
btn_select.pack(pady=5)

# 정렬 옵션
sort_var = StringVar(value="오래된순")
sort_label = Label(root, text="정렬 방식:")
sort_label.pack(pady=5)
sort_menu = ttk.OptionMenu(root, sort_var, "오래된순", "오래된순", "최신순", "크기순", "이름순", command=lambda x: fill_listbox())
sort_menu.pack(pady=5)

# 파일 목록
listbox = Listbox(root, selectmode="multiple", height=15, width=80)
listbox.pack(fill="both", expand=True, padx=10, pady=5)
listbox.bind("<Double-1>", toggle_selection)

# 접두사 입력 및 체크박스
frame_prefix = Frame(root)
frame_prefix.pack(pady=5)
label_prefix = Label(frame_prefix, text="이름 접두사:")
label_prefix.pack(side=LEFT)
entry_prefix = Entry(frame_prefix)
entry_prefix.pack(side=LEFT, padx=5)
folder_name_var = BooleanVar()
chk_folder_name = Checkbutton(frame_prefix, text="폴더 이름 사용", variable=folder_name_var, command=toggle_prefix_entry)
chk_folder_name.pack(side=LEFT)

btn_apply = Button(root, text="적용하기", command=change_names)
btn_apply.pack(pady=5)

progress_var = DoubleVar()
progressbar = ttk.Progressbar(root, maximum=100, variable=progress_var)
progressbar.pack(fill="x", padx=10, pady=5)

root.mainloop()