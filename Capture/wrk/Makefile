run: build
	cd /app && \
	./app

build: clean
	cd build/ && \
	cmake .. && \
	make && \
	make install

clean:
	rm -rf build/*