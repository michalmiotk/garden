#!/bin/bash
cd /home/src && motion -m -c camera0.conf 2> camera.log &
chown root:video /dev/video0
cd /home/src && uvicorn main:app  --host 0.0.0.0 --port 8000  