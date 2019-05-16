CREATE DATABASE hazards; -- creates database hazards

USE hazards; -- chooses database hazards it is required in order to interact with the chosen database

CREATE TABLE satellites ( -- creates table storing satellites
    `id` 		    CHAR(3),
    `name` 	        VARCHAR(50) NOT NULL,
    `direction`     ENUM('ASC', 'DESC') NOT NULL,
    PRIMARY KEY (`id`, `direction`)
);


CREATE TABLE hazards ( -- table allocated for volcanoes, earthquakes and non-hazards
    `id` 		    CHAR(6),
    `type` 	        ENUM('volcano', 'earthquake', 'non_hazard') NOT NULL,
    `name`	        VARCHAR(30) NOT NULL,
    `latitude` 	    VARCHAR(50) NOT NULL,
    `longitude`     VARCHAR(50) NOT NULL,
    `updated` 	    DATE,
    PRIMARY KEY(`id`)
);


CREATE TABLE images ( -- table storing images assigned to particular hazard
    `id`             CHAR(8),
    `haz_id`         CHAR(6),
    `sat_id`         CHAR(3),
    `img_date`       DATE,
    `img_type`       ENUM('geo_backscatter',
                        'geo_coherence',
                        'geo_interferogram',
                        'ortho_backscatter',
                        'ortho_coherence',
                        'ortho_interferogram') NOT NULL,
    `raw_img_url`    VARCHAR(200) NOT NULL,
    `mod_image_url`  VARCHAR(200) NOT NULL,
    `tif_image_url`  VARCHAR(200) NOT NULL,
    PRIMARY KEY(`id`),
    FOREIGN KEY (`haz_id`) REFERENCES hazards(`id`),
    FOREIGN KEY (`sat_id`) REFERENCES satellites(`id`)
);
