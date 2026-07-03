You are an AI assistant helping a compliance officer perform a cross-system data audit. The company uses a polyglot persistence architecture, storing different aspects of user data in a relational database, a document store, and a graph database. 

A diagram detailing the schemas, the relationship mapping across these systems, and the specific rules for identifying "non-compliant" user accounts is provided as an image at `/app/compliance_schema.png`.

You have been provided with data exports from the three systems:
1. `/app/users.db`: An SQLite database containing core user records.
2. `/app/profiles.jsonl`: A JSON Lines file containing unstructured profile documents.
3. `/app/activity.ttl`: An RDF file (Turtle format) representing the graph of user actions and resources.

Your task:
1. Analyze the schema diagram and compliance rules in `/app/compliance_schema.png` (you may need to use OCR tools like `tesseract`, which is installed, or write a vision script).
2. Design a strategy to map and join the identities across the three data representations.
3. Write a script (preferably in Python) that queries the relational data, parses the document data, and executes a SPARQL query against the RDF graph to identify all user IDs that meet the non-compliance criteria specified in the image.
4. Optimize your data retrieval and cross-referencing logic so the script can process the data efficiently.
5. Output the final list of non-compliant `user_id`s to `/home/user/non_compliant.txt`, with one ID per line.

Your output will be evaluated against a hidden ground truth using a metric threshold based on the F1 score of your detected user IDs. You must achieve an F1 score of >= 0.95 to pass.