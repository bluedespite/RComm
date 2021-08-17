FROM python:slim-buster

RUN pip install --upgrade pip

COPY ./app /app

COPY requirements.txt .
CMD "chmod 666 /dev/ttyacm0"
RUN pip install -r requirements.txt

WORKDIR /app

CMD [ "python","main.py" ]

EXPOSE 80
