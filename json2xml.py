import glob
import json

from acdh_obj2xml_pyutils import ObjectToXml
from AcdhArcheAssets.uri_norm_rules import get_normalized_uri


INPUT = "json_dumps/*"

data = glob.glob(INPUT)
for x in data:
    with open(x, "rb") as f:
        file = json.load(f)
    arr = []
    for f in file:
        obj = file[f]
        try:
            any_id = obj["geonames_id"]
            norm_id = get_normalized_uri(any_id)
            obj["geonames_id"] = norm_id
        except KeyError:
            print()
        arr.append(obj)
    if "places" in x:
        filename = f"listplace"
        template_file = "templates/places.xml"
        obj_cl = ObjectToXml(br_input=arr, filename=filename, template_path=template_file)
        tei =  obj_cl.make_xml_single(save=True)
        print("listplace.xml created")
    if "persons" in x:
        filename = f"listperson"
        template_file = "templates/persons.xml"
        obj_cl = ObjectToXml(br_input=arr, filename=filename, template_path=template_file)
        tei =  obj_cl.make_xml_single(save=True)
        print("listperson.xml created")
    if "organizations" in x:
        filename = f"listorg"
        template_file = "templates/orgs.xml"
        obj_cl = ObjectToXml(br_input=arr, filename=filename, template_path=template_file)
        tei =  obj_cl.make_xml_single(save=True)
        print("listorg.xml created")
    if "literary_works" in x:
        filename = f"listbibl"
        template_file = "templates/bibl.xml"
        obj_cl = ObjectToXml(br_input=arr, filename=filename, template_path=template_file)
        tei =  obj_cl.make_xml_single(save=True)
        print("listbibl.xml created")
    