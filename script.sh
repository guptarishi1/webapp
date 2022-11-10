#!/bin/bash

sudo apt-get update
sudo apt-get upgrade -y

sudo apt-get install virtualenv -y
sudo apt install python3-pip -y
sudo apt-get install libmysqlclient-dev -y
sudo python3 -m pip install -U pip
sudo apt install gunicorn -y
sudo apt install mysql-client -y
sudo apt-get install nginx -y
virtualenv -p python3 /home/ubuntu/flask && source /home/ubuntu/flask/bin/activate
sudo pip install statsd
sudo pip install -r requirements.txt

sudo cp default /etc/nginx/sites-available/default

sudo systemctl daemon-reload
sudo systemctl start nginx
sudo systemctl enable nginx
sudo systemctl restart nginx

sudo cp test.service /etc/systemd/system/test.service

sudo systemctl daemon-reload
sudo systemctl start test.service
sudo systemctl enable test.service
sudo systemctl restart test.service

#install cloud watch agent
#download it
sudo curl -o /root/amazon-cloudwatch-agent.deb https://s3.amazonaws.com/amazoncloudwatch-agent/debian/amd64/latest/amazon-cloudwatch-agent.deb
#install it
sudo dpkg -i -E /root/amazon-cloudwatch-agent.deb


#start cloudwatch agent
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
    -a fetch-config \
    -m ec2 \
    -c file:/home/ubuntu/cloudwatch-config.json \
    -s

sudo systemctl enable amazon-cloudwatch-agent.service
sudo service amazon-cloudwatch-agent start
