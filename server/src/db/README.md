# Database

Database Structure
------------------
The database is a standard MySQL 5.x database an can thus be queried using standard MySQL calls.

The structure of the the three database tables are as shown below:

#### hazards
| Column Name  	|  Data Type 	| Details
|---	        |---	        |---
| id  	        | char(16) 	    | **Primary Key**
| type 	        | enum 	        | 'volcanoes', 'earthquakes', 'non-hazards'
| name 	        | varchar(30) 	|
| latitude 	    | float 	    |
| longitude	    | float 	    |
| updated       | date          | YYYY-MM-DD format

#### satellites
| Column Name  	|  Data Type 	| Details
|---	        |---	        |---
| id  	        | char(16) 	    | **Primary Key**
| name 	        | varchar(50) 	|
| direction     | enum          | 'ASC', 'DESC'

#### images
| Column Name  	    |  Data Type 	| Details
|---	            |---	        |---
| id  	            | char(16) 	    | **Primary Key**
| haz_id            | char(30) 	    | Foreign Key to _hazards_
| sat_id 	        | char(30) 	    | Foreign Key to _satellites_
| img_date 	        | date 	        | YYYY-MM-DD format
| img_type	        | enum 	        | 'geo_backscatter', 'geo_coherence', 'geo_interferogram', 'ortho_backscatter', 'ortho_coherence', 'orther_iterferogram'
| raw_image_url     | varchar(1024) | 
| tif_image_url     | varchar(1024) |
| mod_image_url	    | varchar(1024) |

Running the Database Service
----------------------------

Unlike the data processing service and api service, the database can not be run separate, and thus must be invoked using a `docker-compose` call, like below:

`docker-compose build`

`docker-compose up -d`

After these two command are run from the `project/server` directory, the database will take several seconds to setup, after which it can be accessed by both other docker services and externally by other users.

To access the database from outside the docker container, use the following command sequence:

`docker exec -it db /bin/bash`

Executing the above command will, effectively, ssh into the docker container from which the database service is running, allowing you to run standard bash commands within the containers. Once inside the container, use:

`mysql -u root_username -p`

and enter the password accordingly. 

At this point you will have direct access to the MySQL database, and can run SQL calls to select, insert, or remove information from the database.

Database Connection Details
---------------------------- 

Database connection details, incuding the database host, username, password, and port should be stored in the `config.py` file, in a fashion similar to `config_ex.py`. 

If you are connecting from inside another docker container, make sure the `host` is set to the name of the container the database is running in. If you are connecting from outside another docker container, make sure the `host` is the ip address of the server where the database is being run on.

_Note that, when connecting from another docker container that is started via a `docker-compose up` command, the database container make take several seconds to setup before being accessible, so any code that attempts to connect to the database from another container, MUST wait until the database has finished setting up._