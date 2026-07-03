You are an ETL Data Engineer responsible for a Knowledge Graph ingestion pipeline. Recently, our downstream Graph Database has been crashing due to a "Cartesian explosion" (similar to a SQL implicit cross join). This is happening because our raw NoSQL JSON payloads occasionally contain wildcards or arrays in their destination node fields, or they attempt to create undocumented relationship types.

Your task is to build a payload validator script that filters out these bad requests before they hit the database. 

First, look at the whiteboard picture stored at `/app/graph_schema.png`. It contains the authoritative schema rules and constraints for our graph model. You will need to reverse engineer the data model and constraints from this image (you may use `tesseract` or similar tools).

Next, write a validator script at `/home/user/filter_payload.py` (you may also use Node.js at `/home/user/filter_payload.js` or a bash script `/home/user/filter_payload.sh`). 

The script must:
1. Accept a single argument: the path to a JSON file containing a NoSQL graph ingestion payload.
2. Read the JSON file. A payload looks like this:
   `{"source": {"label": "User", "id": "u123"}, "relationship": "PURCHASES", "target": {"label": "Product", "id": "p456"}}`
3. Validate the payload against the rules extracted from `/app/graph_schema.png`.
4. Ensure no implicit cross joins can occur: the `target.id` field MUST be a single string, NEVER an array, list, or the wildcard character `*`.
5. Exit with code `0` if the payload is perfectly valid and should be preserved.
6. Exit with code `1` (or any non-zero) if the payload is invalid, violates the schema, or risks a Cartesian explosion (should be rejected).

We will run an automated test that passes hundreds of clean and evil JSON files to your script using the command format:
`<your_script> <path_to_json_file>`

You must successfully accept all valid payloads and reject all invalid/malicious ones to pass.