CREATE DATABASE IF NOT EXISTS auth_db;

USE auth_db;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE iplog (
    sno INT AUTO_INCREMENT PRIMARY KEY,
    ip VARCHAR(20) NOT NULL,
    tstamp VARCHAR(50) NOT NULL,
    type VARCHAR(20)
);

CREATE TABLE log_in_sessions(
    sno INTO AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    tstamp varchar(50) NOT NULL,
    ip VARCHAR(20) NOT NULL
);