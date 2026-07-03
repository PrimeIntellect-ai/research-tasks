You are an MLOps engineer responsible for tracking experiment artifacts and performance metrics. We need a lightweight, standalone C-based metric server that calculates basic statistics and Bayesian updates from our latest inference run, and exposes them via a simple HTTP API.

You must write and run a C program at `/home/user/metric_server.c` (compiled to `/home/user/server`) that does the following:

1. **Multi-Source Data Processing:**
   - Read the historical inference metrics from `/app/data/historical_metrics.csv`. This file has a header and three columns: `run_id`, `inference_time_ms`, and `accuracy`.
   - Calculate the Pearson correlation coefficient between `inference_time_ms` and `accuracy` across all rows. Let this be `R`.
   - Check the file size of the audio artifact from the latest run located at `/app/audio/eval_sample.wav`. Let this size in bytes be `S`.

2. **Bayesian Inference Update:**
   - We have a prior probability of an optimal deployment: `P(Optimal) = 0.6`.
   - The probability that the output audio artifact exceeds 1,000,000 bytes given an optimal deployment is `P(Large | Optimal) = 0.8`.
   - The probability that the output audio artifact exceeds 1,000,000 bytes given a sub-optimal deployment is `P(Large | ~Optimal) = 0.3`.
   - If the actual file size `S` is greater than 1,000,000 bytes, calculate the posterior probability `P(Optimal | Large)`. If `S <= 1,000,000`, calculate `P(Optimal | ~Large)`. Let this posterior be `P_post`.

3. **HTTP Server (multi_protocol):**
   - The C program must start a TCP socket server listening on `127.0.0.1` port `8080`.
   - It should accept incoming HTTP `GET` requests to the `/metrics` endpoint.
   - For a valid request, it must return an `HTTP/1.1 200 OK` response with a `Content-Type: application/json` header.
   - The response body must be a JSON object with exactly this format:
     `{"correlation": <R>, "posterior": <P_post>, "file_size": <S>}`
   - Format both floating-point numbers (`<R>` and `<P_post>`) to exactly 4 decimal places (e.g., `0.1234` or `-0.9956`). `<S>` should be an integer.

Leave the server running in the background once compiled and executed so the automated verifier can query it. Make sure your C code handles socket creation, binding, listening, accepting, and sending the correct raw HTTP response string.