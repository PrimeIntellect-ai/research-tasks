You are a bioinformatics analyst building an automated sequence processing and primer evaluation pipeline. 

We have a multi-service pipeline located in `/app/` that consists of a fast C-based alignment engine, a Redis cache for sequence motifs, and a Python Flask web API that glues everything together.

Currently, the pipeline is broken. Your task is to fix, compile, test, and deploy the services.

1. **Fix and Compile the C Engine**:
   - In `/app/src/`, there is a C program `primer_score.c` designed to calculate the alignment score of a short primer against a target sequence.
   - It currently has a bug in its mismatch penalty logic and fails the regression tests.
   - Run `/app/tests/regression.sh` to see the failures.
   - Fix the C code so that mismatches *subtract* 2 from the score (currently, it adds 2 by mistake). A match adds 1.
   - Compile the engine to `/app/bin/primer_score`.

2. **Configure and Start Redis**:
   - The pipeline requires a Redis server running locally.
   - Start a Redis server on `127.0.0.1:6379`.
   - Use the `redis-cli` to set a key-value pair required by the API: `SET motif_threshold 15`.

3. **Configure and Start the Web Service**:
   - In `/app/service/`, there is a Flask API script `app.py`.
   - Modify `app.py` to ensure it calls the newly compiled `/app/bin/primer_score` (the path is currently hardcoded incorrectly).
   - The API must listen on `0.0.0.0:8080`.
   - Start the Flask app in the background.

The system will be tested by an automated verifier that sends HTTP POST requests to your Flask API on port 8080. Leave the services running. Create a log file at `/home/user/deployment.log` with the word "READY" when you are done.