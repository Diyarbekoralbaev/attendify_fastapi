PHONY: setup start stop restart logs

setup:
	docker-compose up --build -d


start:
	docker-compose up -d



stop:
	docker-compose down


restart:
	docker-compose restart


logs:
	docker-compose logs -f


