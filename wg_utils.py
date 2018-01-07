def safeget(dct, *keys):
    for key in keys:
        try:
            dct = dct[key]
        except KeyError:
            return None
        except:
            print(str(key) + " not in " + str(dct))
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
        for language in ["en", "fr", "de", "ar"]:
            if language in labels:
                label = labels[language]
                if label:
                    value = label["value"]
                    if value:
                        return value

def get_prop(_dict, propid):
    value = safeget(_dict, "P" + str(propid), 0, "mainsnak", "datavalue", "value")
    if isinstance(value, dict):
        if "amount" in value:
            return cast_if_necessary(value['amount'])
    else:
        return cast_if_necessary(value)
