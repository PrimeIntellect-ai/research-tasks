You are acting as a Database Administrator tasked with optimizing and securing our graph database query pipeline. We have been experiencing performance degradation due to inefficient Cypher queries being submitted by various microservices. 

The Lead DBA has left you an audio recording at `/app/dba_instructions.wav` detailing the specific query patterns that are causing these performance issues (e.g., patterns that cause Cartesian products or unbounded graph traversals).

Your task is to:
1. Transcribe or listen to `/app/dba_instructions.wav` to understand the exact rules for identifying "evil" (inefficient/unsafe) Cypher queries versus "clean" (safe) queries. You may use tools like `whisper-cli`, `ffmpeg`, or Python libraries available or installable in your environment to extract the text.
2. Create a Rust CLI application in `/home/user/cypher_filter`.
3. The Rust application must compile to a binary named `cypher_filter` (e.g., accessible via `cargo run --release -- <file_path>` or directly at `/home/user/cypher_filter/target/release/cypher_filter`).
4. The binary must take exactly one command-line argument: the absolute path to a file containing a Cypher query.
5. The binary must parse or analyze the query and exit with status code `0` if the query is "clean" according to the audio instructions, and exit with status code `1` if the query is "evil".
6. To help you develop and test your logic, two directories of sample Cypher queries are provided:
   - `/app/corpus/clean/`: Contains queries that your program MUST accept (exit 0).
   - `/app/corpus/evil/`: Contains queries that your program MUST reject (exit 1).

Ensure your Rust project is properly initialized, compiles without errors, and strictly adheres to the filtering rules specified in the audio recording. Your solution will be tested against a hidden set of queries in both the clean and evil corpora.