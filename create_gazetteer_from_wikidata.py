from bz2 import BZ2Decompressor
from csv import writer
from csv import QUOTE_ALL
from json import dumps
from json import loads
from time import sleep
from urllib.request import urlopen
from wg_utils import *

# countries = {'Q792': 'El Salvador', 'Q822': 'Lebanon', 'Q1013': 'Lesotho'...
countries = get_countries()

# astronomical_bodies = {'Q405': 'Moon', 'Q313': 'Venus'}
astronomical_bodies = {}

decompressor = BZ2Decompressor()
print("decompressor:", decompressor)

req = urlopen('https://dumps.wikimedia.org/wikidatawiki/entities/latest-all.json.bz2')
print("req:", req)

with open(path_to_output, "w") as output_file:
    csv_writer = writer(output_file, delimiter="\t", quotechar='"', quoting=QUOTE_ALL)
    csv_writer.writerow([
        "wikidata_id",
        "primary_name",
        "enwiki_title",
        "alternative_names",
        "country",
        "country_code",
        "wikidata_classes",
        "elevation",
        "geonames_id",
        "latitude",
        "longitude",
        "population",
        "osm_id",
        "astronomical_body"
    ])
print("wrote header for " + path_to_output)

text = b""


skip = 0

for n in range(number_of_chunks):

    if n < 10 or n % 1000 == 0:
        print("n:", n)

    if n <= skip:
        continue

    sleep(2)
    chunk = req.read(CHUNK)
    if not chunk:
        break
    text += decompressor.decompress(chunk)
    #print("text:", text)
    number_of_lines = text.count(b"\n")
    for n in range(number_of_lines):
        index = text.find(b"},\n")
        print("-", end="", flush=True)
        if index == -1:
            break
        else:
            entity_source_text = text[:index + 1].replace(b"[\n", b"").decode("utf-8")
            #print(entity_source_text)
            entity = loads(entity_source_text)

            entity_id = entity['id']

            entity_type = entity['type']

            primary_name = get_primary_name_from_entity(entity)
            alternative_names = get_alternative_names_from_entity(entity, primary_name)

            if primary_name and "claims" in entity:
                claims = entity["claims"]

                latitude, longitude = get_coords_from_claims(claims)
                if latitude and longitude:

                    wikidata_id = entity.get("id","")
                    sitelinks = get_site_links(entity)
                    elevation = get_prop(claims, 2044)
                    geonames_id = get_prop(claims, 1566)
                    population = get_prop(claims, 1082)
                    country = countries.get(get_prop(claims, 17), None)
                    country_name = country.get("name", "") if country else ""
                    country_code = country.get("cc", "") if country else ""
                    timezone = get_prop(claims, 421)
                    wikidata_classes = get_instance_ofs(claims)
                    enwiki_title = sitelinks.get("enwiki", "")
                    osm_id = get_prop(claims, 402) or ""
                    body = get_prop(claims, 376) or "Earth"
                    if body != "Earth":
                        if body not in astronomical_bodies:
                            for key, value in get_entity_names([body]).items():
                                astronomical_bodies[key] = value
                        body = astronomical_bodies.get(body, body)

                    with open(path_to_output, "a") as output_file:
                        csv_writer = writer(output_file, delimiter="\t", quotechar='"', quoting=QUOTE_ALL)
                        csv_writer.writerow([
                            wikidata_id,
                            primary_name,
                            enwiki_title,
                            alternative_names,
                            country_name,
                            country_code,
                            wikidata_classes,
                            elevation,
                            geonames_id,
                            latitude,
                            longitude,
                            population,
                            osm_id,
                            body
                        ])




            text = text[index + 3:]

req.close()
print("closed network connection")

print("finished creating gazetteer")
