capture:
	echo "Starting capture..." && \
	cd Capture && \
	make && \
	echo "Capture successful !"

orb:
	echo "Starting pose computation..." && \
	cd ORB && \
	make && \
	echo "Pose computation successful !"