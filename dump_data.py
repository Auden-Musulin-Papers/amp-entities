from config import br_client, BASEROW_DB_ID

files = br_client.dump_tables_as_json(BASEROW_DB_ID, folder_name="json_dumps")
print(files)
