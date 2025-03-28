# 폴더 내 이미지 이름 일괄변경 프로그램 by chokoty .
import os
import time
from tkinter import *
from tkinter import filedialog, messagebox, ttk

root = Tk()
root.title("폴더 내 이미지 이름 일괄변경 프로그램 by chokoty (v1.3)")
root.geometry("800x600")

# 전역 변수
dir_path = None
image_extensions = ['.jpg', '.png', '.gif', '.bmp']

# 폴더 선택 함수
def folder_select():
    global dir_path
    dir_path = filedialog.askdirectory(initialdir="/", title="폴더를 선택 해 주세요")
    if dir_path == '':
        messagebox.showwarning("경고", "폴더를 선택하세요!")
    else:
        label_dir.config(text=dir_path)
        fill_listbox()

# 리스트박스에 파일 나열 함수 (확장자별 그룹화)
def fill_listbox(*args):
    listbox.delete(0, END)
    if dir_path:
        files_by_ext = {}
        for f in os.listdir(dir_path):
            ext = os.path.splitext(f)[1].lower()
            if ext in image_extensions:
                files_by_ext.setdefault(ext, []).append(f)
        
        # 정렬 기준 적용
        sort_option = sort_var.get()
        for ext in files_by_ext:
            if sort_option == "이름순":
                files_by_ext[ext].sort()
            elif sort_option == "크기순":
                files_by_ext[ext].sort(key=lambda x: os.path.getsize(os.path.join(dir_path, x)), reverse=True)
            elif sort_option == "최신순":
                files_by_ext[ext].sort(key=lambda x: os.path.getctime(os.path.join(dir_path, x)), reverse=True)
            elif sort_option == "오래된순":
                files_by_ext[ext].sort(key=lambda x: os.path.getctime(os.path.join(dir_path, x)), reverse=False)

        # 파일 개수 업데이트
        total_files = sum(len(files) for files in files_by_ext.values())
        label_count.config(text=f"전체 파일: {total_files}개")

        # 헤더 추가 (간격 조정 및 왼쪽 여백 추가)
        # listbox.insert(END, "        파일이름                          -> 변경 후 이름                      파일크기          날짜")
        # listbox.insert(END, "        ------------------------------    ------------------------------    ---------------    -------------------------")

        # 확장자별로 표시
        prefix = entry_prefix.get() if not folder_name_var.get() else os.path.basename(dir_path)
        file_idx = 0
        for ext in sorted(files_by_ext.keys()):
            listbox.insert(END, f"        --- {ext.upper()} ---")
            all_files = [(ext, file) for file in files_by_ext[ext]]
            
            # 정렬 기준에 따라 파일 정렬
            if sort_option == "이름순":
                all_files.sort(key=lambda x: x[1])
            elif sort_option == "크기순":
                all_files.sort(key=lambda x: os.path.getsize(os.path.join(dir_path, x[1])), reverse=True)
            elif sort_option == "최신순":
                all_files.sort(key=lambda x: os.path.getctime(os.path.join(dir_path, x[1])), reverse=True)
            elif sort_option == "오래된순":
                all_files.sort(key=lambda x: os.path.getctime(os.path.join(dir_path, x[1])), reverse=False)
            
            for ext, file in all_files:
                size = os.path.getsize(os.path.join(dir_path, file)) / 1024
                ctime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getctime(os.path.join(dir_path, file))))
                new_name = f"{prefix}_{str(file_idx+1).zfill(3)}{ext}" if prefix else file
                # 파일 이름과 변경 후 이름 길이 조정 (최소 30자 보장)
                file_padded = file + " " * (40 - len(file)) if len(file) < 40 else file
                new_name_padded = new_name + " " * (40 - len(new_name)) if len(new_name) < 40 else new_name
                display_text = f"        {file_padded:>40}    -> {new_name_padded:>40}    {size:>.2f} KB    {ctime:>25}"
                listbox.insert(END, display_text)
                file_idx += 1

# 이름 변경 함수
def change_names():
    if not dir_path:
        messagebox.showwarning("경고", "폴더를 먼저 선택하세요!")
        return
    
    prefix = entry_prefix.get() if not folder_name_var.get() else os.path.basename(dir_path)
    if not prefix:
        messagebox.showwarning("경고", "이름 접두사를 입력하세요!")
        return
    
    files = [listbox.get(i).split(" -> ")[0].strip() for i in range(listbox.size()) if i > 1 and not listbox.get(i).startswith("        ---")]
    total = len(files)
    if total == 0:
        messagebox.showwarning("경고", "변경할 파일이 없습니다!")
        return
    
    progress_var.set(0)
    for i, file in enumerate(files):
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
    fill_listbox()

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
listbox = Listbox(root, selectmode="multiple", height=15, width=120)
listbox.pack(fill="both", expand=True, padx=10, pady=5)

# 파일 개수
label_count = Label(root, text="전체 파일: 0개")
label_count.pack(pady=5)

# 접두사 입력 및 체크박스
frame_prefix = Frame(root)
frame_prefix.pack(pady=5)
label_prefix = Label(frame_prefix, text="이름 접두사:")
label_prefix.pack(side=LEFT)
entry_prefix = Entry(frame_prefix)
entry_prefix.pack(side=LEFT, padx=5)
entry_prefix.bind("<KeyRelease>", fill_listbox)  # 접두사 입력 시 즉시 반영
folder_name_var = BooleanVar()
chk_folder_name = Checkbutton(frame_prefix, text="폴더 이름 사용", variable=folder_name_var, command=toggle_prefix_entry)
chk_folder_name.pack(side=LEFT)

btn_apply = Button(root, text="적용하기", command=change_names)
btn_apply.pack(pady=5)

progress_var = DoubleVar()
progressbar = ttk.Progressbar(root, maximum=100, variable=progress_var)
progressbar.pack(fill="x", padx=10, pady=5)

root.mainloop()