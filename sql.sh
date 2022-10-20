#!/bin/bash

sudo apt-get update
sudo apt-get upgrade -y
sudo apt install mysql-server -y
sudo systemctl start mysql.service

sudo mysql <<MYSQL_SCRIPT
CREATE USER 'FlaskDB'@'localhost' IDENTIFIED BY 'FlaskDB@12345678';
GRANT ALL PRIVILEGES ON *.* TO 'FlaskDB'@'localhost' WITH GRANT OPTION;
CREATE DATABASE FlaskDB;
FLUSH PRIVILEGES;
MYSQL_SCRIPT

mysql -uFlaskDB -pFlaskDB@12345678<<eof
use FlaskDB;

eof
