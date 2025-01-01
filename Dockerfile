FROM almalinux/9-base
RUN dnf update -y
RUN dnf install python3-pip wget procps -y
RUN pip3 install --upgrade pip
RUN pip3 install fastapi
RUN pip3 install "uvicorn[standard]"
RUN pip3 install requests

RUN wget https://raw.githubusercontent.com/earthlabinfo/switchbot-webhook/refs/heads/main/main.py

EXPOSE 8080/tcp
CMD [ "uvicorn", "main:app", "--host=0.0.0.0","--port=8080" ]

ENV WAITURL_PRE="http://FQDN:port"
ENV SWITCHBOT_TOKEN=""
ENV SWITCHBOT_SECRET=""

