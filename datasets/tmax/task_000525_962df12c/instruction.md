You are helping a researcher organize and audit their data pipelines. We suspect there are "deadlock" cyclical dependencies in how some datasets were derived, meaning a dataset is ultimately marked as being derived from itself through a chain of transformations. 

You have two files in your home directory:
1. `/home/user/derivations.tsv`: A tab-separated file with columns `Source`, `Target`, and `Relation`. This represents a directed graph where `Source` -> `Target` with a specific `Relation`.
2. `/home/user/metadata.tsv`: A tab-separated file with columns `DatasetID`, `ResearcherName`, and `CreationYear`.

Your task is to write a Python script (you can save it as `/home/user/find_deadlocks.py`) that performs the following steps:
1. Parse `/home/user/derivations.tsv` to build a directed graph of dependencies.
2. Find all simple directed cycles of exactly length 3 (e.g., A -> B -> C -> A) where the `Relation` for all edges in the cycle is exactly `"DERIVED_FROM"`. Ignore cycles that involve other relation types like `"CITES"`.
3. For each found cycle, look up the `ResearcherName` for each dataset in the cycle using `/home/user/metadata.tsv`. This acts as a join between your graph query results and the relational metadata.
4. Export the findings to `/home/user/deadlocks.json`.

The output `/home/user/deadlocks.json` must be a JSON array of objects, one for each unique cycle found. Each object must have exactly two keys:
- `"cycle_nodes"`: A strictly sorted list of the dataset IDs in the cycle (lexicographical order).
- `"researchers"`: A strictly sorted list of the unique researcher names responsible for the datasets in this cycle (lexicographical order, no duplicates).

The JSON array itself must be sorted by the first element of `"cycle_nodes"`.

Example of the expected JSON structure:
```json
[
  {
    "cycle_nodes": ["DS1", "DS2", "DS3"],
    "researchers": ["Dr. Smith", "Dr. Vance"]
  }
]
```

Ensure your Python script runs cleanly and produces exactly this output format. Use only standard Python libraries (no external pip packages are pre-installed).