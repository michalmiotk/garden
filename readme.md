# run
if You first time run this repo:
```
sudo ufw allow 8000
```
Remember to plugin Camera, then run :
```
sudo docker pull 32233223/garden:latest
sudo docker run -p 8000:8000 --device=/dev/video0 --device=/dev/ttyUSB0 -v $(pwd -- "$0")/src:/home/src -it 32233223/garden:latest
```
then go to https://0.0.0.0:8000

if you want internet:
```
sudo apt install -y npm
sudo npm install -g localtunnel
```
and then in separate console for steering : 
```
lt --port 8000
```
docs on http://127.0.0.1:8000/docs
# run in dev mode
```
pip install -r requirements.txt
sudo apt install motion uvicorn -y
sudo motion -m -c src/camera0.conf -d 9 -k INFO
cd src && uvicorn main:app  --host 0.0.0.0 --port 8000 --reload
```
documentation in swageer style is on https://0.0.0.0:8000/docs 
to have synthetic uart:
socat -d -d pty,raw,echo=0 pty,raw,echo=0
echo '{"temp_inside":3}' > /dev/pts/3
cat < /dev/pts/2
# run tests

cd src && pytest

# how it looks

![upper view of index.html](imgs_readme/1.png)
![bottom view of index.html](imgs_readme/2.png)