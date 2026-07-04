You are a database administrator tasked with optimizing queries and processing an exported NoSQL graph dataset. The data represents a large social dependency graph, but the raw export has been poisoned with corrupted records and NoSQL injection attempts.

Your objective is to build a C++ data sanitizer, process the raw graph data, and extract a specific cluster of interest.

Here are your instructions:

1. **Identify the Target Cluster:**
   You have been provided with an image file at `/app/cluster_target.png` containing the DBA team's target cluster ID. Use OCR tools (like `tesseract`) to extract this specific cluster ID.

2. **Build the C++ Data Sanitizer:**
   Write a C++ program that reads JSON-lines (JSONL) data from standard input (stdin) and writes valid, sanitized JSON-lines to standard output (stdout). Compile it to `/home/user/sanitizer`. 
   
   A line is considered **"clean"** and must be preserved if it meets ALL the following criteria:
   * It is a valid JSON object.
   * The `page_rank` numeric field is >= 0 (not negative).
   * Inside the `properties` sub-object, NO keys start with the `$` character (this is to prevent NoSQL operator injection in downstream systems).
   
   If a line violates any of these rules, it is considered **"evil"** and must be completely omitted from the output.

   *Note: To assist with testing your sanitizer, two directories are provided:*
   * `/app/clean/`: Contains individual valid JSON-line files. Your sanitizer must output these exactly as they are.
   * `/app/evil/`: Contains individual invalid JSON-line files. Your sanitizer must output absolutely nothing when fed these.

3. **Process the Raw Export:**
   You have a raw, unprocessed graph export at `/app/raw_graph_export.jsonl`. Use your compiled `/home/user/sanitizer` to clean this file.

4. **Extract Target Cluster Nodes:**
   From the *cleaned* output, filter out all records except those belonging to the cluster ID you extracted from `/app/cluster_target.png` in Step 1 (the cluster ID is located in the `cluster_id` field of the JSON).

5. **Format Conversion:**
   Export the final filtered target nodes to a CSV file at `/home/user/final_target_nodes.csv`. The CSV must have exactly this header and format:
   `node_id,page_rank,cluster_id`
   Sort the CSV rows by `node_id` in ascending alphabetical order.