You are a data engineer building an ETL pipeline to extract graph data into a structured relational format.

We have a local RDF graph stored in Turtle format at `/home/user/data/network.ttl`.
Your task is to write a Python script `/home/user/extract.py` that queries this graph, aggregates the data, validates the output against a JSON schema, and saves the results.

The script must:
1. Accept an RDF type (like `Person` or `Organization`) as a command-line argument.
2. Construct and execute a parameterized SPARQL query using the `rdflib` library to find all subjects of that specific type (in the `http://example.org/` namespace) and count the number of outgoing `http://example.org/connectedTo` edges they have. 
3. Aggregate the results into a list of dictionaries with the keys `"entity"` (the full URI string) and `"connection_count"` (integer).
4. Validate the resulting JSON array against the schema located at `/home/user/data/schema.json` using the `jsonschema` library.
5. If validation passes, write the JSON array to `/home/user/output_<Type>.json` (e.g., `output_Person.json`), sorted alphabetically by the `"entity"` URI.

Once you have written the script, use it to extract and generate the output files for two types:
- `Person`
- `Organization`

Both `rdflib` and `jsonschema` are available in the Python environment. Ensure the generated JSON files are properly formatted and strictly match the schema.