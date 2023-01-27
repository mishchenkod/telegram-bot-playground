build:
	docker compose up --build -d --remove-orphans
deploy:
	docker compose up --build -d --remove-orphans mongo bot
up:
	docker compose up -d
down:
	docker compose down
logs:
	docker compose logs
mongo:
	docker compose up -d mongo mongo-express
	
