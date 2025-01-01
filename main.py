#!/usr/bin/env python3
# coding: UTF-8

from fastapi import FastAPI, Request
import string
import random
import uvicorn

import os
import time
import uuid
import hmac
import hashlib
import base64
import requests

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

waiturl_prefix = str(os.environ.get("WAITURL_PRE"))
token = str(os.environ.get("SWITCHBOT_TOKEN"))
secret = str(os.environ.get("SWITCHBOT_SECRET"))


def update_switchbot_webhook_setting(new_url):
    # エポックミリ秒
    t = int(time.time() * 1000)
    # UUIDv4をnonceとして利用
    nonce = str(uuid.uuid4())

    # bash で行っていた sign の生成 (HMAC-SHA256 + base64)
    message = f"{token}{t}{nonce}"
    sign = hmac.new(
        secret.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256
    ).digest()
    sign = base64.b64encode(sign).decode("utf-8")

    # webhook 情報取得リクエスト
    url = "https://api.switch-bot.com/v1.1/webhook/queryWebhook"
    headers = {
        "Authorization": token,
        "sign": sign,
        "t": str(t),
        "nonce": nonce,
        "Content-Type": "application/json; charset=utf8"
    }
    payload = {
        "action": "queryUrl"
    }

    response = requests.post(url, headers=headers, json=payload)
    result = response.json()  # curl -s の結果にあたる
    deleterul = result["body"]["urls"][0] if "body" in result and "urls" in result["body"] else None

    print("deleterul =", deleterul)

    #################################################################################################################設定削除
    # webhook 情報設定リクエスト
    url = "https://api.switch-bot.com/v1.1/webhook/deleteWebhook"
    headers = {
        "Authorization": token,
        "sign": sign,
        "t": str(t),
        "nonce": nonce,
        "Content-Type": "application/json; charset=utf8"
    }
    payload = {
        "action": "deleteWebhook",
        "url": deleterul
    }

    response = requests.post(url, headers=headers, json=payload)
    result = response.json()  # curl -s の結果にあたる
    print(result)



    #################################################################################################################設定追加
    # webhook 情報設定リクエスト
    url = "https://api.switch-bot.com/v1.1/webhook/setupWebhook"
    headers = {
        "Authorization": token,
        "sign": sign,
        "t": str(t),
        "nonce": nonce,
        "Content-Type": "application/json; charset=utf8"
    }
    payload = {
        "action": "setupWebhook",
        "url": new_url,
        "deviceList":"ALL"
    }

    response = requests.post(url, headers=headers, json=payload)
    result = response.json()  # curl -s の結果にあたる
    print(result)

    # webhook 情報取得リクエスト
    url = "https://api.switch-bot.com/v1.1/webhook/queryWebhook"
    headers = {
        "Authorization": token,
        "sign": sign,
        "t": str(t),
        "nonce": nonce,
        "Content-Type": "application/json; charset=utf8"
    }
    payload = {
        "action": "queryUrl"
    }

    response = requests.post(url, headers=headers, json=payload)
    result = response.json()  # curl -s の結果にあたる
    current_url = result["body"]["urls"][0] if "body" in result and "urls" in result["body"] else None

    print("currenturl =", current_url)


def generate_random_path(length: int = 32) -> str:
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

############################################################################################################
random_path = f"/webhook/switchbot/{generate_random_path()}/"
print(random_path)

update_switchbot_webhook_setting(waiturl_prefix+random_path)

@app.post(f"{random_path}")
async def call_switchbot(request: Request):
    #print(request.headers)
    #print(dict(request.headers))
    print(await request.body())
    #print(dict(await request.body()))

    return {}
if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
