You are an AI assistant helping a data researcher organize and query a large network of interlinked research datasets.

The researcher has left a SQLite database of dataset metadata and their dependency graph at `/app/research_data.db`. 
The database has two tables:
1. `datasets` (id INTEGER PRIMARY KEY, name TEXT, tag TEXT)
2. `lineage` (source_id INTEGER, target_id INTEGER) - represents a directed dependency from `source_id` to `target_id`.

The researcher also left a voice memo at `/app/instructions.wav`. This audio file dictates two critical parameters for the query tool:
1. A specific `tag` that marks datasets as strictly invalid (they must be filtered out).
2. A strictly enforced `page_size` for result pagination.

Your task is to:
1. Extract the hidden rules (the excluded tag and the page size) from the voice memo `/app/instructions.wav`. You may install tools like `openai-whisper` or `ffmpeg` to transcribe or listen to it.
2. Write a Python script at `/home/user/query_graph.py` that explores this knowledge graph using complex SQL joins or Recursive CTEs. 

The script MUST have the following command-line signature:
`python /home/user/query_graph.py <start_id> <max_depth> <page_number>`

Behavioral requirements for `query_graph.py`:
- Accept `<start_id>` (integer), `<max_depth>` (integer), and `<page_number>` (integer, 1-indexed).
- Find all descendant dataset IDs reachable from `<start_id>` through the `lineage` table (following directed edges from source to target) up to `<max_depth>` hops away. (A depth of 0 should only consider the `start_id` itself, depth 1 includes its immediate targets, etc.)
- Exclude any dataset (both from being traversed through AND from the final results) if its `tag` matches the excluded tag mentioned in the audio.
- From the valid reachable datasets (including the start node if it's valid), sort their IDs in strictly ASCENDING order.
- Paginate the sorted IDs using the `<page_number>` and the `page_size` specified in the audio file.
- Print the final IDs for that page as a single comma-separated string on standard output (e.g., `42,45,49`). If the page is empty, print nothing or an empty string.

Ensure your script operates entirely on the database using efficient SQL queries (like Recursive CTEs) where possible, rather than pulling all data into memory.