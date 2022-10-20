#!/bin/bash

sudo apt-get update
sudo apt-get upgrade -y
sudo apt install python3.10

sudo apt install python3-pip -y
sudo apt-get install python3.10 libmysqlclient-dev -y
sudo pip install -r requirements.txt

sudo apt install gunicorn -y
sudo apt install python3-flask -y

sudo cp test.service /etc/systemd/system/test.service
sudo systemctl daemon-reload
sudo systemctl start test
sudo systemctl enable test

sudo apt-get install nginx -y
sudo systemctl start nginx
sudo systemctl enable nginx
sudo cp default /etc/nginx/sites-available/default
sudo systemctl restart nginx