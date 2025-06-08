#!/usr/bin/env python
# -*- coding:utf-8 -*-
import base64
import requests


def register_image(user_id, user_info, file_object, group_id="test"):
    # 1. 获取 access token
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=5WiPHY8QlXyopEHB3S8Subak&client_secret=lkkhzAcqd0TUtFFaLh1I2DTyIpdpaEm2'
    response = requests.get(host)
    access_token = response.json().get("access_token")

    # 2. 图片进行base64编码
    # with open("test.jpeg", mode='rb') as file:
    #     data = base64.b64encode(file.read())
    data = base64.b64encode(file_object.read())

    # 3. 上传图片
    res = requests.post(
        url="https://aip.baidubce.com/rest/2.0/face/v3/faceset/user/add",
        headers={
            "Content-Type": "application/json"
        },
        params={
            "access_token": access_token
        },
        data={
            "image": data,
            "image_type": "BASE64",
            "group_id": group_id,
            "user_id": user_id,
            "user_info": user_info,
        }
    )
    result = res.json()
    return result["result"]['face_token']


def search(file_object):
    # 1. 获取 access token
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=5WiPHY8QlXyopEHB3S8Subak&client_secret=lkkhzAcqd0TUtFFaLh1I2DTyIpdpaEm2'
    response = requests.get(host)
    access_token = response.json().get("access_token")

    # 2. 图片进行base64编码
    data = base64.b64encode(file_object.read())

    # 3. 检验图片
    res = requests.post(
        url="https://aip.baidubce.com/rest/2.0/face/v3/search",
        headers={
            "Content-Type": "application/json"
        },
        params={
            "access_token": access_token
        },
        data={
            "image": data,
            "image_type": "BASE64",
            "group_id_list": "test",
            "match_threshold": 80,  # 人脸匹配的阈值 当人脸识别的score大于80才能通过
            # "liveness_control": "HIGH", # 活体检测详见官方文档https://cloud.baidu.com/doc/FACE/s/ek37c1qiz
        }
    )

    # {"error_code":0,"error_msg":"SUCCESS","log_id":8975998965357,"timestamp":1593273355,"cached":0,"result":{"face_token":"daf9ead990ef00738ab842801e7d212c","user_list":[{"group_id":"test","user_id":"test","user_info":"","score":97.43611907959}]}}
    return res.json()


def delete(user_id, face_token, group_id="test"):
    # https://aip.baidubce.com/rest/2.0/face/v3/faceset/face/delete

    # 1. 获取 access token
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=5WiPHY8QlXyopEHB3S8Subak&client_secret=lkkhzAcqd0TUtFFaLh1I2DTyIpdpaEm2'
    response = requests.get(host)
    access_token = response.json().get("access_token")

    # 2. 检验图片
    res = requests.post(
        url="https://aip.baidubce.com/rest/2.0/face/v3/faceset/face/delete",
        headers={
            "Content-Type": "application/json"
        },
        params={
            "access_token": access_token
        },
        data={
            "user_id": user_id,
            "group_id": group_id,
            "face_token": face_token
        }
    )

    # {"error_code":0,"error_msg":"SUCCESS","log_id":8975998965357,"timestamp":1593273355,"cached":0,"result":{"face_token":"daf9ead990ef00738ab842801e7d212c","user_list":[{"group_id":"test","user_id":"test","user_info":"","score":97.43611907959}]}}


def speed(file_object):
    from aip import AipSpeech   # 语音识别技术依赖包pip install baidu-aip官网sdk文档：https://ai.baidu.com/ai-doc/SPEECH/0lbxfnc9b
    APP_ID = '21212118'
    API_KEY = '5RYoUwOCHcexcWfa2iRC0ftq'
    SECRET_KEY = 'GQQkpl5sOZPdA90kmLPIO4oRenwmhBFG'
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    data = file_object.read()
    # 识别本地文件
    return client.asr(data, 'pcm', 16000, {'dev_pid': 1537})

if __name__ == '__main__':
    # search()
    pass