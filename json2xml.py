from baserow_utils import make_xml, make_geojson


data = {
    "persons": "json_dumps/persons.json",
    "places": "json_dumps/places.json",
    "lit": "json_dumps/literary_works.json",
    "org": "json_dumps/organizations.json",
    "eve": "json_dumps/events.json"
}
# create TEI/XML
listperson = make_xml(data["persons"], "listperson", "gnd", "persons")
listplace = make_xml(data["places"], "listplace", "geonames_id", "places")
listorg = make_xml(data["org"], "listorg", "wikidata", "orgs")
listbibl = make_xml(data["lit"], "listbibl", "is_linked_with", "bibl")
listbibl = make_xml(data["eve"], "listevent", "wikidata", "events")
# create geojson
placejson = make_geojson(
    data["places"],
    "listplace",
    "geonames_coordinates",
    "google_maps_coordinates",
    "location"
)
orgjson = make_geojson(
    data["org"],
    "listorg",
    "geonames_coordinates",
    "google_maps_coordinates",
    "location"
)
orgjson = make_geojson(
    data["eve"],
    "listevent",
    "geonames_coordinates",
    "google_maps_coordinates",
    "place_of_event"
)
