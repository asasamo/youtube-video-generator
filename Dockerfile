FROM ubuntu:latest

WORKDIR /usr/src/app

RUN apt update
RUN apt install -y wget python3 python3-pip ffmpeg

COPY . .

RUN mkdir input out tmp_dir

RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-2/wkhtmltox_0.12.6.1-2.jammy_amd64.deb -nv

RUN apt install -y ./wkhtmltox_0.12.6.1-2.jammy_amd64.deb

RUN pip install -r ./requirements.txt
RUN pip install python-telegram-bot -U --pre

CMD ["python3", "bot.py"]