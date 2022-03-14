ROOT=..

cp $ROOT/app/app                    build_context/
cp $ROOT/app/main.py                build_context/
cp $ROOT/app/RealSense_D435i.yaml   build_context/
cp $ROOT/app/ORBvoc.txt             build_context/

docker build -t lmwafer/ecva-vlsam:1.0 -f ./Dockerfile --no-cache build_context/

rm -rf build_context/*