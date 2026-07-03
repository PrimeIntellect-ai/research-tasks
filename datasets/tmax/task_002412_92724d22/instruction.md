You are a bioinformatics analyst tasked with building a scalable sequence-filtering pipeline. Your goal is to identify and filter out sequencing artifacts (specifically, adapter read-through contamination) from DNA sequence data. 

We have a multi-service architecture located in `/app/` that consists of Nginx, Redis, and three Go worker services. The system is currently broken and incomplete. You need to fix the service configurations, implement the filtering logic in Go, and ensure the pipeline accurately separates clean sequences from contaminated ones.

### 1. Multi-Service Configuration
The setup script `/app/start.sh` starts Nginx, Redis, and three Go instances, but they are not wired correctly.
- Fix `/app/nginx/nginx.conf` so that Nginx listens on port 8080 and load-balances incoming HTTP requests to the three Go worker instances running on `127.0.0.1:8081`, `127.0.0.1:8082`, and `127.0.0.1:8083`.
- Ensure the Go worker `/app/worker/main.go` correctly connects to the local Redis instance on `127.0.0.1:6379` (no password).

### 2. Sequence Analysis and Filtering Logic
In `/app/worker/analyzer.go`, implement the `AnalyzeSequence(seq string) string` function to classify sequences. A sequence is passed as a string of A, C, G, T characters. You must return either `"clean"` or `"evil"`.

To detect adapter read-through contamination, perform the following analysis:
1. **Windowed GC Content**: Divide the sequence into non-overlapping sliding windows of exactly 20 bases. Discard any remaining bases at the end that don't make a full window.
2. **Calculate GC Ratio**: For each window, calculate the GC ratio (number of 'G' and 'C' bases divided by 20).
3. **Curve Fitting and Regression**: Fit a simple linear regression `y = mx + c` where `x` is the window index (0, 1, 2, ...) and `y` is the GC ratio for that window.
4. **Statistical Comparison**: Calculate the R-squared ($R^2$) value of the linear fit to determine how well the GC content follows a linear trend (which indicates adapter contamination gradually dominating the read).
   - If $R^2 \ge 0.60$, the sequence exhibits a significant trend and is considered contaminated. Return `"evil"`.
   - Otherwise, the sequence is considered biological. Return `"clean"`.

*Hint*: You will need to implement basic linear regression and $R^2$ calculation from scratch in Go, as no external math libraries are provided. 

### 3. Concurrency
Update the handler in `/app/worker/main.go` to process incoming JSON POST requests (`{"sequence": "ATGC..."}`) at the `/analyze` endpoint. Use Go routines to allow the worker to handle multiple requests concurrently without blocking. Wait for the analysis, cache the result in Redis with the sequence as the key and the result as the value, and return an HTTP 200 JSON response `{"status": "<result>"}`.

### Verification
The verification script will exercise the entire flow by sending sequences to the Nginx endpoint at `http://127.0.0.1:8080/analyze`.
It will test your system against two corpora:
- Clean sequences: Normal biological reads with stable GC content.
- Evil sequences: Reads containing severe adapter read-through, showing strong linear GC gradients.

You must achieve a 100% pass rate: all clean sequences must be classified as `"clean"`, and all evil sequences must be classified as `"evil"`.

Once you have completed the implementation and updated the configurations, ensure all services are running by executing `/app/start.sh`. Leave the services running for verification.