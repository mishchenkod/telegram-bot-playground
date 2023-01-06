FROM python:3.9
ARG TOKEN
ENV TELEGRAM_TOKEN=${TOKEN}
WORKDIR /usr/src/app/bot
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD python bot.py