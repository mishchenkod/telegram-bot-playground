build:
	docker compose up --build -d --remove-orphans
up:
	docker compose up -d
down:
	docker compose down
logs:
	docker compose logs
mongo:
	docker compose up -d mongo mongo-express
	
