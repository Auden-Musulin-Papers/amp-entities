from baserow_utils import denormalize_json
from config import (MAPPING_PERSONS, MAPPING_PLACES, MAPPING_ORGS,\
    MAPPING_RELATIONSHIPS, MAPPING_RELATION_TYPES, MAPPING_LITERARY_WORKS, MAPPING_EVENTS)


denormalize_json("persons", "json_dumps", MAPPING_PERSONS)
denormalize_json("places", "json_dumps", MAPPING_PLACES)
denormalize_json("organizations", "json_dumps", MAPPING_ORGS)
denormalize_json("relationships", "json_dumps", MAPPING_RELATIONSHIPS)
denormalize_json("relation_types", "json_dumps", MAPPING_RELATION_TYPES)
denormalize_json("literary_works", "json_dumps", MAPPING_LITERARY_WORKS)
denormalize_json("events", "json_dumps", MAPPING_EVENTS)