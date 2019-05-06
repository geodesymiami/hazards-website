***mySQL code creating the database with all necesary tables***

--all data is pretty much self expenatory, the main designation of each table is described

CREATE DATABASE hazards; --//--creates database hazards

USE hazards; --//--chooses database hazards -- it is reqired in order to interact with the chosen database

CREATE TABLE satellites (  --//-- creates table storing satellites
sat_id 		CHAR(16),
sat_name 	VARCHAR(50) NOT NULL,
ascending 	VARCHAR(10) NOT NULL,
PRIMARY KEY (sat_id));

CREATE TABLE hazard ( --// table allocatef for volcanos, earthquakes and non-hazards
haz_id 		CHAR(16),
haz_type 	ENUM('volcano', 'earthquake', 'non_hazard') NOT NULL,
haz_name 	VARCHAR(30) NOT NULL,
location 	VARCHAR(50) NOT NULL,
haz_date 	DATETIME,
PRIMARY KEY(haz_id));

CREATE TABLE image( --//table storing images assigned to particular (non)hazard
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
