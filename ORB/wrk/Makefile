all: clean build run

clean:
	rm -rf build/*
	rm /app/app

build:
	cd build && \
	cmake .. && \
	make && \
	make install

run: 
	cd /app && \
	./app