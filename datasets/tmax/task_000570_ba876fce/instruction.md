You are a database administrator tasked with optimizing and securing a custom graph database querying system. Recently, there have been performance degradation issues due to unbounded graph traversal queries and missing schema validations. The lead engineer left a voice memo detailing the new security constraints that must be implemented, but they are currently offline.

Your objectives are:
1. **Extract Constraints:** An audio memo is located at `/app/dba_notes.wav`. You must transcribe this audio (a transcription tool like `whisper-cli` or `ffmpeg` pipeline is available in your environment) to discover the exact graph traversal limits and the required output schema fields that every query must include.

2. **Implement Query Sanitizer:** Write a C program at `/home/user/query_sanitizer.c` and compile it to `/home/user/query_sanitizer`. This tool must act as a filter for our graph query pipeline. 
   - The tool must read a query file path as its first command-line argument.
   - The queries are formatted in a custom text-based query structure. For example:
     ```
     MATCH (n:User)-[r:KNOWS*1..3]->(m:User)
     WHERE n.id = ?
     RETURN m.id, m.name
     ```
   - Your C program must parse the `MATCH` traversal depths (e.g., `*1..3`) and the `RETURN` output schema.
   - It must enforce the constraints you extracted from the audio file.
   - It must exit with code `0` if the query is safe and meets all schema requirements.
   - It must exit with code `1` (or higher) and print an error message to `stderr` if the query is malicious, unbounded, exceeds the depth limit, or fails output schema validation.

3. **Validate Against Corpus:** The security team has provided a test suite of queries:
   - `/app/corpus/clean/`: Contains safe, optimized graph queries that your tool MUST accept (exit code 0).
   - `/app/corpus/evil/`: Contains malicious queries (unbounded traversals like `*1..`, deep traversals exceeding the limit, missing schema fields, or injection patterns) that your tool MUST reject (exit non-zero).

Ensure your C program is robust enough to handle the exact strings and patterns found in the corpora. You may write additional shell scripts to help automate testing your binary against the corpora. Your final compiled binary must be located exactly at `/home/user/query_sanitizer`.