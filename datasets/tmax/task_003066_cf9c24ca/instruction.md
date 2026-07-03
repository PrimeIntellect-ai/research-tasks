You are assisting a researcher who is organizing a large network dataset of biological interactions. The researcher left an audio voice note specifying which two specific proteins (nodes) need to be queried for the shortest interaction path. 

Your task is to:
1. **Transcribe** the audio file located at `/app/voice_query.wav` to identify the starting and ending node IDs. (You may use `whisper` or Python libraries like `openai-whisper` or `SpeechRecognition` if you install them, but the final querying tool must be written in C).
2. **Optimize the query program:** The researcher has provided a dataset `/app/interactions.csv` (format: `source_node,target_node,weight`). They wrote a naive C program at `/app/naive_query.c` that finds the shortest path, but it is incredibly slow because it scans the CSV file from disk for every node expansion instead of building an in-memory index.
3. Write a new, optimized C program at `/home/user/fast_query.c` that:
   - Takes the start and end nodes as command-line arguments (parameterized query construction).
   - Reads `/app/interactions.csv` exactly once to build an efficient in-memory adjacency list (index strategy design).
   - Computes the shortest path using an efficient graph traversal (e.g., Dijkstra's algorithm).
   - Outputs the result to standard output strictly matching this JSON schema: `{"start": INT, "end": INT, "path": [INT, INT, ...], "total_weight": FLOAT}`
4. **Create a pipeline:** Write a shell script at `/home/user/run_pipeline.sh` that extracts the node IDs from your transcription, compiles `/home/user/fast_query.c`, runs it with the extracted IDs, and saves the final JSON output to `/home/user/final_result.json`.

The dataset is large, so your C program must be highly optimized. Your solution will be evaluated based on the execution speed of the C program compared to a threshold, as well as the strict correctness of the JSON output schema.