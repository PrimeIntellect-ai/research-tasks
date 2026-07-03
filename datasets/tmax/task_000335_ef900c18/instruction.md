You are an MLOps engineer tasked with fixing and deploying a custom dimensionality reduction service for our experiment tracking pipeline. 

We have a vendored C library and CLI tool located at `/app/artifact_pca`. It is supposed to take 4D experiment embeddings and project them to 2D for our visualization dashboard. The tool reads from standard input and prints to standard output. 

However, the previous engineer left it broken:
1. **Analysis Environment & Compilation:** The `Makefile` in `/app/artifact_pca` fails to compile the `reducer` executable. Fix the build configuration (hint: it's missing standard library linkage for math functions).
2. **Data Schema Enforcement:** The `reducer.c` file is supposed to enforce a strict schema where lines must exactly match the format `EMBEDDING:<float>,<float>,<float>,<float>`. There is a typo in the C code's format string that causes it to reject perfectly valid float inputs. Find and fix this bug so it correctly parses the four floats.
3. **Service Deployment:** Once you have successfully compiled the `reducer` binary, set up a persistent TCP service listening on `localhost:8888`. You must use standard shell utilities (e.g., `socat` or `ncat`, which are pre-installed) to wrap the `reducer` executable so that any incoming TCP connection to port 8888 executes the tool, feeds the TCP payload to the tool's stdin, and sends the tool's stdout back to the client. Keep this service running in the background.

Your final deliverable is the running TCP service on port 8888 that correctly compiles, parses the embeddings, and applies the dimensionality reduction.