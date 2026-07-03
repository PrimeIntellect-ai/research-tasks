You are a database reliability engineer taking over a complex microservice ecosystem. We are rolling out a new Graph Database to map out our services, databases, and their backup dependencies. Before we integrate this fully, we need a policy validator to ensure that any inserted graph data (representing our backup topology) complies with our security and retention constraints.

Unfortunately, the previous engineer left the topology rules as an image snippet on the server instead of documenting them properly. The image is located at `/app/policy.png`. You can use `tesseract` (which is pre-installed) to read the text from this image.

Your task is to:
1. Extract the backup topology rules from `/app/policy.png`.
2. Write a Python script at `/home/user/validator.py` that takes a single command-line argument: the path to a JSON file containing a serialized subgraph.
3. The script must evaluate the JSON subgraph against the rules extracted from the image.
4. If the subgraph complies with ALL rules, print `VALID` and exit with code `0`.
5. If the subgraph violates ANY rule, print `INVALID` and exit with code `1`.

The JSON files will have the following structure:
```json
{
  "nodes": [
    {"id": 1, "label": "Service", "properties": {"is_global": false}},
    {"id": 2, "label": "Database", "properties": {"region": "us-east"}},
    {"id": 3, "label": "Backup", "properties": {"region": "us-east", "retention_days": 14}}
  ],
  "edges": [
    {"source": 1, "target": 2, "type": "BELONGS_TO"},
    {"source": 2, "target": 3, "type": "BACKUPS_TO"}
  ]
}
```

Write a robust validator that traverses these edges and enforces the graph pattern rules. Your solution will be tested against two sets of graph JSON files: a "clean" set that strictly adheres to the policy and an "evil" set that contains violations. Your script must perfectly separate them.