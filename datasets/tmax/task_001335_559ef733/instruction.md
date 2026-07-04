I am a researcher organizing a large, multi-modal dataset of research records. The records contain both unstructured document metadata and structured knowledge graph mappings. Unfortunately, our data ingestion pipeline was corrupted, and many records now contain invalid cross-representation mappings or logical anomalies (such as circular relationships). 

I need you to build a robust data validation tool to filter out the corrupted ("evil") records from the valid ("clean") ones. 

Here is what you need to do:

1. **Fix the Vendored Graph Library**:
   We use a local Rust library for graph querying called `graph-mapper` located at `/app/vendored/graph-mapper`. However, the previous maintainer made a mistake, and it currently fails to compile. Identify and fix the perturbation in the library (hint: check its dependencies and build configuration).

2. **Create the Validator CLI**:
   Create a new Rust executable project at `/home/user/record-validator`. It must depend on the local `graph-mapper` crate.
   Your CLI should accept a single directory path as an argument.
   Example invocation: `cargo run --release -- /app/data/clean_corpus`

3. **Validation Logic**:
   The CLI must read every `.json` file in the provided directory. Each file has this schema:
   ```json
   {
     "document": {
       "doc_id": "string",
       "dataset_refs": ["string", "string"]
     },
     "graph": {
       "nodes": [
         {"id": "string", "type": "string"}
       ],
       "edges": [
         {"source": "string", "target": "string", "relation": "string"}
       ]
     }
   }
   ```
   A record is considered **VALID** (clean) if and only if **all** the following conditions are met:
   - The knowledge graph (defined by `graph.nodes` and `graph.edges`) contains **no directed cycles**.
   - The `document.doc_id` exists as a node in the graph with the exact type `"Document"`.
   - Every ID listed in `document.dataset_refs` exists as a node in the graph with the exact type `"Dataset"`.
   - For every ID in `document.dataset_refs`, there is a valid directed path in the graph from the `"Document"` node to that `"Dataset"` node.

   If a record violates *any* of these rules, it is considered **INVALID** (evil).

4. **Output Format**:
   For every file processed in the directory, your program must print exactly one line to `stdout` in the following format:
   `ACCEPT <filename>` (if valid)
   `REJECT <filename>` (if invalid)
   Where `<filename>` is just the base name of the file (e.g., `record_01.json`).

Please ensure your tool is completely accurate. I have test datasets at `/app/data/clean_corpus` and `/app/data/evil_corpus`. Your tool must accept all clean records and reject all evil records.