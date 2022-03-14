up:
	docker-compose -f img/docker-compose-dev.yml up -d
	clear && docker exec -it ecva-atlas bash

down:
	docker-compose -f img/docker-compose-dev.yml down

mesh-up:
	sudo xhost +local:root
	docker-compose -f img/docker-compose-mesh.yml up -d
	clear && docker exec -it mesh-container bash

mesh-down:
	docker-compose -f img/docker-compose-mesh.yml down