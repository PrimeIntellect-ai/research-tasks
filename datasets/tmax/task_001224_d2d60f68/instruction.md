You are tasked with building a reproducible audio processing and embedding retrieval pipeline in C and bash for preparing machine learning training data. 

We have a dataset of raw audio clips, and for this task, you will work with a single fixture located at `/app/fixture.wav`. 

Your goal is to:
1. **Audio Feature Extraction**: Write a C program `extract_features.c` that reads the raw WAV file (assuming 16-bit PCM, mono, 16kHz) and computes a simple 4-dimensional "embedding" vector for the entire file. For simplicity, the 4 dimensions should be:
   - Average amplitude (absolute value)
   - Maximum amplitude
   - Zero-crossing rate (number of sign changes per sample)
   - Root Mean Square (RMS) energy
2. **Reproducibility & Tracking**: Write a bash script `run_pipeline.sh` that compiles the C code, runs it on `/app/fixture.wav`, and saves the resulting 4D vector to a text file `experiment_results.txt`. The script should ensure reproducibility by checking the hash of the compiled binary and logging it.
3. **Embedding Retrieval Service**: Write a C program `embedding_server.c` that loads the 4D embedding from `experiment_results.txt` and starts a TCP server listening on `127.0.0.1:8080`. 
   - The server must accept incoming TCP connections.
   - When a client sends a 4D query vector (as a comma-separated string of floats, e.g., "0.1,0.2,0.3,0.4\n"), the server should compute the Euclidean distance between the query and the extracted embedding.
   - The server should respond with the calculated distance formatted as a string (e.g., "Distance: 1.2345\n") and then close the connection.

Please implement the C code using only standard C libraries and system calls. Run `run_pipeline.sh` to generate the embedding, and then start the `embedding_server` in the background. Leave the server running.