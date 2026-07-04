You are a machine learning engineer preparing a data processing pipeline for a new training dataset. As part of this pipeline, we need a fast C-based TCP server that calculates sentence embeddings and their correlations on the fly. 

We have a proprietary stripped binary located at `/app/embedding_oracle` that generates a 16-dimensional embedding for any given text.

Your task is to implement and start a TCP server in C that listens on `127.0.0.1:9000`. You may need to install standard build tools (like `gcc`).

The server must accept multiple sequential TCP connections (though it only needs to handle one at a time for our tests) and process line-based commands (terminated by `\n`).

### Protocol Specification:

1. **`EMBED <text>`**
   - **Schema Enforcement**: First, validate that `<text>` consists of exactly 8 to 16 alphanumeric characters (a-z, A-Z, 0-9). If it fails this validation, respond exactly with `ERROR_SCHEMA\n`.
   - **Embedding Computation**: If valid, execute the `/app/embedding_oracle <text>` binary. The binary will output exactly 16 space-separated floating-point numbers to standard output.
   - **Storage & Retrieval**: Store this 16-dimensional vector in memory. Assign it a 0-based index (the first valid embedded text is index 0, the next is 1, etc.).
   - **Response**: Respond with `OK <index>\n`.

2. **`CORRELATE <index1> <index2>`**
   - **Correlation Analysis**: Retrieve the embeddings for `index1` and `index2`. Calculate the Pearson correlation coefficient between the two 16-dimensional vectors.
   - **Response**: Respond with the correlation formatted to exactly 4 decimal places, e.g., `0.9231\n` or `-0.1420\n`. If either index does not exist, respond with `ERROR_NOT_FOUND\n`.

3. **`EXIT`**
   - **Response**: Respond with `GOODBYE\n`, close the connection, and continue listening for new connections.

### Requirements:
- Write the server code in C (e.g., save as `server.c`).
- Compile it to `/home/user/server`.
- Run the server in the background so it is listening on port `9000` when your final step completes.
- Ensure the server is robust enough to not crash on invalid commands (just return `ERROR_INVALID\n` for unrecognized commands).

Leave the server running on `127.0.0.1:9000`. Our automated test suite will connect via TCP and issue a series of `EMBED` and `CORRELATE` commands to verify the pipeline's correctness.