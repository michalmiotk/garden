from debian

RUN apt update -y && apt upgrade -y
RUN apt-get install -y motion
COPY requirements.txt requirements.txt
RUN apt install pip -y
RUN pip3 install -r requirements.txt
RUN apt install -y uvicorn
COPY src/start.sh start.sh
RUN chmod a+x start.sh

ENTRYPOINT ./start.sh
