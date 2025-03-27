from tkinter import * # tkinter 임포트
from tkinter import filedialog


width, height = 330, 360 # 창 크기 값 설정
# - width: 너비
# - height: 높이

root = Tk()
root.geometry('{0}x{1}'.format(width, height)) # 창 크기 설정
root.resizable(False, False) # 크기 조정 가능 여부
root.title('Offline Image File Converter!') # 창 제목 설정

path, image = None, None

# 파일 불러오기
path = filedialog.askopenfilename(filetypes=[('Image File','.jpg'), ('Image File','.png'), ('Image File','.gif'), ('Image File','.bmp')])
path = path.replace('\\', '/')
if path == '': exit()
print(path)

root.mainloop()