import json
import os
import lxml.etree as ET
from acdh_tei_pyutils.tei import TeiReader

listperson = os.path.join("out", "amp-index-persons.xml")
doc = TeiReader(listperson)

for bad in doc.any_xpath(".//tei:div[@xml:id='relations']"):
    bad.getparent().remove(bad)

body = doc.any_xpath(".//tei:body")[0]
div_relations = ET.Element("{http://www.tei-c.org/ns/1.0}div")
div_relations.attrib["{http://www.w3.org/XML/1998/namespace}id"] = "relations"
body.append(div_relations)

rel_type = "person_person"
print(f"processing {rel_type} relations")
list_rel = ET.Element("{http://www.tei-c.org/ns/1.0}listRelation")
list_rel.attrib["{http://www.w3.org/XML/1998/namespace}id"] = rel_type
div_relations.append(list_rel)

with open(f"./json_dumps/{rel_type}.json", "r", encoding="utf-8") as fp:
    data = json.load(fp)
for x in data.values():
    active_id = f'#amp_person_{x["source"][0]["id"]}'
    active_label = x["source"][0]["value"]
    passive_id = f'#amp_person_{x["target"][0]["id"]}'
    passive_label = x["target"][0]["value"]
    relation_name = x["relation_type_object"][0]["value"].replace("_", "-")
    relation_label = relation_name.replace("-", " ")
    n = f"{active_label} — {relation_label} — {passive_label}"
    rel = ET.Element("{http://www.tei-c.org/ns/1.0}relation")
    list_rel.append(rel)
    rel.attrib["name"] = relation_name
    rel.attrib["active"] = active_id
    rel.attrib["passive"] = passive_id
    rel.attrib["n"] = n

rel_type = "person_org"
print(f"processing {rel_type} relations")
list_rel = ET.Element("{http://www.tei-c.org/ns/1.0}listRelation")
list_rel.attrib["{http://www.w3.org/XML/1998/namespace}id"] = rel_type
div_relations.append(list_rel)
with open(f"./json_dumps/{rel_type}.json", "r", encoding="utf-8") as fp:
    data = json.load(fp)
for x in data.values():
    active_id = f'#amp_person_{x["source"][0]["id"]}'
    active_label = x["source"][0]["value"]
    passive_id = f'#amp_organization_{x["target"][0]["id"]}'
    passive_label = x["target"][0]["value"]
    relation_name = x["relation_type_object"][0]["value"].replace("_", "-")
    relation_label = relation_name.replace("-", " ")
    n = f"{active_label} — {relation_label} — {passive_label}"
    rel = ET.Element("{http://www.tei-c.org/ns/1.0}relation")
    list_rel.append(rel)
    rel.attrib["name"] = relation_name
    rel.attrib["active"] = active_id
    rel.attrib["passive"] = passive_id
    rel.attrib["n"] = n

rel_type = "person_place"
print(f"processing {rel_type} relations")
list_rel = ET.Element("{http://www.tei-c.org/ns/1.0}listRelation")
list_rel.attrib["{http://www.w3.org/XML/1998/namespace}id"] = rel_type
div_relations.append(list_rel)
with open(f"./json_dumps/{rel_type}.json", "r", encoding="utf-8") as fp:
    data = json.load(fp)
for x in data.values():
    active_id = f'#amp_person_{x["source"][0]["id"]}'
    active_label = x["source"][0]["value"]
    passive_id = f'#amp_place_id_{x["target"][0]["id"]}'
    passive_label = x["target"][0]["value"]
    relation_name = x["relation_type_object"][0]["value"].replace("_", "-")
    relation_label = relation_name.replace("-", " ")
    n = f"{active_label} — {relation_label} — {passive_label}"
    rel = ET.Element("{http://www.tei-c.org/ns/1.0}relation")
    list_rel.append(rel)
    rel.attrib["name"] = relation_name
    rel.attrib["active"] = active_id
    rel.attrib["passive"] = passive_id
    rel.attrib["n"] = n

doc.tree_to_file(listperson)
print("done")
