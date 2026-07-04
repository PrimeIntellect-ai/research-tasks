I am a researcher organizing a massive, undocumented dataset of academic publications and institutional relationships. The dataset is provided in N-Triples format, but unfortunately, the original ontology/schema documentation was lost. 

I need you to reverse-engineer the data model from the dataset and output a validated schema summarizing what properties belong to what entity types.

The dataset is located at `/home/user/dataset.nt`.

Please write a Rust application to process this dataset. 
Create your Rust project in `/home/user/schema_extractor`. You can use any crates you need (like `regex`, `serde_json`, etc.). 

Your Rust program must do the following:
1. Parse the N-Triples file.
2. Identify the "Type" of every subject. The type is specified by the predicate `<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>`.
3. For every subject that has a defined type, observe all the predicates that are used where this subject is the subject of the triple (including the `type` predicate itself).
4. Aggregate this to reverse-engineer the schema: map each Type URI to a deduplicated, alphabetically sorted list of all Predicate URIs that are ever used by any subject of that Type.
5. Write the result to `/home/user/schema_output.json`.

The output must be a valid JSON object where the keys are the Type URIs (e.g., `http://example.org/Paper`) and the values are arrays of strings representing the Predicate URIs (e.g., `["http://example.org/author", "http://example.org/title", ...]`).

Once you have written the Rust code, compile and run it so that `/home/user/schema_output.json` is generated.