from tkinter import *
import os
import os.path
 
## 함수 선언부
# 왼쪽 폴더박스를 클릭했을때
def clickListBox(event):
    global currentDir, searchDirList
    if (dirListBox.curselection() == ()) :  # 다른 리스트박스를 클릭할 때는 바로 끝낸다.
        return
    dirName = str(dirListBox.get(dirListBox.curselection())) # 클릭한 폴더명
    if dirName=='상위폴더':
        if len(searchDirList)==1 :  # 상위폴더를 클릭했는데 현재 C:\\이면 무시한다.
            return
        searchDirList.pop()         # 상위폴더 이동이라 마지막 검색 폴더(현재 폴더)
    else :
        searchDirList.append(currentDir + dirName + '\\')   # 검색 리스트에 클릭한 폴더 추가한다.
    fillListBox()
 
# 박스에 내용채우기 (왼쪽, 오른쪽 박스 모두)
def fillListBox():
    global currentDir, searchDirList, dirLabel, dirListBox, fileListBox
    dirListBox.delete(0,END)    # 폴더 리스트 박스 지우기
    fileListBox.delete(0,END)   # 파일 리스트 박스 지우기
 
    dirListBox.insert(END,"상위폴더")
    currentDir = searchDirList[len(searchDirList)-1]
    dirLabel.configure(text = currentDir)
    folderList = os.listdir(currentDir)
    for item in folderList:
        if os.path.isdir(currentDir + item):
            dirListBox.insert(END,item)
        elif os.path.isfile(currentDir + item):
            fileListBox.insert(END,item)
 
 
## 전역 변수 선언
window = None
searchDirList = ['C:\\']    # 검색한 폴더 목록의 스택
currentDir = 'C:\\'
dirLabel, dirListBox, fileListBox = None, None, None
 
## 메인 코드
window = Tk()
window.title("폴더 및 파일 목록 보기")
window.geometry('300x500')
 
dirLabel = Label(window,text = currentDir)
dirLabel.pack()
 
dirListBox = Listbox(window)
dirListBox.pack(side=LEFT, fill=BOTH, expand=1)
dirListBox.bind('<<ListboxSelect>>', clickListBox)
 
fileListBox = Listbox(window)
fileListBox.pack(side=RIGHT, fill=BOTH, expand=1)
 
fillListBox() # 초기에는 C:\\폴더 목록 만든다.
 
 
window.mainloop()
