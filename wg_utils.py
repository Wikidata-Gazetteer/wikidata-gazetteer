from config import *
from json import loads
from os.path import isfile
from requests import get
from SPARQLWrapper import SPARQLWrapper, JSON
from urllib.request import urlretrieve

qid2name = {}

# returns something like {'Q792': 'El Salvador', 'Q822': 'Lebanon', 'Q1013': 'Lesotho'...}
def get_countries():
    sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
    sparql.setQuery("""
SELECT ?instance ?instanceLabel ?ISO_3166_2_code WHERE {
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
  ?instance wdt:P31 wd:Q6256.
  OPTIONAL { ?instance wdt:P297 ?ISO_3166_2_code. }
}
LIMIT 300    
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    bindings = results["results"]["bindings"]
    countries = dict([(i["instance"]["value"].split("/")[-1], {"name": i["instanceLabel"]["value"], "cc": i.get('ISO_3166_2_code',{}).get('value', None)}) for i in bindings])
    return countries

def safeget(dct, *keys):
    #print(dct)
    for key in keys:
        try:
            dct = dct[key]
        except KeyError:
            return None
        except:
            print(str(key) + " not in " + str(dct))
    #print("got", dct, "from", keys)
    return dct
    
def cast_if_necessary(value):
    if value is None:
        return value
    if value.startswith("+"):
        return float(value)
    else:
        return value

def get_coords_from_claims(claims):
    latitude = None
    longitude = None
    if "P625" in claims:
        P625 = claims["P625"]
        if len(P625) > 0:
            P625_0 = P625[0]
            if "mainsnak" in P625_0:
                mainsnak = P625_0["mainsnak"]
                if "datavalue" in mainsnak:
                    datavalue = mainsnak["datavalue"]
                    if "value" in datavalue:
                        value = datavalue["value"]
                        latitude = value.get("latitude")
                        longitude = value.get("longitude")  
    return latitude, longitude
    
def get_primary_name_from_entity(entity):
    if "labels" in entity:
        labels = entity["labels"]
        for language in ["en", "es", "fr", "de", "ar", "zh"]:
            if language in labels:
                label = labels[language]
                if label:
                    value = label["value"]
                    if value:
                        return value

def get_alternative_names_from_entity(entity, primary_name):
    names = []
    if "labels" in entity:
        labels = entity["labels"]
        for language in labels:
            label = labels[language]
            name = safeget(labels, language, "value")
            if name and name != primary_name and name not in names:
                names.append(name)
    if "aliases" in entity:
        aliases = entity["aliases"]
        for language in aliases:
            aliases_for_language = aliases[language]
            for alias in aliases_for_language:
                name = alias["value"]
                if name and name != primary_name and name not in names:
                    names.append(name)
    return ",".join([name for name in names if "," not in name])

def get_prop(_dict, propid):
    value = safeget(_dict, "P" + str(propid), 0, "mainsnak", "datavalue", "value")
    if isinstance(value, dict):
        if "amount" in value:
            return cast_if_necessary(value['amount'])
        elif "id" in value:
            return cast_if_necessary(value['id'])
    else:
        return cast_if_necessary(value)
 
 
def get_entity_names(qids):
    result = {}
    qids_to_query = []
    for qid in qids:
        if qid == "QNone":
            pass
        elif qid in qid2name:
            result[qid] = qid2name[qid]
        else:
            qids_to_query.append(qid)

    # don't query for a qid more than once
    if qids_to_query:    
        url = "https://www.wikidata.org/w/api.php?action=wbgetentities&ids=" + "|".join(qids_to_query) + "&languages=en&format=json"
        response_json = get(url).json()
        if "entities" in response_json:
            entities = response_json["entities"]
            for qid in entities:
                value = safeget(entities, qid, "labels", "en", "value")
                result[qid] = value
                qid2name[qid] = value
        else:
            print("[get_entity_names] entities for " + str(qids_to_query) + " not in " + str(response_json))
            
    return result
       
def get_instance_ofs(claims):
    instance_ofs = set()
    if "P31" in claims:
        P31 = claims["P31"]
        qids = ["Q" + str(safeget(v, "mainsnak", "datavalue", "value", "numeric-id")) for v in P31]
        #print("qids:", qids)
        names = get_entity_names(qids)
        #print("names:", names)
        for value in claims["P31"]:
            numeric_id = safeget(value, "mainsnak", "datavalue", "value", "numeric-id")
            if numeric_id:
                numeric_id_as_str = str(numeric_id)
                qid = "Q" + numeric_id_as_str
                instance_of = names.get(qid, numeric_id_as_str)
                if instance_of and ";" not in instance_of:
                    instance_ofs.add(instance_of)
    return "; ".join(list(instance_ofs))
        
def get_site_links(entity):
    result = {}
    if "sitelinks" in entity:
        sitelinks = entity["sitelinks"]
        for site in sitelinks:
            result[site] = sitelinks[site]["title"]
    return result
        
