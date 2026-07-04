You are assisting a researcher in organizing and securing their dataset querying pipelines. The lab uses a NoSQL document database that also supports graph projection queries. The researcher has left an audio memo detailing the strict schema and security rules for any queries executed against the lab's dataset.

Your task is to write a C-based query sanitizer that filters NoSQL aggregation pipelines and graph projections submitted by various lab members, rejecting malicious or malformed queries while allowing valid ones.

Step 1: Retrieve the requirements
An audio memo is located at `/app/research_log.wav`. You must transcribe or listen to this audio file to understand the specific rules the researcher has set for the NoSQL queries. (You may use available command-line tools or write a quick script to transcribe it).
The audio will specify:
- Allowed and forbidden graph node labels / collections.
- Rules regarding parameterized query construction (preventing NoSQL injection).
- Required output schema validation fields.

Step 2: Build the Sanitizer
Write a C program at `/home/user/sanitizer.c`. 
- It must take a single command-line argument: the path to a JSON file containing a NoSQL/Graph query payload.
- It must parse the JSON. (A copy of the `cJSON` library is available at `/opt/cJSON/cJSON.h` and `/opt/cJSON/cJSON.c`. You can compile it alongside your code).
- It must evaluate the query against the rules extracted from the audio memo.
- If the query satisfies all rules (clean), the program must exit with status code `0`.
- If the query violates any rule (evil), the program must exit with a non-zero status code (e.g., `1`).

Compile your program to the executable `/home/user/sanitize_query`.

Step 3: Verification
The lab has provided a training corpus of queries to test your sanitizer.
- Clean queries: `/app/corpus/clean/`
- Evil/Malicious queries: `/app/corpus/evil/`

Your compiled `/home/user/sanitize_query` program must perfectly distinguish between the two corpora. It will be invoked via `"/home/user/sanitize_query <file_path>"` for every file in both directories.