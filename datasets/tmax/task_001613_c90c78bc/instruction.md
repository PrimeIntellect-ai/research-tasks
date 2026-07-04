You are an AI assistant helping a data researcher analyze a custom citation knowledge graph. The researcher has dumped their dataset into two JSONL (JSON Lines) files but hasn't formalized the schema. They need you to write a Rust application to reverse engineer the implicit graph structure, perform a specific pattern matching query, and output the strictly validated results.

**Background & Setup:**
The raw dataset is located at `/home/user/dataset/` and consists of two files:
1. `/home/user/dataset/nodes.jsonl` - Contains entities (Authors). Each line is a JSON object with at least `id`, `type`, and `field` attributes.
2. `/home/user/dataset/edges.jsonl` - Contains relationships. Each line is a JSON object with at least `src` (source node ID), `dst` (destination node ID), and `rel` (relationship type).

**Your Objective:**
1. Initialize a new Rust project named `graph_analyzer` in `/home/user/`.
2. Write a Rust program that reads both JSONL files and constructs an in-memory directed graph.
3. Perform a graph pattern matching query to find all instances of a "Transitive Citation Gap". A Transitive Citation Gap is defined as a sequence of three distinct nodes (X, Y, Z) where:
    *   X, Y, and Z are all of `type` == `"Author"`.
    *   X, Y, and Z all share the exact same `field`.
    *   There is a `"CITES"` edge from X to Y.
    *   There is a `"CITES"` edge from Y to Z.
    *   There is **NO** `"CITES"` edge from X to Z.
    *   X, Y, and Z must be distinct nodes (X != Y, Y != Z, X != Z).
4. The output must be written to `/home/user/results/gaps.json` as a single JSON array of objects. 
5. The output MUST strictly conform to the following JSON schema (which means you must sort the output and format it exactly as specified):
    *   The root is a JSON array.
    *   Each element is an object with exactly three string keys: `"x"`, `"y"`, `"z"`, corresponding to the IDs of the nodes.
    *   The array must be sorted lexicographically by the `"x"` ID. If there are ties, sort by `"y"`, then `"z"`.

**Constraints:**
* Use **Rust** (Cargo is available). You can use any standard crates (e.g., `serde`, `serde_json`) by adding them to your `Cargo.toml`.
* Create the directory `/home/user/results/` if it does not exist before writing the output file.
* Compile your Rust program in release mode (`cargo build --release`) and run it to produce the final `gaps.json` file.
* Do not modify the original dataset files.

Your task is complete when the correctly formatted, sorted JSON file is successfully generated at `/home/user/results/gaps.json`.