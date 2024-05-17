from baserow_utils import make_xml, make_geojson


data = {
    "persons": "json_dumps/persons__denorm.json",
    "places": "json_dumps/places__denorm.json",
    "lit": "json_dumps/literary_works__denorm.json",
    "org": "json_dumps/organizations__denorm.json",
    "eve": "json_dumps/events__denorm.json"
}
# create TEI/XML
listperson = make_xml(data["persons"], "amp-index-persons", "gnd", "persons")
listplace = make_xml(data["places"], "amp-index-places", "geonames_id", "places")
listorg = make_xml(data["org"], "amp-index-organizations", "wikidata", "orgs")
listbibl = make_xml(data["lit"], "amp-index-works", "is_linked_with", "bibl")
listbibl = make_xml(data["eve"], "amp-index-events", "wikidata", "events")
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
