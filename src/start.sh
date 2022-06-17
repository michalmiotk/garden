#!/bin/bash
cd /home/src && motion -m -c camera0.conf 2> camera.log &
chown root:video /dev/video0
#echo "STEER URL"
#cd /home/src && lt --port 8000 > steer_url.log &
cd /home/src && uvicorn main:app  --host 0.0.0.0 --port 8000 --ssl-keyfile /etc/motion/motion.key --ssl-certfile /etc/motion/motion.crt