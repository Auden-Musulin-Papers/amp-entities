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
    "person_event": "person_event.json",
    "person_place": "person_place.json",
    "literary_work": "literary_works.json",
    "person_place": "person_place.json",
    "person_org": "person_org.json",
}
MAPPING_PLACES = {
    "birth_place": "persons.json",
    "death_place": "persons.json",
    "organizations": "organizations.json",
    "is_part_of": "places.json",
    "person_place": "person_place.json",
    "relation_types": "relation_types.json",
    "events": "events.json",
    "same_as": "places.json",
}
MAPPING_ORGS = {
    "location": "places.json",
    "part_of": "organizations.json",
    "literary_works": "literary_works.json",
    "org_event": "org_event.json",
    "person_org": "person_org.json",
}
MAPPING_EVENTS = {
    "place_of_event": "places.json",
    "person_event": "person_event.json",
    "org_event": "org_event.json",
}
MAPPING_LITERARY_WORKS = {
    "is_written_by": "persons.json",
    "version_of": "literary_works.json",
    "relation_types": "relation_types.json",
    "is_part_of": "literary_works.json",
    "has_publisher": "organizations.json",
}
MAPPING_RELATIONSHIPS_PERSONS = {
    "source": "persons.json",
    "target": "persons.json",
    "relation_type_object": "relation_types.json",
}
MAPPING_RELATIONSHIPS_PLACES = {
    "source": "persons.json",
    "target": "places.json",
    "relation_type_object": "relation_types.json",
}
MAPPING_RELATIONSHIPS_EVENTS = {
    "source": "persons.json",
    "target": "events.json",
    "relation_type_object": "relation_types.json",
}
MAPPING_RELATIONSHIPS_ORGS = {
    "source": "persons.json",
    "target": "organizations.json",
    "relation_type_object": "relation_types.json",
}
MAPPING_RELATIONSHIPS_ORGS_EVENT = {
    "source": "organizations.json",
    "target": "events.json",
    "relation_type_object": "relation_types.json",
}
MAPPING_RELATION_TYPES = {
    "has_broader": "relation_types.json",
    "person_person": "person_person.json",
    "person_place": "person_place.json",
    "person_event": "person_event.json",
    "org_event": "org_event.json",
    "person_org": "person_org.json",
    "literary_works": "literary_works.json",
    "places": "places.json",
}

try:
    br_client = BaseRowClient(
        BASEROW_USER, BASEROW_PW, BASEROW_TOKEN, br_base_url=BASEROW_URL
    )
except KeyError:
    print("Please provide BASEROW_USER, BASEROW_PW, BASEROW_TOKEN in your environment.")
    br_client = None
