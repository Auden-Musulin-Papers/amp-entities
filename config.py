import os

from acdh_baserow_pyutils import BaseRowClient


BASEROW_DB_ID = 274
BASEROW_URL = "https://baserow.acdh-dev.oeaw.ac.at/api/"
BASEROW_USER = os.environ.get("BASEROW_USER")
BASEROW_PW = os.environ.get("BASEROW_PW")
BASEROW_TOKEN = os.environ.get("BASEROW_TOKEN")
GEONAMES_USER = os.environ.get("GEONAMES_USER")

MAPPING_PERSONS = {
    "birth_place": "places.json",
    "death_place": "places.json",
    "person_person": "relationships.json",
    "person_person - target": "relationships.json",
    "literary_work": "literary_works.json",
    "events": "events.json"
}
MAPPING_PLACES = {
    "persons": "persons.json",
    "persons - death_place": "persons.json",
    "organizations": "organizations.json",
    "is_part_of": "places.json",
    "relation_types": "relation_types.json",
    "events": "events.json"
}
MAPPING_ORGS = {
    "location": "places.json"
}
MAPPING_RELATIONSHIPS = {
    "source": "persons.json",
    "target": "persons.json",
    "relation_type_object": "relation_types.json"
}
MAPPING_RELATION_TYPES = {
    "has_broader": "relation_types.json",
    "relationships": "relationships.json",
    "literary_works": "literary_works.json",
    "places": "places.json"
}
MAPPING_LITERARY_WORKS = {
    "is_written_by": "persons.json",
    "version_of": "literary_works.json",
    "relation_types": "relation_types.json",
    "is_part_of": "literary_works.json"
}
MAPPING_EVENTS = {
    "participants": "persons.json",
    "place_of_event": "places.json",
    "events_relationships": "events_relationships.json"
}


br_client = BaseRowClient(BASEROW_USER, BASEROW_PW, BASEROW_TOKEN, br_base_url=BASEROW_URL)
