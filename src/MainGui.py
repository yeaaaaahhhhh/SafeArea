#!/usr/bin/env python
# coding: utf-8

# In[31]:


from tkinter import *
from tkinter.simpledialog import *
import webbrowser
import kakaoToken
import VideoProcess

camset='../sample.mp4'

def onClick_camset():
    global camset
    camset= askstring("비디오 설정", "원하는 비디오의 경로를 입력해주세요,\n 컴퓨터에 연결된 기본 카메라로 연결하려면 0을 입력해주세요")
    
def callback(url):
    webbrowser.open_new_tab(url)

def onClick_alertset():
    toplevel = Toplevel(root)

    toplevel.title("관리자 카카오톡 연동")

    label1=Label(toplevel,text='1단계: ')
    label1.grid(row=0,column=0)
    
    label2 = Label(toplevel, text='링크를 클릭하여 접속하세요', foreground='blue')
    label2.bind("<Button-1>", lambda e:callback("https://kauth.kakao.com/oauth/authorize?client_id=4d3301cdacb5791322d903a3d6e4827c&redirect_uri=https://example.com/oauth&response_type=code"))
    label2.grid(row=0,column=1)
    label3=Label(toplevel,text='2단계:')
    label3.grid(row=1,column=0)
    label4=Label(toplevel,text='카카오톡 연동 동의 후 연결되는 페이지의 주소를 입력하세요')
    label4.grid(row=1,column=1)
    strvar = StringVar()
    entry = Entry(toplevel,width=30,textvariable = strvar)
    entry.grid(row = 2,column=0,columnspan=2)
    btn_ok=Button(toplevel,text='입력',command=lambda:[btnok(strvar),toplevel.destroy()])
    btn_ok.grid(row=2,column=2)
    
def btnok(strvar):
    #https://example.com/oauth?code=-qWGCAkIVIW46PUxG4T34olSl81zjnehYX-Pf0l01PVJAEnUTlRORlVwaP962ZzpUk9U9wopcJ8AAAGDPz9k2A
    addr=strvar.get()
    pos=addr.find('code=')
    addr=addr[pos+5:]
    if kakaoToken.updateToken(addr):
        messagebox.showinfo('카카오톡 연결 성공','성공적으로 연결되었습니다.')
    else:
        messagebox.showinfo('카카오톡 연결 실패','연결에 실패하였습니다. 카카오톡 연동 동의 후 연결되는 빈 페이지의 주소를 다시 확인해주세요')
    
root = Tk()
root.title("SafeArea")
root.geometry("500x300")

label1=Label(root,text='1.설정')
label1.grid(row=0,column=0)
btn_video=Button(root,text='2.프로그램 시작',command=lambda:[VideoProcess.video_play(camset)])
btn_video.grid(row=2,column=0,pady=15)

btn_camset=Button(root,text="(1) 캠 혹은 비디오 설정",command=onClick_camset)
btn_camset.grid(row=0,column=1)
btn_alertset=Button(root,text="(2) 관리자 카카오톡 알림연동",command=onClick_alertset)
btn_alertset.grid(row=1,column=1)
label_set=Label(root,text='기본 설정 - 비디오: sample video, 카카오톡 알림-없음')
label_set.grid(row=2,column=1)
label_video=Label(root,text='접근을 확인할 구역을 선택하려면 s키를 길게 누른 후\n마우스로 영역 선택 후 space키를 누르세요.\n비디오 창을 끄기 위해 esc키를 눌러주세요.')
label_video.grid(row=3,column=1)

root.mainloop()
    

