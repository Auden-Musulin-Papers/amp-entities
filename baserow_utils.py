import requests
import geocoder
import json

from acdh_id_reconciler import gnd_to_wikidata_custom, geonames_to_gnd, geonames_to_wikidata
from AcdhArcheAssets.uri_norm_rules import get_normalized_uri
from acdh_obj2xml_pyutils import ObjectToXml

from config import (BASEROW_URL, BASEROW_TOKEN, br_client)


def enrich_data(br_table_id, uri, field_name_input, field_name_update):
    table = [x for x in br_client.yield_rows(br_table_id=br_table_id)]
    br_rows_url = f"{BASEROW_URL}database/rows/table/{br_table_id}/"
    v_wd = 0
    v_pmb = 0
    v_geo = 0
    for x in table:
        update = {}
        if uri == "gnd":
            try:
                norm_id = get_normalized_uri(x[field_name_input["gnd"]])
                print(norm_id)
            except Exception as err:
                print(err)
            try:
                wdc = gnd_to_wikidata_custom(norm_id, "P12483")
                wd = wdc["wikidata"]
                update[field_name_update["wikidata"]] = wd
                if len(wdc["custom"]) > 0:
                    pmb = wdc["custom"]
                    update[field_name_update["pmb"]] = f"https://pmb.acdh.oeaw.ac.at/entity/{pmb}"
                    v_pmb += 1
                    print(f"gnd id matched with pmb: https://pmb.acdh.oeaw.ac.at/entity/{pmb}")
                v_wd += 1
                print(f"gnd id matched with wikidata: {wd}")
            except Exception as err:
                print(err)
                print(f"no match for {norm_id} found.")
        if uri == "geonames":
            try:
                norm_id = get_normalized_uri(x[field_name_input["geonames"]])
                print(norm_id)
                update[field_name_update["geonames"]] = norm_id
            except Exception as err:
                print(err)
            try:
                geo = geonames_to_gnd(norm_id)
                gnd = geo["gnd"]
                update[field_name_update["gnd"]] = f"https://d-nb.info/gnd/{gnd}"
                wd = geo["wikidata"]
                update[field_name_update["wikidata"]] = wd
                v_geo += 1
                print(f"geonames id matched with gnd: {gnd} and wikidata: {wd}")
            except Exception:
                try:
                    wd = geonames_to_wikidata(norm_id)
                    wd = wd["wikidata"]
                    update[field_name_update["wikidata"]] = wd
                    print(f"geonames id matched with wikidata id: {wd}")
                except Exception:
                    print(f"no wikidata match for {norm_id} found.")
                print(f"no gnd match for {norm_id} found.")
        if update:
            print(update)
            update["updated"] = True
            row_id = x["id"]
            url = f"{br_rows_url}{row_id}/?user_field_names=true"
            print(url)
            try:
                requests.patch(
                    url,
                    headers={
                        "Authorization": f"Token {BASEROW_TOKEN}",
                        "Content-Type": "application/json"
                    },
                    json=update
                )
            except Exception as err:
                print(err)
    print(f"""{str(v_wd)} wikidata uri, {str(v_pmb)} pmb uri and {str(v_geo)}
          geonames uri of {len(table)} table rows matched""")


def geonames_to_location(br_table_id, user, field_name_input, field_name_update):
    table = [x for x in br_client.yield_rows(br_table_id=br_table_id)]
    br_rows_url = f"{BASEROW_URL}database/rows/table/{br_table_id}/"
    geo_u = 0
    for x in table:
        update = {}
        if (x["updated_geonames"] is False):
            try:
                norm_id = get_normalized_uri(x[field_name_input["geonames"]])
                print(norm_id)
                geo_id = norm_id.split('/')[-2]
            except Exception as err:
                print(err)
            try:
                g = geocoder.geonames(geo_id, method='details', key=user)
                lat = g.lat
                lng = g.lng
                typ = g.class_description
                typ_c = g.feature_class
                ctry_c = g.country_code
                ctry = g.country
                if lat and lng:
                    update[field_name_update["coordinates"]] = f"{lat}, {lng}"
                if typ:
                    update[field_name_update["place_type"]] = typ
                if typ_c:
                    update[field_name_update["place_type_class"]] = typ_c
                if ctry:
                    update[field_name_update["country"]] = ctry
                if ctry_c:
                    update[field_name_update["country_code"]] = ctry_c
                geo_u += 1
                print(f"geonames id {geo_id} found. Updating lat: {lat} and lng: {lng}")
            except Exception:
                print(f"no match for {norm_id} found.")
        if update:
            update["updated_geonames"] = True
            row_id = x["id"]
            url = f"{br_rows_url}{row_id}/?user_field_names=true"
            print(url)
            try:
                requests.patch(
                    url,
                    headers={
                        "Authorization": f"Token {BASEROW_TOKEN}",
                        "Content-Type": "application/json"
                    },
                    json=update
                )
            except Exception as err:
                print(err)
    print(f"{geo_u} geonames uri and of {len(table)} table rows matched")


