#!/usr/bin/env python3
# coding: UTF-8

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


import string
import random
import uvicorn

import os
import time
import uuid
import hmac
import hashlib
import base64
import logging
import requests
import sqlite3

DB_NAME = "/data/switchbot-webhook.db"
TABLE_NAME = "records"
logger = logging.getLogger('uvicorn')

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

    #################################################################################################################設定取得
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

    #################################################################################################################設定再取得
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


def init_db():
    """データベースとテーブルの初期化を行う。"""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    # idは自動インクリメントされる
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS records(
            id   INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT
        );
    """)
    conn.commit()
    conn.close()



def insert_data(data_str: str):
    """
    dict形式の文字列(data_str)をデータベースに書き込む。
    書き込み時にidは自動的にインクリメントされる。
    """
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(f"INSERT INTO records(data) VALUES (?)", (data_str,))
    conn.commit()
    conn.close()

def fetch_all_data():
    """書き込まれた全データを取得して返す。"""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute(f"SELECT id, data FROM records")
    rows = cur.fetchall()
    conn.close()
    return rows

def delete_data(mode="all", record_num=None):
    """
    データを削除する。
    mode が "all" の場合、全データを削除。
    mode が "before" の場合、record_num で指定した id 以下のデータを削除。
    """
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    if mode == "all":
        cur.execute(f"DELETE FROM records")
    elif mode == "before" and record_num is not None:
        cur.execute(f"DELETE FROM records WHERE id <= ?", (record_num,))
    else:
        print("削除モードが不正、またはレコード番号が指定されていません。")

    conn.commit()
    conn.close()

def generate_random_path(length: int = 32) -> str:
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


#################################################################################################################API受信用URLランダム生成、webhook呼び出し側設定


init_db()
random_path = f"/webhook/switchbot/{generate_random_path()}/"
print(random_path)

update_switchbot_webhook_setting(waiturl_prefix+random_path)

#################################################################################################################APIコールされた場合の動作
@app.post(f"{random_path}")
async def call_switchbot(json_data: dict):
    logger.info(json_data)
    insert_data(str(json_data))
    return {}

@app.get(f"/view/logs")
async def viewall():
    all_records = fetch_all_data()
    json_compatible_item_data = jsonable_encoder(all_records)
    return JSONResponse(content=all_records)

@app.get(f"/delete/logs")
async def deleteall():
    delete_data(mode="all")
    return JSONResponse(content="done")

if __name__ == "__main__":

    uvicorn.run("main:app", reload=True)
