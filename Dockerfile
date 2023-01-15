FROM python:3.9
WORKDIR /usr/src/app/bot
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD python bot.py