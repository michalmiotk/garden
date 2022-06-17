from debian

RUN apt update -y && apt upgrade -y
RUN apt-get install -y motion
COPY requirements.txt requirements.txt
RUN apt install pip -y
RUN pip3 install -r requirements.txt
RUN apt install -y uvicorn
COPY src/start.sh start.sh
RUN chmod a+x start.sh
RUN apt-get install openssl -y



RUN openssl req -x509 -sha256 -nodes -days 365 -newkey rsa:2048 -keyout /etc/motion/motion.key -outform pem -out /etc/motion/motion.crt -subj "/CN=*.com"
ENTRYPOINT ./start.sh
