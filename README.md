# Telegram Bot Playground
Telegram bot on Python.

## Environment
Environment variables should be added to the `.env` file:
```
TELEGRAM_TOKEN=
MONGO_URI=mongodb://mongo:mongo@localhost:27017/?authSource=admin
```

## How to run
### MongoDB
Using Makefile:
```
make mongo
``` 
Or manually using Docker (the same as Makefile):
```
docker compose up -d mongo mongo-express
```
Mongo Express will be available on `localhost:8081`.

### Bot
Using local Python installation (3.8+):
```
python bot.py
```
Or using Docker:
```
docker compose up -d bot
```
