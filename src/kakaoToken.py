#!/usr/bin/env python
# coding: utf-8

# In[19]:


import requests
import json
def updateToken(ucode):
    url = 'https://kauth.kakao.com/oauth/token'
    client_id = '4d3301cdacb5791322d903a3d6e4827c'
    redirect_uri = 'https://example.com/oauth'
    code = ucode

    data = {
        'grant_type':'authorization_code',
        'client_id':client_id,
        'redirect_uri':redirect_uri,
        'code': code,
        }
    
    response = requests.post(url, data=data)
    tokens = response.json()
    
    #발행된 토큰 저장
    with open("token.json","w") as kakao:
        json.dump(tokens, kakao)

    if tokens.get('error') is None:
        return True
    else:
        return False


# In[14]:


import requests
import json
import datetime
def sendAlert():
    now=datetime.datetime.now()
    with open("token.json","r") as kakao:
        tokens = json.load(kakao)

    url="https://kapi.kakao.com/v2/api/talk/memo/default/send"

    headers={
        "Authorization" : "Bearer " + tokens["access_token"]
    }

    data = {
           'object_type': 'feed',
           "content": {
                "title": "선택 구역에 움직임 감지됨",
                "description": "사건 발생 일시:"+now.strftime('%Y-%m-%d %H:%M:%S'),
                "image_url": "../event.jpeg",
                "image_width": 640,
                "image_height": 640,
                "link": {
                    "web_url": "http://www.daum.net",
                    "mobile_web_url": "http://m.daum.net",
                    "android_execution_params": "contentId=100",
                    "ios_execution_params": "contentId=100"
                }
           }
       }

    data = {'template_object': json.dumps(data)}
    response = requests.post(url, headers=headers, data=data)
    response.status_code

