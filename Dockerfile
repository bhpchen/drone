FROM ultralytics/yolov5 

#WORKDIR /usr/src/app

ADD . ./

RUN apt-get -y update && apt-get -y upgrade

RUN pip3 install -r requirements.txt

EXPOSE 5000

#CMD ["echo haha"]

#CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]

#CMD ['bash']

ENTRYPOINT ["python3","app.py"]