def make_xml(input, fn, clmn, temp):
    with open(input, "rb") as f:
        file = json.load(f)
    arr = []
    for f in file:
        obj = file[f]
        try:
            any_id = obj[clmn]
            norm_id = get_normalized_uri(any_id)
            obj[clmn] = norm_id
        except KeyError as err:
            print(err)
        if clmn == "is_linked_with":
            try:
                uri = obj["is_linked_with"].split("/")[2]
            except IndexError:
                uri = "none"
            if uri == "www.wikidata.org":
                obj["wikidata"] = obj["is_linked_with"]
            elif uri == "d-nb.info":
                obj["gnd"] = obj["is_linked_with"]
            elif uri != "baserow.acdh-dev.oeaw.ac.at":
                obj["other"] = obj["is_linked_with"]
        arr.append(obj)
    filename = fn
    template_file = f"templates/{temp}.xml"
    obj_cl = ObjectToXml(br_input=arr, filename=filename, template_path=template_file)
    tei = obj_cl.make_xml_single(save=True)
    print(f"{fn}.xml created")
    return tei


def make_geojson(input, fn, clmn1, clmn2, clm3):
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }
    with open(input, "rb") as f:
        file = json.load(f)
    for f in file:
        obj = file[f]
        try:
            loc = obj[clmn1]
            if loc:
                if len(loc) != 0:
                    coords = loc
                    coords = coords.split(",")
                    feature_point = {
                        "type": "Feature",
                        "geometry": {
                            "type": "Point",
                            "coordinates": [float(coords[1]), float(coords[0])]
                        },
                        "properties": {
                            "title": obj["name"],
                            "id": obj["amp_id"],
                            "country_code": obj["country_code"]
                        }
                    }
                    geojson["features"].append(feature_point)
        except KeyError as err:
            print(err)
        try:
            loc = obj[clmn2]
            if loc:
                if len(loc) != 0:
                    coords = loc
                    coords = coords.split(",")
                    feature_point = {
                        "type": "Feature",
                        "geometry": {
                            "type": "Point",
                            "coordinates": [float(coords[1]), float(coords[0])]
                        },
                        "properties": {
                            "title": obj["name"],
                            "id": obj["amp_id"],
                            "country_code": obj["country_code"]
                        }
                    }
                    geojson["features"].append(feature_point)
        except KeyError as err:
            print(err)
        try:
            loc = obj[clm3]
        except KeyError as err:
            print(err)
            loc = []
        if len(loc) > 0:
            nm = obj["name"]
            o_id = obj["amp_id"]
            for x in loc:
                try:
                    coords = x["data"][clmn1]
                except KeyError:
                    coords = {}
                if coords:
                    coords = coords.split(",")
                    feature_point = {
                        "type": "Feature",
                        "geometry": {
                            "type": "Point",
                            "coordinates": [float(coords[1]), float(coords[0])]
                        },
                        "properties": {
                            "title": nm,
                            "id": o_id,
                            "title_plc": x["data"]["name"],
                            "id_plc": x["data"]["amp_id"],
                            "country_code": x["data"]["country_code"]
                        }
                    }
                    geojson["features"].append(feature_point)
                else:
                    try:
                        coords = x["data"][clmn2]
                    except KeyError:
                        coords = {}
                    if len(coords) > 0:
                        coords = coords.split(",")
                        feature_point = {
                            "type": "Feature",
                            "geometry": {
                                "type": "Point",
                                "coordinates": [float(coords[1]), float(coords[0])]
                            },
                            "properties": {
                                "title": nm,
                                "id": o_id,
                                "title_plc": x["data"]["name"],
                                "id_plc": x["data"]["amp_id"],
                                "country_code": x["data"]["country_code"]
                            }
                        }
                        geojson["features"].append(feature_point)
    with open(f"out/{fn}.geojson", "w") as f:
        json.dump(geojson, f)
    return geojson


def load_lockup(path, mapping):
    files = {}
    for x in mapping:
        ldn = mapping[x].split(".")[0]
        with open(f"{path}/{mapping[x]}", "rb") as fb:
            files[ldn] = json.load(fb)
    # with open(f"{path}/test_{mapping[x]}", "w") as fb:
    #     json.dump(files, fb)
    return files


def load_base(fn):
    with open(fn, "rb") as fb:
        data = json.load(fb)
    return data


def denormalize_json(fn, path, mapping):
    save_and_open = f"{path}/{fn}.json"
    print(f"updating {save_and_open}")
    # load mapping file
    mpg = mapping
    # load lockup file to match with
    files = load_lockup(path, mpg)
    # load base json file for matching
    dta = load_base(save_and_open)
    for m in mpg:
        # if mapping key is found in base json
        for d in dta:
            if dta[d][m]:
                # get filename without ext
                ldn = mpg[m].split(".")[0]
                print(ldn, "json file found")
                # get specific mapping from lockup file
                lockup = files[ldn]
                # iterate over mapping entity array
                for i in dta[d][m]:
                    i_id = i["id"]
                    print(i_id, "id found")
                    # use id for lockup file
                    try:
                        i_upt = lockup[str(i_id)]
                        # create normalized data
                        norm = {n: i_upt[n] for n in i_upt
                                if n != "id" and n != "order"}
                        i["data"] = norm
                        i["data"]["filename"] = mpg[m]
                    except KeyError:
                        continue
    with open(save_and_open.replace(".json", "__denorm.json"), "w") as w:
        json.dump(dta, w)
    print(f"finished update of {save_and_open} and save as {save_and_open}.")
    return dta


def merge_relationships_json(*args):
    new_dict = []
    for x in args:
        with open(x, "rb") as fb:
            file = json.load(fb)
            for f in file:
                new_dict.append(file[f])
    with open("json_dumps/merged_relationships.json", "w") as f:
        json.dump(new_dict, f)
    return file
