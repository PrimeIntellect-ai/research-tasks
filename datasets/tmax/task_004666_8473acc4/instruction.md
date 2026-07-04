You are a bioinformatics analyst tasked with setting up a statistical sequence analysis pipeline. The pipeline calculates a numerical derivative of smoothed GC-content across DNA sequences.

There are two main objectives: 
1. Fix the multi-service pipeline integration.
2. Implement the statistical analysis engine in Go.

### Part 1: Service Integration
In `/app/`, there is a multi-service workflow consisting of:
- A Redis server (message queue).
- A Sequence Emitter (`/app/emitter/emitter.py`) which generates random DNA sequences and pushes them to a Redis list named `dna_jobs`.
- A Webhook Listener (`/app/webhook/listener.py`) which expects POST requests containing the processed sequence scores.

The services are started via `/app/start_services.sh`. However, the configuration is broken. 
- The Emitter is currently configured to connect to a redis host named `redis_db` on port 6380, but Redis is actually running on `127.0.0.1:6379`. Modify `/app/emitter/config.env` to point to the correct Redis host and port.
- The Webhook Listener currently binds to port 5000, but the overall system expects it on port 8081. Modify `/app/webhook/listener.py` to listen on port 8081.
- You must create a bash script at `/home/user/worker.sh` that acts as the glue: it should continuously pop tasks from the Redis list `dna_jobs` (using `redis-cli`), pass the sequence to your Go program (see Part 2), and `curl POST` the resulting string to `http://127.0.0.1:8081/results`.

### Part 2: Statistical Analysis Engine (Go)
Write a Go program at `/home/user/analyze.go` and compile it to `/home/user/analyze`.
It must take exactly one command-line argument: a string representing a DNA sequence (e.g., `ATGC...`).
It must print a space-separated list of floating-point numbers (formatted to 2 decimal places, e.g., `0.25 -0.12 0.00`) to standard output.

**Algorithm:**
1. Map the DNA characters to a numerical array $X$: `G` and `C` = 1.0, `A` and `T` = 0.0.
2. Smooth the array using a 3-element discrete filter with weights `[0.25, 0.5, 0.25]`. For a sequence of length $L$, the smoothed array $S$ has length $L$.
   $S[i] = 0.25 \cdot X[i-1] + 0.5 \cdot X[i] + 0.25 \cdot X[i+1]$
   *(Treat out-of-bounds indices of $X$ as having a value of 0.0)*.
3. Calculate the numerical derivative using central difference: 
   $D[i] = (S[i+1] - S[i-1]) / 2.0$
4. Output the array $D$ for indices $i = 1$ to $L-2$. (So if the input string has length $L$, the output has length $L-2$).

You are provided with a compiled reference oracle at `/opt/oracle/analyze_oracle`. Your Go program's output must be **bit-exact equivalent** to this oracle for any valid DNA sequence. You can use the oracle to test your implementation and perform regression testing.

Ensure the services are running and your `worker.sh` is processing jobs.