from config import GEONAMES_USER, geonames_to_location


TABLE_ID = "1483"
geonames_to_location(br_table_id=TABLE_ID, user=GEONAMES_USER, field_name_input={"geonames": "geonames_id"}, field_name_update={"coordinates": "geonames_coordinates", "place_type": "place_type", "place_type_class": "place_type_class", "country": "country", "country_code": "country_code"})
