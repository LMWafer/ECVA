run:
	sudo xhost +local:root
	docker-compose -f img/docker-compose-run.yml up -d

up:
	sudo xhost +local:root
	docker-compose -f img/docker-compose-dev.yml up -d
	clear && docker exec -it ECVA-capture bash

down:
	docker-compose -f img/docker-compose-dev.yml down