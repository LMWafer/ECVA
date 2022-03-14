run :
	sudo xhost +local:root
	docker-compose -f img/docker-compose-run.yml up

up:
	sudo xhost +local:root
	docker-compose -f img/docker-compose-dev.yml up -d
	docker exec -it ECVA-vslam bash

down:
	docker-compose -f img/docker-compose-dev.yml down