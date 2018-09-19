# wikidata-gazetteer
Gazetteer of places mentioned in wikidata.org

# download link
https://s3.amazonaws.com/firstdraftgis/wikidata-gazetteer.tsv.zip

## columns
| name                | description                                | example                                |
| ------------------- | -----------------------------------------  | -------------------------------------- |
| wikidata_id         | unique identifier (UID) used in Wikidata   | Q142                                   |
| primary_name        | name, usually in English                   | Armenia                                |
| enwiki_title        | title of wikipedia article                 | Georgia (country)                      |
| alternative_names   | aliases, acronymns and other names         | Грузи,জর্জিয়া,格鲁吉亚,Georgien,འཇོར་ཇི་ཡ,... |
| country             | name of country                            | Germany                                |
| country_code        | country code                               | FR                                     |
| wikidata_classes    | place is an instance of these classes      | member state of the European Union; island nation ... |
| elevation           | in raw units from wikidata                 | 52.0                                   |
| geonames_id         | id that corresponds to GeoNames record     | 614540                                 |
| latitude            | latitude in decimal degrees                | 42.016669444444                        |
| longitude           | longitude in decimal degrees               | 43.733330555556                        |
| population          | population                                 | 3729500.0                              |
| osm_id              | id in OpenStreetMap                        | 51477                                  |
| astronomical_body   | name of planet, moon, or other body        | Mars                                   |

## license
This code and gazetteer data is provided under a Public Domain License.  You can read the specific license here:
https://creativecommons.org/publicdomain/zero/1.0/.  If you have any concerns, please don't hesitate to contact us and we'll address them promptly.

# pickled set
You can also download a zipped pickled set in Python that holds all the titles of the articles about the places in the English Wikipedia.
You can download that [here](https://s3.amazonaws.com/firstdraftgis/place_titles.pickle.zip).

## contact
If you have any questions or comments about the data, license, or anything else, please don't hesitate to contact me at daniel.j.dufour@gmail.com.
