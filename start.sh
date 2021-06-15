docker stop drone
docker rm drone
docker build --tag drone-docker .
docker run --gpus all -p 5000:5000 -d -v $(pwd)/detect.py:/usr/src/app/detect.py -v $(pwd)/cut_video.py:/usr/src/app/cut_video.py -v $(pwd)/app.py:/usr/src/app/app.py --name drone drone-docker
#docker run --gpus all --ipc=host --entrypoint "" -it -v $(pwd)/detect.py:/usr/src/app/detect.py -v $(pwd)/cut_video.py:/usr/src/app/cut_video.py -v $(pwd)/app.py:/usr/src/app/app.py --name flask python-docker bash
#docker run --ipc=host --entrypoint "" -it --name flask python-docker bash
#docker run --gpus all -p 5000:5000 --entrypoint "" -it -v $(pwd)/detect.py:/usr/src/app/detect.py -v $(pwd)/cut_video.py:/usr/src/app/cut_video.py -v $(pwd)/app.py:/usr/src/app/app.py --name drone drone-docker bash
