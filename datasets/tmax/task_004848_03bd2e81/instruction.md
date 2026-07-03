I am a bioinformatics researcher organizing a dataset of protein-protein interactions. I have exported a dataset from our NoSQL document database into a JSON file located at `/home/user/interactions.json`. 

I need you to write and run a Python script that does the following:
1. Reads the document-oriented data from `/home/user/interactions.json`. The file contains a list of records, where each record has a `"protein"` (string) and `"interacts_with"` (list of strings).
2. Maps this document data into an undirected graph representation.
3. Computes the shortest path from the protein `"MAPK1"` to `"TP53"`.
4. Exports the result to a new JSON file at `/home/user/shortest_path.json`.
5. Validates the output dictionary against the JSON schema provided at `/home/user/schema.json` before saving it. You may need to install the `jsonschema` python package to do this.

The output JSON file (`/home/user/shortest_path.json`) must perfectly match this schema and look exactly like this structure:
```json
{
  "source": "MAPK1",
  "target": "TP53",
  "path": ["MAPK1", "...", "TP53"],
  "distance": 2
}
```
Note: `distance` is the number of edges in the path.

Please create and execute the script to produce the final `/home/user/shortest_path.json` file.