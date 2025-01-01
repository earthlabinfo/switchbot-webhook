# switchbot-webhook
for https://github.com/OpenWonderLabs/SwitchBotAPI?tab=readme-ov-file#webhook


## ATTENTION

This program will update(set) your switchbot Webhook config by API.

## how to install

on AlmaLinux 9
```bash
dnf install python3-pip wget
pip3 install --upgrade pip
pip3 install fastapi
pip3 install "uvicorn[standard]"
pip3 install requests

RUN wget https://raw.githubusercontent.com/earthlabinfo/switchbot-webhook/refs/heads/main/main.py
```

## how to run

```bash
export WAITURL_PRE="http://YOURIPorFQDN:PORT"
export SWITCHBOT_TOKEN="YOURTOKENofSwitchbotTOKEN"
export SWITCHBOT_SECRET="YOURTOKENofSwitchbotSECRET"
uvicorn main:app --host=0.0.0.0 --port=8080
```

