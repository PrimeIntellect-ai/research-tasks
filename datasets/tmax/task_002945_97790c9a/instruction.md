You are a data engineer building a graph ETL pipeline. 

We have received a new set of schema mapping and aggregation rules from the data architects. Curiously, they delivered these rules encoded within an audio artefact located at `/app/schema_instructions.wav`. 

Your task is to:
1. Extract the hidden ETL instructions from the audio file. (Hint: The architects didn't record spoken words; they embedded the text instructions directly into the audio file's standard metadata/comments. Use a tool like `ffprobe` or `ffmpeg` to recover it).
2. Create a Rust project in `/app/etl_pipeline` and write a high-performance CLI program that implements these exact rules.
3. The Rust program must be compiled in release mode. The final executable must be located at `/app/etl_pipeline/target/release/graph_etl`.
4. Your program must read a single JSON payload from standard input (STDIN), perform the graph aggregation according to the rules extracted from the audio, and output the exact canonical JSON string result to standard output (STDOUT).

The input JSON will always have this structure:
```json
{
  "nodes": [
    {"id": "node1", "status": "ACTIVE"},
    {"id": "node2", "status": "INACTIVE"}
  ],
  "edges": [
    {"src": "node1", "dst": "node2", "action": "CONNECT", "val": 10},
    {"src": "node1", "dst": "node2", "action": "DISCONNECT", "val": 5}
  ]
}
```

The output must be a tightly packed JSON string (no unnecessary spaces or newlines) representing the resulting aggregated graph structure as dictated by the hidden rules. 

Your program will be rigorously tested against an automated fuzzer that streams thousands of randomized graph JSONs into your executable and compares your bit-for-bit output against a reference oracle. Ensure your JSON serialization uses standard alphabetical key sorting if utilizing maps, or relies strictly on the requirements given in the hidden rules.