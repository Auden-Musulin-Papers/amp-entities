from baserow_utils import denormalize_json
from config import (
    MAPPING_PERSONS, MAPPING_PLACES, MAPPING_ORGS,
    MAPPING_RELATIONSHIPS_PERSONS, MAPPING_RELATIONSHIPS_PLACES,
    MAPPING_RELATION_TYPES, MAPPING_LITERARY_WORKS, MAPPING_EVENTS,
    MAPPING_RELATIONSHIPS_EVENTS, MAPPING_RELATIONSHIPS_ORGS,
    MAPPING_RELATIONSHIPS_ORGS_EVENT
)

denormalize_json("literary_works", "json_dumps", MAPPING_LITERARY_WORKS)
denormalize_json("persons", "json_dumps", MAPPING_PERSONS)
denormalize_json("places", "json_dumps", MAPPING_PLACES)
denormalize_json("organizations", "json_dumps", MAPPING_ORGS)
denormalize_json("events", "json_dumps", MAPPING_EVENTS)
denormalize_json("relation_types", "json_dumps", MAPPING_RELATION_TYPES)
denormalize_json("person_person", "json_dumps", MAPPING_RELATIONSHIPS_PERSONS)
denormalize_json("person_place", "json_dumps", MAPPING_RELATIONSHIPS_PLACES)
denormalize_json("person_org", "json_dumps", MAPPING_RELATIONSHIPS_ORGS)
denormalize_json("person_event", "json_dumps", MAPPING_RELATIONSHIPS_EVENTS)
denormalize_json("org_event", "json_dumps", MAPPING_RELATIONSHIPS_ORGS_EVENT)
