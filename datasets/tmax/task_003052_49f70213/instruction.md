You are an AI assistant helping a bioinformatics researcher organize and analyze a dataset of biological interactions. 

The researcher has a dataset of biological relationships in a CSV file located at `/home/user/interactions.csv`. The CSV has no header and contains the following columns:
`source_entity`, `source_type`, `relation`, `target_entity`, `target_type`

Your task is to write a Python script at `/home/user/kg_analyzer.py` that processes this data and performs knowledge graph pattern matching.

The script must meet the following requirements:
1. It should accept a single command-line argument: the name of a Disease.
2. It must create a local SQLite database at `/home/user/kg.db`.
3. It must reverse-engineer the flat CSV data into a proper graph data model inside SQLite. Specifically, create a `nodes` table (with entity names and their types) and an `edges` table (with source, target, and relation types).
4. You must design and implement an index strategy on these tables to optimize multi-hop path traversal queries.
5. The script must parse `/home/user/interactions.csv` and populate the database.
6. Using a securely parameterized SQL query, find all "Drug" entities that have a "targets" relation to a "Gene", where that same "Gene" has an "associated_with" relation to the Disease provided as the command-line argument.
7. The script must output the matching Drug names, one per line, sorted alphabetically, to a file named `/home/user/treatment_candidates.txt`.

Ensure your script handles the creation of the database, table schema, indexes, data insertion, and querying. Run your script using the argument `"Asthma"` to generate the final output file.