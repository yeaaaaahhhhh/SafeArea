#!/usr/bin/env python
# coding: utf-8

# In[1]:


from imutils.video import VideoStream
from tkinter.simpledialog import *
import argparse
import imutils
import time
import cv2
import kakaoToken
import json
import os

def video_play(camset):
    # 동영상 열기
    #cap = cv2.VideoCapture('../cctv.mp4')
    if camset == '0':
        cap = cv2.VideoCapture(0)
    else:
        cap=cv2.VideoCapture(camset)

    #알림이 연속해서 전송되지 않도록 타이머를 사용하여 30초 이상 지났을때 전송
    timer=0

    rc=None
    back_img=None


    if not cap.isOpened():
        messagebox.showinfo('Video open failed!','비디오를 찾을 수 없습니다.')
        return;

    # 매 프레임 처리
    while True:
        ret, frame = cap.read()

        if not ret:
            messagebox.showinfo('Frame read failed!','프레임을 더이상 읽어들일 수 없습니다.')
            break;
        if rc is not None:
            cv2.rectangle(frame, rc, (0, 0, 255), 2)


        if back_img is not None:
            x,y,w,h=rc
            #cv2.imshow('back',back_img)
            frame_img=frame[y:y+h,x:x+w]


            frame_img = cv2.cvtColor(frame_img, cv2.COLOR_BGR2GRAY)

            frame_img = cv2.GaussianBlur(frame_img, (0, 0), 1.0)    
            diff = cv2.absdiff(frame_img, back_img)

            _, diff = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
            #cv2.imshow('diff',diff)

            # 흑백으로 된 diff에서 흰색(새로운물체)가 있는지 확인
            cnt, _, stats, _ = cv2.connectedComponentsWithStats(diff)

            for i in range(2, cnt):
                # x, y, width, height, area
                sx, sy, sw, sh, sa = stats[i]

                if sa < 200 or sw< 10 or sh<10:
                    continue
                #print(x+sx, y+sy, sw, sh, sa)
                if time.time()>timer+30:
                    timer=time.time()
                    if os.path.exists('token.json'):
                        with open("token.json","r") as kakao:
                            tokens = json.load(kakao)
                            print(tokens)
                            if tokens.get('error') is None:
                                kakaoToken.sendAlert()
                            else:
                                messagebox.showinfo('카카오톡 연동 실패','카카오톡 재연동이 필요합니다')
                    else:
                        messagebox.showinfo('움직임 감지','선택 구역에 움직임 감지됨')

                cv2.rectangle(frame, (x+sx, y+sy, sw, sh), (0, 255, 0), 2)  
        cv2.imshow('frame', frame)

        if cv2.waitKey(20) == ord(" "):
            cv2.waitKey(100000)
        if cv2.waitKey(20) == 27:
            break

        if cv2.waitKey(3) == ord("s"):
            print('s pressed')

            box = cv2.selectROI("frame", frame, fromCenter=False,showCrosshair=True)


            rc = tuple([int(_) for _ in box])
            x,y,w,h=rc
            back_img=frame[y:y+h,x:x+w]

            back_img = cv2.cvtColor(back_img, cv2.COLOR_BGR2GRAY)


            back_img = cv2.GaussianBlur(back_img, (0, 0), 1.0)    



    cv2.destroyAllWindows()
    return True

