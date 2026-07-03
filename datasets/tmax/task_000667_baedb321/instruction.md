You are acting as a bioinformatics analyst and systems engineer. We have a multi-service sequence processing pipeline that is currently misconfigured, and we need a custom Rust-based sequence filter to protect downstream systems from synthetic anomalous sequences (our "evil" corpus) while allowing natural sequences ("clean" corpus) through.

### Environment Setup & Multi-Service Compose
Our pipeline relies on three interconnected services located in `/app/services/`:
1. **Redis (Port 6379):** Stores essential motif substitution matrices. 
2. **Sequence Provider (Flask, Port 5000):** Exposes metadata about reference genomes.
3. **Result Aggregator (Express, Port 3000):** A webhook receiver that logs anomalies.

First, you must fix the startup script `/app/start_services.sh`. It currently attempts to start these services but has incorrect port bindings and environment variables. Adjust the script so that:
- Redis binds to `127.0.0.1:6379`.
- The Sequence Provider (Flask) is given the environment variable `REDIS_HOST=127.0.0.1` and binds to port `5000`.
- The Result Aggregator is started on port `3000`.
Verify they are all running and communicating.

### The Rust Sequence Filter
Next, you must write a Rust-based sequence classifier in `/home/user/sequence_filter/`. You can initialize a new cargo project here.

The classifier must be a command-line tool with the following signature:
`cargo run --release -- <input_dir> <output_dir>`

**Algorithm Requirements:**
1. Read all `.fasta` files from `<input_dir>`.
2. For each sequence, compute a 2D k-mer frequency matrix (using k=3, yielding a 64x64 matrix mapping adjacent 3-mers).
3. **Iterative Refinement (Convergence):** Apply a Markov transition smoothing step to the matrix. Multiply the matrix by the base substitution weights fetched from Redis (key: `substitution_weights`, a JSON array of floats). Repeat this smoothing iteration until the maximum cell value change between iterations is strictly less than `1e-4` (convergence test).
4. **Analytical Validation:** Calculate the dominant eigenvalue or the simple matrix trace (sum of the diagonal) of the converged matrix. Compare it to the analytical baseline exposed at `http://127.0.0.1:5000/baseline_score`.
5. **Classification:** If the sequence's smoothed trace is mathematically divergent (greater than 1.5x the baseline score), classify the sequence as **"evil"** (synthetic/anomalous). Otherwise, classify it as **"clean"**.
6. **Action:** The program must write the original `.fasta` file to `<output_dir>` ONLY if it is classified as "clean". Do not copy evil sequences. For every sequence classified as evil, send a POST request with the filename to `http://127.0.0.1:3000/flag`.

### Verification Corpora
We have provided two directories containing test sequences:
- `/app/corpora/clean/`: Contains strictly natural, benign sequences.
- `/app/corpora/evil/`: Contains synthetically engineered anomalous sequences.

Your tool will be tested automatically. To pass, your Rust binary must achieve a 100% success rate:
- **100% of the files in `/app/corpora/clean/` must be written to the output directory.**
- **100% of the files in `/app/corpora/evil/` must be rejected (not written to the output directory), and reported to the aggregator.**

Create a final execution log at `/home/user/verification.log` detailing how many files were processed, accepted, and rejected.