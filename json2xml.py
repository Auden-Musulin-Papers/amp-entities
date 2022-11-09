import glob
import json

from acdh_obj2xml_pyutils import ObjectToXml


INPUT = "json_dumps/*"

data = glob.glob(INPUT)
for x in data:
    with open(x, "r") as f:
        file = json.load(f)
    arr = []
    for f in file:
        arr.append(file[f])
    if "places" in x:
        filename = f"listplace"
        template_file = "templates/places.xml"
        obj_cl = ObjectToXml(br_input=arr, filename=filename, template_path=template_file)
        tei =  obj_cl.make_xml_single(save=True)
    if "persons" in x:
        filename = f"listperson"
        template_file = "templates/persons.xml"
        obj_cl = ObjectToXml(br_input=arr, filename=filename, template_path=template_file)
        tei =  obj_cl.make_xml_single(save=True)
    if "organizations" in x:
        filename = f"listorg"
        template_file = "templates/orgs.xml"
        obj_cl = ObjectToXml(br_input=arr, filename=filename, template_path=template_file)
        tei =  obj_cl.make_xml_single(save=True)
    if "literary_works" in x:
        filename = f"listbibl"
        template_file = "templates/bibl.xml"
        obj_cl = ObjectToXml(br_input=arr, filename=filename, template_path=template_file)
        tei =  obj_cl.make_xml_single(save=True)
    