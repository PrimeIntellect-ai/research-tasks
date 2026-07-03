You are a data engineer building an ETL pipeline that processes spoken network logs into a structured graph database. We receive automated voice logs of network connections and need to materialize this into a graph to analyze average latencies.

Your task consists of the following steps:

1. **Audio Transcription**: 
   An audio file containing spoken connection logs is located at `/app/network_log.wav`. The logs follow the pattern: "Node [A] connected to Node [B] with latency [X] milliseconds." 
   Transcribe this audio. You may install and use any CLI tools or Python libraries (like `openai-whisper` or `SpeechRecognition`) to generate a raw text transcript.

2. **Database Insertion (C++)**:
   Write a C++ program at `/home/user/pipeline.cpp`. Your program must:
   - Read the transcribed text.
   - Parse out the Source Node, Target Node, and Latency (integer).
   - Create an SQLite database at `/home/user/network.db` with a table `connections (source TEXT, target TEXT, latency INTEGER)`.
   - Use **parameterized queries** (via the C SQLite3 API) to securely insert the parsed records into the database. Do not use string concatenation for values.

3. **Graph Projection & Export (C++)**:
   Extend your C++ program to project a graph from the relational data.
   - Query the database to find the distinct edges and aggregate the data to calculate the **average latency** for each unique (source, target) pair.
   - Materialize this projected graph and export it to a CSV file at `/home/user/graph_export.csv`.
   - The CSV must have exactly this header: `source,target,avg_latency` and be comma-separated. `avg_latency` should be rounded to the nearest integer.

Compile your C++ program using `g++ /home/user/pipeline.cpp -o /home/user/pipeline -lsqlite3` and run it to produce the final `graph_export.csv`.

**Success Criteria:**
An automated test will compute the Mean Squared Error (MSE) of the `avg_latency` values in your `/home/user/graph_export.csv` against a hidden ground-truth reference file. Your pipeline's output must achieve an MSE of 5.0 or lower.