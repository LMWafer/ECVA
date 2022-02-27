up:
	sudo xhost +local:root
	docker-compose -f img/docker-compose.yml up -d
	clear && docker exec -it ECVA-capture bash

down:
	docker-compose -f img/docker-compose.yml down