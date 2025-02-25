import json
# import lxml.etree as ET
# from acdh_tei_pyutils.tei import TeiReader


with open("./json_dumps/person_person.json", "r", encoding="utf-8") as fp:
    data = json.load(fp)

for x in data.values():
    print(x["source"][0]["id"])
