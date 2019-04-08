# CSC 431 REST API Protocol

This document describes the protocol for retrieving data from the backend. This API is how frontend will iteract with the backend to retrieve data.

There are three endpoints:
1. _**Hazards Summary Endpoint**_: This endpoint will be used by the hazard landing page
2. _**Hazard Data Endpoint**_: This endpoint will be used by the hazard information page.
3. _**Hazard Data Download Endpoint**_: This endpoint will be used by the hazard information page and possibly used independently to generate a zip download.

## Test Server
Limited functionality of this API is currently supported at this URL: http://ec2-3-82-161-15.compute-1.amazonaws.com. Check out the first API endpoint: http://ec2-3-82-161-15.compute-1.amazonaws.com/api/volcanoes.

Features that are currently not supported.
1. There is no `earthquakes` support
2. There is no support for downloading zips.
3. How images are served may change

## The API

**Hazards Summary Endpoint**
-----------

* **URL**

	`/api/:hazard_type/`

* **Use Case**
  * Get all data for hazard landing page.
  * The 2 supported hazard types are "volcanoes" and "earthquakes"
<br/><br/>

* **Method**

	`GET /api/<hazard_type>`


* **Successful Response example**

```
$ curl -i <url.com>/api/volcanoes
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 627
Server: Werkzeug/0.14.1 Python/3.6.7
Date: Wed, 19 Mar 2019 18:22:27 GMT

{
  "hazards": [
    {
      "hazard_id": "VolcanoName0",
      "last_updated": "05182019",
      "location": {
        "latitude": 0.0,
        "longitude": 0.0
      },
      "name": "Volcano Name 0"
    },
    {
      "hazard_id": "VolcanoName1",
      "last_updated": "05182019",
      "location": {
        "latitude": 1.0,
        "longitude": 1.0
      },
      "name": "Volcano Name 1"
    },
  ],
  "type": "volcanoes"
}
```

* **Unsuccessful Response**

```
$ curl -i "<url.com>/api/tornadoes"
HTTP/1.0 404 NOT FOUND
Content-Type: application/json
Content-Length: 70
Server: Werkzeug/0.14.1 Python/3.6.7
Date: Wed, 20 Mar 2019 18:24:58 GMT

{
  "error": "404 Not Found: Hazard Type tornadoes does not exist."
}
```

* **Notes**

	- The `earthquakes` hazard type is not currently implemented on the test server



**Hazard Data Endpoint**
----------

* **URL**

	`/api/:hazard_type/:hazard_id`

* **Use Case**
  * Get data for the hazard information page by `hazard_id`.
  * Supported hazards: `volcanoes` and `earthquakes`.
<br/><br/>

* **Method**

	`GET /api/:hazard_type/:hazard_id`

* **URL Params**

	*Required*

	* `'image_types'=List[geo_backscatter, geo_interferogram, ...]`
  	- Any empty list of `image_type`s (i.e. not declaring the parameter)
     will retrieve all image types.
    - These are the  supported image types: "geo_backscatter", "geo_coherence", "geo_interferogram", "ortho_backscatter", "ortho_coherence", "ortho_interferogram"

	*Optional*

  * `"satellites"=[<satellite_id>]`
    - An empty list of satellites
  * `"start_date"="mmddyyyy"`
  * `"end_date"="mmddyyyy"`
  * `"max_num_images"=Integer`
  * `"last_n_days"=Integer`
<br/><br/>

* **Success Response**

```
$ curl -i "<url.com>/api/volcanoes/VolcanoName?image_types=ortho_interferogram,ortho_backscatter&max_num_images=2"
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 2012
Server: Werkzeug/0.14.1 Python/3.6.7
Date: Wed, 20 Mar 2019 18:46:41 GMT

{
  "hazard_id": "VolcanoName",
  "hazard_name": "Volcano Name",
  "images_by_satellite": {
    "satellite_id0": {
      "ortho_backscatter": [
        {
          "compressed_image_url": "/api/images/scatter03061999_compressed.jpg",
          "date": "03061999",
          "full_image_url": "/api/images/scatter03061999_full.jpg"
        },
        {
          "compressed_image_url": "/api/images/scatter03061999_compressed.jpg",
          "date": "03061999",
          "full_image_url": "/api/images/scatter03061999_full.jpg"
        }
      ],
      "ortho_interferogram": [
        {
          "compressed_image_url": "/api/images/scatter03061999_compressed.jpg",
          "date": "03061999",
          "full_image_url": "/api/images/scatter03061999_full.jpg"
        },
        {
          "compressed_image_url": "/api/images/scatter03061999_compressed.jpg",
          "date": "03061999",
          "full_image_url": "/api/images/scatter03061999_full.jpg"
        }
      ]
    },
    "satellite_id1": {...}
  },
  "last_updated": "05182019",
  "location": {
    "latitude": 0.0,
    "longitude": 0.0
  }
}
```


* **Notes**
  * Should we include any metadata with each image?
    - Assuming the image date is "in" the generated image, do we need to include the image date?
  * The `last_n_days` parameter can only be used if neither the `start_date` and `end_date` parameters are used.
  * `max_num_images` will use the most recent images first.
  * Images in the response content will be ordered chronologically with newest images first.
  * TODO

**Hazard Download**
----------

* **URL**

	`/api/:hazard/download/:hazard_id`

* **Use Case**
  * Download data by `hazard_id`
<br/><br/>

* **Method**

	`GET`

* **URL Params**

  *Required*

  * `"hazard_id"=Integer`

  *Optional*

  * `"satellites"=[satellite_id]`
  * `"start_date"="mmddyyyy"`
  * `"end_date"="mmddyyyy"`
  * `"max_num_images"=Integer`
  * `"last_n_days"=Integer`
  * `"dataType"=OneOf["GEOTIFF", "KMZ", "raw", "GIF"]`
<br/><br/>
* **Success Response**

	**Content:** link to file for download
