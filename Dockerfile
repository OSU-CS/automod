FROM python:3.7

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip --version

RUN pip install -r requirements.txt

COPY app.py app.py
COPY emoji_message.py emoji_message.py
COPY new_channel_message.py new_channel_message.py
COPY new_user_message.py new_user_message.py

CMD ["python3", "app.py"]