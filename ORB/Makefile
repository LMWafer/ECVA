up:
	sudo xhost +local:root
	docker-compose -f img/docker-compose.yml up -d
	docker exec -it ECVA-vslam bash

down:
	docker-compose -f img/docker-compose.yml down