# Data Processing

Processing Routine
------------------

1. Obtain list of image files from S3 bucket to process
2. Pull summary statistics from each image file
3. Save full size image as a .jpg file at 300 DPI
3. Compress full size image by 70%
4. Pad top of image to create room to write date to the image
5. Write date as text to the top of the image
6. Save image to the local file system
7. Push the local images to the S3 bucket
8. Remove local copies of the images from the local file system
9. Create a new entry in the database for the new image

Running the Processing Pipeline
-------------------------------

The processing pipeline, like the other components of this system, runs inside of a docker container, configured by the `Dockerfile` in this directory.
 
 To run this component of the system separately from the database and the api services, simply run the following commands from the `project/server` directory:
 
 `docker build --tag=processing src/preprocessing/Dockerfile .` 
 
 `docker run processing`
 
 Note that running the processing pipeline as above may result in errors when attempting to write entries to the database, as the database may or may not be active.
 
 To run this component in conjunction with the database and api services, as is the expected run configuration, simply run the following command from the `project/server` directory:
 
 `docker-compose build`
 
 `docker-compose up -d`
 
 `docker-compose` unlike `docker` is used to startup and run multiple linked services at once. Because the api/database/processing routines are all interdependent, using docker-compose is the suggest means by which to run the backend components.
 
Service Components
------------------
 
 #### _summary.py_
 
 Pulls the relevant summary statistics from a provided `.tif` image file. Summary statistics include:
 
 - Volcano Number
 - Volcano Name
 - Satellite Name
 - Satellited Direction
 - Image Type
 - Image Date
 - Geographic Coordinates of the image center
 
 (For more information on these data types )
 
 The volcano number and name are pulled from a local copy of the Smithsonian Institute database of volcanos, which can be found in the `resources/` directory. 
 
 The satellite name and direction, image type, and image date information is pulled from metadata stored in the `.tif` file.
 
 #### _image_saving.py_
 
 Contains several functions that allow for the saving of `pillow` image objects to the file system. Functionality includes the ability to save image objects to a local file or to an S3 service, as well as a function to move S3 objects around the S3 file system.
 
 #### _image_manipulation.py_
 
 Contains several functions to manipulate the content of images files. Functionality includes basic image compression, the ability to pad an image, and the ability to write text to an image file.
 
 #### _pipeline.py_
 
 Runs the complete data processing routine as outlined above.
 
 AWS S3 Storage
 -------------------
 
 Both `pipeline.py` and `image_saving.py` utilize `boto3` to connect to, save, and manipulate files on an AWS S3 Instance. 
 
 This, obviously, requires certain S3 authentication credentials. Such credentials can be stored in one of two ways: directly in a `config.py` file, or in a `~/.aws/credentials` file. 
 
 If you opt to use the config file approach, follow the syntax in `src/common/cofig_ex.py` and file in the S3 credentials where relevant.
 
 Otherwise, you can install the AWS Command-Line Interface from Amazon, and follow the setup instructions from there. This will generate the proper `~/.aws/` directory and files, which `boto3` and `gdal` will reference automatically where necessary. 
 