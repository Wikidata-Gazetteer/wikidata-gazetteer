from bz2 import BZ2Decompressor
from csv import writer
from csv import QUOTE_ALL
from json import dumps
from json import loads
from urllib.request import urlopen
from wg_utils import *

number_of_chunks = 50
CHUNK = 16 * 1024

decompressor = BZ2Decompressor()
print("decompressor:", decompressor)

req = urlopen('https://dumps.wikimedia.org/wikidatawiki/entities/latest-all.json.bz2')
print("req:", req)


text = b""

output_file = open("/tmp/wikidata-gazetteer.csv", "w")
writer = writer(output_file, delimiter="\t", quotechar='"', quoting=QUOTE_ALL)

for n in range(number_of_chunks):
    chunk = req.read(CHUNK)
    if not chunk:
        break
    text += decompressor.decompress(chunk)
    number_of_lines = text.count(b"\n")
    for n in range(number_of_lines):
        index = text.find(b"},\n")
        if index == -1:
            break
        else:
            entity = loads(text[:index + 1].replace(b"[\n", b"").decode("utf-8"))

            entity_id = entity['id']

            entity_type = entity['type']

            primary_name = get_primary_name_from_entity(entity)
            alternative_names = get_alternative_names_from_entity(entity, primary_name)

            if primary_name and "claims" in entity:
                claims = entity["claims"]

                latitude, longitude = get_coords_from_claims(claims)
                if latitude and longitude:

                    sitelinks = get_site_links(entity)
                    elevation = get_prop(claims, 2044)
                    geonames_id = get_prop(claims, 1566)
                    population = get_prop(claims, 1082)
                    country = get_prop(claims, 17)
                    #print("country:", country)
                    timezone = get_prop(claims, 421)
                    #wikidata_classes = get_prop(claims, 31)
                    wikidata_classes = get_instance_ofs(claims)
                    #print("wikidata_classes:", wikidata_classes)
                    #print("timezone:", timezone)
                    enwiki_title = sitelinks.get("enwiki", "")
                    writer.writerow([
                        primary_name,
                        enwiki_title,
                        alternative_names,
                        country,
                        wikidata_classes,
                        elevation,
                        geonames_id,                       
                        latitude,
                        longitude,
                        population,
                    ])
                    
                                    


            text = text[index + 3:]

req.close()
output_file.close()
