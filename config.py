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
    "events_relationships": "relationships_person.json",
    "relationships_place": "relationships_place.json",
    "literary_work": "literary_works.json",
    "events": "events.json",
    "residence": "places.json",
    "workplace": "places.json",
}
MAPPING_PLACES = {
    "birth_place": "persons.json",
    "death_place": "persons.json",
    "organizations": "organizations.json",
    "is_part_of": "places.json",
    "persons_workedin": "persons.json",
    "relationships_place": "places.json",
    "events": "events.json",
    "persons_residence": "persons.json",
    "same_as": "places.json",
}
MAPPING_ORGS = {
    "location": "places.json",
    "part_of": "organizations.json",
}
MAPPING_EVENTS = {
    "participants": "persons.json",
    "place_of_event": "places.json",
    "events_relationships": "events_relationships.json"
}
MAPPING_LITERARY_WORKS = {
    "is_written_by": "persons.json",
    "version_of": "literary_works.json",
    "relation_types": "relation_types.json",
    "is_part_of": "literary_works.json"
}
MAPPING_RELATIONSHIPS_PERSONS = {
    "source": "persons.json",
    "target": "persons.json",
    "relation_type_object": "relation_types.json"
}
MAPPING_RELATIONSHIPS_PLACES = {
    "source": "persons.json",
    "target": "persons.json",
    "relation_type_object": "relation_types.json"
}
MAPPING_RELATIONSHIPS_EVENTS = {
    "person": "persons.json",
    "event": "events.json",
}
MAPPING_RELATION_TYPES = {
    "has_broader": "relation_types.json",
    "relationships_person": "relationships_person.json",
    "relationships_place": "relationships_place.json",
    "literary_works": "literary_works.json",
    "places": "places.json"
}

br_client = BaseRowClient(BASEROW_USER, BASEROW_PW, BASEROW_TOKEN, br_base_url=BASEROW_URL)
