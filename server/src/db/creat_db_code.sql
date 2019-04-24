CREATE DATABASE hazards;

USE hazards;

CREATE TABLE satellites ( 
sat_id 		CHAR(16),
sat_name 	VARCHAR(50) NOT NULL,
ascending 	VARCHAR(10) NOT NULL,
PRIMARY KEY (sat_id));

CREATE TABLE hazard (
haz_id 		CHAR(16),
haz_type 	ENUM('volcano', 'earthquake', 'non_hazard') NOT NULL,
haz_name 	VARCHAR(30) NOT NULL,
location 	VARCHAR(50) NOT NULL,
haz_date 	DATETIME,
PRIMARY KEY(haz_id));

CREATE TABLE image(
img_id CHAR(16),
img_date DATETIME,
haz_id CHAR(30),
sat_id CHAR(30),
img_type INT NOT NULL,
raw_img_url VARCHAR(1024) NOT NULL,
tif_image_url VARCHAR(1024) NOT NULL,
modified_image_url VARCHAR(1024) NOT NULL,
PRIMARY KEY(img_id),
FOREIGN KEY (haz_id) REFERENCES hazard(haz_id),
FOREIGN KEY (sat_id) REFERENCES satellites(sat_id));