You are an AI assistant helping a machine learning engineer prepare a training data pipeline. 

We have a microservice that generates deterministic L2-normalized embeddings for entities. Currently, it's acting like a broken plotting script—producing "blank" or zeroed-out embeddings instead of actual normalized floats, and the API gateway isn't even connecting to it.

The pipeline consists of two services:
1. An Nginx reverse proxy (intended to run on port 8080).
2. A custom C backend server (intended to run on port 9000).

Your tasks are:
1. **Fix the API Gateway**: Edit `/app/nginx.conf` so that HTTP requests to Nginx on port `8080` correctly proxy to the C backend on `127.0.0.1:9000`. Ensure Nginx runs using this config.
2. **Fix the C Backend**: The C source code is at `/app/server.c`. There is a numerical accuracy bug in the `normalize_embedding` function causing the embeddings to lose precision or zero out (truncation/type error). Fix the mathematical bug so the schema enforcement of returning proper 32-bit floating point arrays holds.
3. **Compile and Start**: Compile the C backend (`gcc /app/server.c -lm -o /app/server`) and start both the Nginx service (using `/app/nginx.conf`) and the C server in the background.

When correctly configured, sending a request like `curl "http://127.0.0.1:8080/embed?id=5"` should return a JSON response containing a properly L2-normalized float array.

Leave the services running in the background. Do not alter the HTTP JSON response format in the C code, only fix the mathematical bug and Nginx routing.