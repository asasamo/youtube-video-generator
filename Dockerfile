FROM ubuntu:latest

WORKDIR /usr/src/app

RUN apt update
RUN apt install -y wget python3 python3-pip

COPY . .

RUN mkdir input out tmp_dir

RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-2/wkhtmltox_0.12.6.1-2.jammy_amd64.deb -o wk.deb

RUN apt install -y ./wk.deb

RUN pip install -r ./requirements.txt

CMD ["python", "bot.py"]