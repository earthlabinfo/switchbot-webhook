# switchbot-webhook
for https://github.com/OpenWonderLabs/SwitchBotAPI?tab=readme-ov-file#webhook

This program receives webhook from switchbot cloud system.

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


## sample output

- WAITURL_PRE, HEREISYOURMAC is MASKED by earthlabinfo
- 54.64.81.21 is not my ip. this is a ip of switchbot(maybe on AWS EC2)
 
```
/webhook/switchbot/pFOUvPdXF6AeNvmr4g28t9q2o2SZ0Bzp/
deleterul = http://WAITURL_PRE//webhook/switchbot/K4PKp1caPY55B16vnSXSgRSe3XSsErp6/
{'statusCode': 100, 'body': {}, 'message': 'success'}
{'statusCode': 100, 'body': {}, 'message': 'success'}
currenturl = http://WAITURL_PRE/webhook/switchbot/pFOUvPdXF6AeNvmr4g28t9q2o2SZ0Bzp/
INFO:     Started server process [142]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8080 (Press CTRL+C to quit)
b'{"eventType":"changeReport","eventVersion":"1","context":{"battery":100,"deviceMac":"HEREISYOURMAC","deviceType":"WoMeter","humidity":30,"scale":"CELSIUS","temperature":30,"timeOfSample":1735725788804}}'
INFO:     54.64.81.21:2186 - "POST /webhook/switchbot/pFOUvPdXF6AeNvmr4g28t9q2o2SZ0Bzp/ HTTP/1.1" 200 OK
b'{"eventType":"changeReport","eventVersion":"1","context":{"deviceMac":"HEREISYOURMAC","deviceType":"WoHub2","humidity":34,"lightLevel":1,"scale":"CELSIUS","temperature":25.9,"timeOfSample":1735725957825}}'
INFO:     54.64.81.21:37249 - "POST /webhook/switchbot/pFOUvPdXF6AeNvmr4g28t9q2o2SZ0Bzp/ HTTP/1.1" 200 OK
b'{"eventType":"changeReport","eventVersion":"1","context":{"CO2":887,"battery":100,"deviceMac":"HEREISYOURMAC","deviceType":"MeterPro(CO2)","humidity":33,"scale":"CELSIUS","temperature":24.9,"timeOfSample":1735726069242}}'
INFO:     54.64.81.21:53238 - "POST /webhook/switchbot/pFOUvPdXF6AeNvmr4g28t9q2o2SZ0Bzp/ HTTP/1.1" 200 OK
b'{"eventType":"changeReport","eventVersion":"1","context":{"battery":100,"deviceMac":"HEREISYOURMAC","deviceType":"WoMeter","humidity":73,"scale":"CELSIUS","temperature":9.8,"timeOfSample":1735726098873}}'
INFO:     54.64.81.21:2593 - "POST /webhook/switchbot/pFOUvPdXF6AeNvmr4g28t9q2o2SZ0Bzp/ HTTP/1.1" 200 OK
```
