You are assisting a data researcher in organizing a complex dataset lineage tracking system. 

We have an SQLite database at `/app/lineage.db` containing two tables:
- `nodes` (id INTEGER PRIMARY KEY, name TEXT)
- `edges` (source INTEGER, target INTEGER, weight INTEGER)

There are three main objectives to complete:

1. **Audio Transcription & Data Entry**: 
The researcher recorded some recent updates to the lineage graph in an audio file located at `/app/update_notes.wav`. You need to transcribe this audio file (you may install and use tools like `whisper` or `ffmpeg` as needed). The audio dictates several new edges in the format: "Source [X] connects to target [Y] with weight [Z]". Extract these and `INSERT` them into the `/app/lineage.db` `edges` table.

2. **Fixing the Graph Traversal Engine**:
There is a C program located at `/home/user/path_finder.c`. This program is supposed to take two integer arguments (`source_id` and `target_id`) and output the shortest path between them based on the weights. 
Currently, the program attempts to execute a recursive Common Table Expression (CTE) in SQLite to find the shortest path, but the researcher accidentally wrote an implicit cross join in the CTE's recursive step. This causes incorrect results, infinite loops on cyclic graphs, and terrible performance.
You must fix `path_finder.c` so that it:
- Uses a correctly parameterized query to prevent SQL injection (do not use `sprintf` for user input in the query).
- Correctly computes the shortest path using a fixed recursive CTE or by querying the edges and performing Dijkstra's algorithm in C.
- Validates the output schema: it must print *only* a strict JSON array of the node IDs in the shortest path, e.g., `[5, 12, 19, 3]`. If no path exists, print `[]`.

3. **Compilation & Fuzzing Readiness**:
Compile your fixed C program to `/home/user/path_finder`.
The program must be robust. An automated fuzzer will run your executable against a reference oracle binary thousands of times with random `source_id` and `target_id` pairs. It must produce the exact same JSON output as the oracle for every possible input pair.

Provide the final executable at `/home/user/path_finder`. Make sure it only outputs the JSON array to standard output.