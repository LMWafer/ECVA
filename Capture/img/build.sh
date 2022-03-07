ROOT=..

cp $ROOT/app/main.py    build_context/

docker build -t lmwafer/ecva-capture:1.0 -f ./Dockerfile --no-cache build_context/

rm -rf build_context/*