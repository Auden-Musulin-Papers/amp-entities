import requests
import geocoder

from acdh_id_reconciler import gnd_to_wikidata, geonames_to_gnd, geonames_to_wikidata
from AcdhArcheAssets.uri_norm_rules import get_normalized_uri

from config import (BASEROW_URL, BASEROW_TOKEN, br_client)


def enrich_data(br_table_id, uri, field_name_input, field_name_update):
    table = [x for x in br_client.yield_rows(br_table_id=br_table_id)]
    br_rows_url = f"{BASEROW_URL}database/rows/table/{br_table_id}/"
    v_wd = 0
    v_geo = 0
    for x in table:
        update = {}
        if uri == "gnd":
            if (len(x[field_name_input["gnd"]]) > 0 and len(x[field_name_input["wikidata"]]) == 0):
                norm_id = get_normalized_uri(x[field_name_input["gnd"]])
                print(norm_id)
                try:
                    wd = gnd_to_wikidata(norm_id)
                    wd = wd["wikidata"]
                    v_wd += 1
                    update[field_name_update["wikidata"]] = wd
                    print(f"gnd id matched with wikidata: {wd}")
                except Exception as err:
                    print(err)
                    print(f"no match for {norm_id} found.")
        if uri == "geonames":
            if (len(x[field_name_input["geonames"]]) and len(x[field_name_input["wikidata"]]) == 0):
                norm_id = get_normalized_uri(x[field_name_input["geonames"]])
                print(norm_id)
                update[field_name_update["geonames"]] = norm_id
                try:
                    geo = geonames_to_gnd(norm_id)
                    gnd = geo["gnd"]
                    update[field_name_update["gnd"]] = f"https://d-nb.info/gnd/{gnd}"
                    wd = geo["wikidata"]
                    update[field_name_update["wikidata"]] = wd
                    v_geo += 1
                    print(f"geonames id matched with gnd: {gnd} and wikidata: {wd}")
                except Exception as err:
                    try:
                        wd = geonames_to_wikidata(norm_id)
                        wd = wd["wikidata"]
                        update[field_name_update["wikidata"]] = wd
                    except Exception:
                        print(f"no wikidata match for {norm_id} found.")
                    print(f"no gnd match for {norm_id} found.")
        if update:
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
    print(f"{v_wd} wikidata uri and {v_geo} geonames uri of {len(table)} table rows matched")

def geonames_to_location(br_table_id, user, field_name_input, field_name_update):
    table = [x for x in br_client.yield_rows(br_table_id=br_table_id)]
    br_rows_url = f"{BASEROW_URL}database/rows/table/{br_table_id}/"
    geo_u = 0
    for x in table:
        update = {}
        if (len(x[field_name_input["geonames"]]) > 0 and x["updated"] == False):
            norm_id = get_normalized_uri(x[field_name_input["geonames"]])
            print(norm_id)
            geo_id = norm_id.split('/')[-2]
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
            except Exception as err:
                print(f"no match for {norm_id} found.")
        if update:
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
    print(f"{geo_u} geonames uri and of {len(table)} table rows matched")
