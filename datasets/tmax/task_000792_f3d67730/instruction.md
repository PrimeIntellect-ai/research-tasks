You are a developer debugging a failing build step in a CI/CD pipeline. 

The build script `/home/user/generate_catalog.py` is supposed to query the local SQLite database `/home/user/catalog.db` to generate a static JSON asset file at `/home/user/catalog_output.json`. 

However, the script is currently crashing. 

Your task is to fix the `generate_catalog.py` script so that it runs successfully and generates the correct `/home/user/catalog_output.json` file. 

The build has the following requirements:
1. The final `catalog_output.json` must ONLY contain products where the `status` is exactly `'active'`.
2. The `meta` field in the output JSON must be a properly parsed JSON object (dictionary), not a string. Some active database records might have serialization anomalies in their metadata column that you will need to handle programmatically in the script.

Do not manually modify the database; you must fix the Python script to handle the data correctly and filter the query results appropriately. Run the script once you have fixed it.