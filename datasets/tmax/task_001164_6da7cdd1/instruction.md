You are assisting a researcher who is organizing datasets and papers. They have created a lightweight knowledge graph stored in an SQLite3 database located at `/home/user/knowledge_graph.db`.

The database contains two tables representing a directed property graph:
1. `nodes` (id INTEGER PRIMARY KEY, type TEXT, name TEXT)
2. `edges` (source INTEGER, target INTEGER, relation TEXT)

The graph contains nodes of types: 'Author', 'Paper', 'Dataset', and 'Topic'.
The relations between them are: 
- Author -> 'authored' -> Paper
- Paper -> 'uses' -> Dataset
- Dataset -> 'tagged' -> Topic

Your task is to write a C program named `/home/user/query_graph.c` that connects to this SQLite database and finds all Authors who have authored a Paper that uses a Dataset tagged with the Topic named "Machine Learning". 

This is equivalent to the Cypher query:
`MATCH (a:Author)-[:authored]->(p:Paper)-[:uses]->(d:Dataset)-[:tagged]->(t:Topic {name: 'Machine Learning'}) RETURN a.name, d.name`

The C program must:
1. Use the `sqlite3` C API to perform the equivalent complex join query.
2. Execute the query and write the results directly to `/home/user/output.csv`.
3. The output must strictly adhere to the following CSV schema validation requirements:
   - The first line must be exactly the header: `Author_Name,Dataset_Name`
   - Following lines must contain the author's name and the dataset's name, separated by a comma.
   - The rows must be ordered alphabetically by `Author_Name` ascending, then `Dataset_Name` ascending.
   - No extra spaces, quotes, or trailing empty lines (except standard Unix newline).

Compile your program to `/home/user/query_graph` and run it so that `/home/user/output.csv` is generated successfully.