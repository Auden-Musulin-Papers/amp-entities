import os
import requests

from acdh_id_reconciler import gnd_to_wikidata, geonames_to_wikidata
from AcdhArcheAssets.uri_norm_rules import get_normalized_uri
from acdh_baserow_pyutils import BaseRowClient


BASEROW_DB_ID=274
BASEROW_URL="https://baserow.acdh-dev.oeaw.ac.at/api/"
BASEROW_USER = os.environ.get("BASEROW_USER")
BASEROW_PW = os.environ.get("BASEROW_PW")
BASEROW_TOKEN = os.environ.get("BASEROW_TOKEN")


br_client = BaseRowClient(BASEROW_USER, BASEROW_PW, BASEROW_TOKEN, br_base_url=BASEROW_URL)

def enrich_data(br_table_id, uri, field_name_input, field_name_update):
    table = [x for x in br_client.yield_rows(br_table_id=br_table_id)]
    br_rows_url = f"{BASEROW_URL}database/rows/table/{br_table_id}/"
    v_wd = 0
    v_geo = 0
    for x in table:
        update = {}
        if uri == "gnd":
            if (len(x[field_name_input["gnd"]]) > 0):
                norm_id = get_normalized_uri(x[field_name_input["gnd"]])
                print(norm_id)
                try:
                    wd = gnd_to_wikidata(norm_id)
                    wd = wd["wikidata"]
                    v_wd += 1
                    print(f"gnd id matched with wikidata: {wd}")
                except Exception as err:
                    wd = "N/A"
                    print(err)
                    print(f"no match for {norm_id} found.")
                update[field_name_update["wikidata"]] = wd
        if uri == "geonames":
            if (len(x[field_name_input["geonames"]]) > 0):
                norm_id = get_normalized_uri(x[field_name_input["geonames"]])
                print(norm_id)
                try:
                    geo = geonames_to_wikidata(norm_id)
                    gnd = geo["gnd"]
                    wd = geo["wikidata"]
                    v_geo += 1
                    print(f"geonames id matched with gnd: {gnd} and wikidata: {wd}")
                except Exception as err:
                    wd = "N/A"
                    gnd = "N/A"
                    print(err)
                    print(f"no match for {norm_id} found.")
                update[field_name_update["gnd"]] = f"https://d-nb.info/gnd/{gnd}"
                update[field_name_update["wikidata"]] = wd
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
