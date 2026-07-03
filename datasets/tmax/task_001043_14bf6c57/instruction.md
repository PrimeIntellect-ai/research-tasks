You are a data engineer building an ETL pipeline to extract and validate a Bill of Materials (BOM) for a manufacturing system. 

The source data is in an SQLite database located at `/home/user/bom.db`. It contains two tables:
- `components (part_id TEXT PRIMARY KEY, name TEXT, category TEXT)`
- `assembly (parent_id TEXT, child_id TEXT)`

**The Problem:**
Due to a known storage fault, the index `idx_assembly_parent` on the `assembly` table is corrupted and occasionally returns stale or missing rows when queried directly with `WHERE parent_id = ?`. To bypass this, you have decided to extract the full tables (which bypasses the corrupted index) and load them into an in-memory Graph database to perform the hierarchical querying.

**Your Objectives:**
1. Write a Python script to extract all records from `components` and `assembly`. 
2. Construct an in-memory RDF graph using the `rdflib` Python library. 
   - Use the namespace `http://example.org/bom/` for all entities.
   - Represent components as URIs (e.g., `http://example.org/bom/PROD-001`).
   - Represent assembly relationships using the predicate `http://example.org/bom/hasChild`.
   - Add the `name` and `category` as literals using custom predicates `http://example.org/bom/name` and `http://example.org/bom/category`.
3. Execute a **SPARQL query** against this RDF graph to find *all* transitive dependencies (children, grandchildren, etc.) of the root part `"PROD-001"`. 
4. For each transitive dependency found, determine if it is a "leaf" node (meaning it has no children of its own).
5. Format the extracted dependencies into a list of dictionaries and validate them against the following output schema requirements:
   - `part_id`: string
   - `name`: string
   - `category`: string
   - `is_leaf`: boolean
6. Write the validated output as a JSON array of objects to `/home/user/final_bom.json`. The array must be sorted alphabetically by `part_id`.

*Note: You may install any necessary Python packages (like `rdflib`, `pydantic`, or `jsonschema`) using pip.*