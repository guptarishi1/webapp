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
CREATE TABLE customer (
    id int not null AUTO_INCREMENT PRIMARY KEY,
    Last_Name varchar(255) NOT NULL,
    First_Name varchar(255) NOT NULL,
    username varchar(255) NOT NULL UNIQUE,
    account_created  varchar(255),
    password varchar(255) NOT NULL,
	account_updated  varchar(255)  
);
eof
