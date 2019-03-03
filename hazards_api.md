# **RSMAS Geohazards API**

## Main URL: `hazards.miami.edu/api/`
----

## **GET: hazard_type**
Description: returns back all of the individual hazards in the database of the provided hazard type (either volcano or earthquake)

URL: `/:hazard_type`

* `hazard_type`: String
  * "volcanoes"
  * "earthquakes"
* Example Call:
```
  GET: hazards.miami.edu/api/volcanoes/
```

Response: JSON `HazardType` Object

* Success
```
  {
    type: String,
    num_hazards: Integer,
    hazards: [Hazard]
  }
```
  * Example Response:
  ```
    {
      type: "volcano"
      num_hazards: 20,
      hazards: [Hazard]
    }
  ```
* Failure
```
  {
    type: String,
    error: String
  }
```
  * Example Response:
  ```
    {
      type: "tsunami"
      error: "Invalid hazard type `tsunami`"
    }
  ```
----

## **GET: hazard_id**
Description: returns back summary information and images for a specific hazard, *hazard_id*

URL: `/:hazard_type/:hazard_id`

* `hazard_type`: String
  * "volcanoes"
  * "earthquakes"
* `hazard_id`: Integer
* `image_types`: [String]
  * "geo_backscatter"
  * "geo_coherence"
  * "geo_interferogram"
  * "ortho_backscatter"
  * "ortho_coherence"
  * "ortho_interferogram"
  * "all_backscatter"
  * "all_coherence"
  * "all_interferogram"
* `satellites`: [String], *optional*
* `startDate`: StringDate ("mmddyyy"), *optional*
* `endDate`: StringDate ("mmddyyyy"), *optional*
* `max_images`: Integer, *optional*
* `last_n_days`: Integer, *optional*

Example Call:
```
  GET: hazards.miami.edu/api/volcanoes/000001?image_types="geo_backscatter","ortho_backscatter"&satellites="satellite1","satellite2"&startDate="11201998"&endDate="02282019"
```

Response: JSON `Hazard` Object

* Success
```
  {
    hazard_id: Integer
    summary_info: {
      hazard_name: String,
      location: {
        north: Double
        south: Double
        east:  Double
        west:  Double
      },
      ...
    },
    images: [
      {
        satellite_id: {
          name: String
          satellite_info: {
            ...
          },
          image_type: [
            {
              name: String,
              images: [
                {
                  date: StringDate ("mmddyyyy"),
                  comp_url: String,
                  full_url: String
                }
              ]
            },
            ...
          ]
        },
        ...
      }
    ]
  }
```
  * Example Response:
  ```
    {
      hazard_id: 000001,
      summary_info: {
        hazard_name: Fernandina1,
        location: {
          north: 20.0000,
          south: 19.0000,
          east:  10.0000,
          west:  12.0000
        },
        ...
      },
      images: [
        {
          000001: {
            name: "Sen000001",
            satellite_info: {
              ...
            },
            image_type: [
              {
                name: "geo_backscatter",
                images: [
                  {
                    date: "03061999",
                    comp_url: "hazards.miami.edu/images/scatter03061999_compressed.jpg",
                    full_url: "hazards.miami.edu/images/scatter03061999_full.jpg"
                  },
                  {
                    date: "04252015",
                    comp_url: "hazards.miami.edu/images/scatter04252015_compressed.jpg",
                    full_url: "hazards.miami.edu/images/scatter04252015_full.jpg"
                  },
                  ...
                ]
              },
              {
                name: "geo_coherence",
                images: [
                  {
                    date: "03061999",
                    comp_url: "hazards.miami.edu/images/coherence03061999_compressed.jpg",
                    full_url: "hazards.miami.edu/images/coherence03061999_full.jpg"
                  },
                  {
                    date: "04252015",
                    comp_url: "hazards.miami.edu/images/coherence04252015_compressed.jpg",
                    full_url: "hazards.miami.edu/images/coherence04252015_full.jpg"
                  },
                  ...
                ]
              },
              ...
            ]
          },
          000002: {
            name: "Sen000002",
            satellite_info: {
              ...
            },
            image_type: [
              {
                name: "geo_backscatter",
                images: [
                  {
                    date: "03061999",
                    comp_url: "hazards.miami.edu/images/scatter03061999_compressed.jpg",
                    full_url: "hazards.miami.edu/images/scatter03061999_full.jpg"
                  },
                  {
                    date: "04252015",
                    comp_url: "hazards.miami.edu/images/scatter04252015_compressed.jpg",
                    full_url: "hazards.miami.edu/images/scatter04252015_full.jpg"
                  },
                  ...
                ]
              },
              {
                name: "geo_coherence",
                images: [
                  {
                    date: "03061999",
                    comp_url: "hazards.miami.edu/images/coherence03061999_compressed.jpg",
                    full_url: "hazards.miami.edu/images/coherence03061999_full.jpg"
                  },
                  {
                    date: "04252015",
                    comp_url: "hazards.miami.edu/images/coherence04252015_compressed.jpg",
                    full_url: "hazards.miami.edu/images/coherence04252015_full.jpg"
                  },
                  ...
                ]
              },
              ...
            ]
          }
        }
      ]
    }
  ```

* Failure
```
  {
    hazard_id: String,
    error: String
  }
```
  * Example Response:
  ```
    {
      type: "21639"
      error: "Invalid hazard_id `21639`"
    }
  ```
----

## **GET: hazard_download**
Description: returns back all of the individual hazards in the database of the provided hazard type (either volcano or earthquake)

URL: `/:hazard_type/download/:hazard_id`

* `hazard_type`: String
  * "volcanoes"
  * "earthquakes"
* `hazard_id`: Integer
* `image_types`: [String]
  * "geo_backscatter"
  * "geo_coherence"
  * "geo_interferogram"
  * "ortho_backscatter"
  * "ortho_coherence"
  * "ortho_interferogram"
  * "all_backscatter"
  * "all_coherence"
  * "all_interferogram"
* `satellites`: [String], *optional*
* `startDate`: StringDate ("mmddyyy"), *optional*
* `endDate`: StringDate ("mmddyyyy"), *optional*
* `max_images`: Integer, *optional*
* `last_n_days`: Integer, *optional*
* `dataType`: [String], *optional*
  * "raw"
  * "kmz"
  * "gif"
  * "compressed"
  * "full"

Example Call:
```
  GET: hazards.miami.edu/api/volcanoes/download/000001?image_types="geo_backscatter","ortho_backscatter"&satellites="satellite1","satellite2"&startDate="11201998"&endDate="02282019"&dataType="raw"
```

Response: JSON `HazardDownload` Object

* Success
```
  {
    type: String,
    hazard_id: Integer,
    download: {
      raw: String,
      kmz: String,
      compressed: String,
      full: String,
      gif: String
    }
  }
```
  * Example Response:
  ```
    {
      type: "volcano"
      hazard_id: "96024"
      download: {
        raw: "hazards.miami.edu/volcanos/data/96024.data",
        kmz: null,
        compressed: null,
        full: null,
        gif: null
      }
    }
  ```
* Failure
```
  {
    type: String,
    hazard_id: String,
    data_type: [String]
    error: String
  }
```
  * Example Response:
  ```
    {
      type: "volcano",
      hazard_id: "96024"
      data_type: ["raw", "kml"]
      error: "Invalid data type `kml`"
    }
  ```
