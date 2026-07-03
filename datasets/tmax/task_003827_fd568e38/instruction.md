You are assisting a researcher who is organizing a dataset of academic papers, authors, and institutions to be ingested into a graph database. The researcher needs a C program to validate the dataset against a graph schema and generate Cypher queries for the valid entries.

You have been provided with two files (you will need to assume they exist or write a script to simulate them if testing locally, but expect them at `/home/user/schema.txt` and `/home/user/dataset.csv` in the environment):

1. **`/home/user/schema.txt`** defines the valid node types and directed relationship types.
```text
Nodes: Paper, Author, Institution
Edges:
Paper -> CITES -> Paper
Author -> WROTE -> Paper
Author -> AFFILIATED_WITH -> Institution
```

2. **`/home/user/dataset.csv`** contains the raw relationship data in the format: `SourceID,SourceType,TargetID,TargetType,RelType`. 
Example: `P1,Paper,P2,Paper,CITES`

Your task is to write a C program, saved at `/home/user/graph_parser.c`, and compile it to `/home/user/graph_parser`. The program must take two arguments: the path to the dataset and the path to the schema.
Example: `./graph_parser /home/user/dataset.csv /home/user/schema.txt`

The program must perform the following:
1. **Schema Validation**: For each line in the dataset, verify that both node types are valid, the relationship type is valid, and the specific directed relationship (SourceType -> RelType -> TargetType) exactly matches an edge rule in `schema.txt`.
2. **Cypher Generation**: For every valid row, output a single Cypher query to a file named `/home/user/queries.cypher` in the exact following format:
   `MERGE (a:SourceType {id: 'SourceID'})-[:RelType]->(b:TargetType {id: 'TargetID'});`
3. **Invalid Row Logging**: For every row that violates the schema (invalid node type, invalid relationship, or wrong types for a relationship), append the exact raw line (without a trailing newline if it's the last line, but typical CSV lines have newlines) to `/home/user/invalid_rows.log`.

Requirements:
- Ensure the output in `/home/user/queries.cypher` maintains the exact same order as the valid rows in the CSV.
- Ensure the output in `/home/user/invalid_rows.log` maintains the exact same order as the invalid rows in the CSV.
- Use strict exact string matching for validation.

Compile the code and run it against the provided dataset. Provide the bash commands you used.