You are an operations engineer triaging a severe incident. Downstream financial reporting services are occasionally failing due to massive floating-point inaccuracies originating from a legacy C-based microservice binary.

We have a stripped legacy binary located at `/app/legacy_aggregator`. It accepts a sequence of floating-point numbers via `stdin` (one per line) and prints their sum to `stdout`. 

We have isolated a time window where the inaccuracies occurred. The transaction data during this window is fragmented across three different service logs:
1. `/data/gateway.log`
2. `/data/queue.log`
3. `/data/aggregator_node.log`

Each log contains partial information (timestamps, transaction IDs, and fragmented numeric payloads). 

Your task consists of three parts:

**Part 1: Log Timeline Reconstruction**
Correlate the logs across the three services to reconstruct the full sequence of inputs for each transaction. Extract the values in chronological order based on the log timestamps. Create a minimal reproducible dataset of these failed transactions at `/home/user/reconstructed_inputs.csv` with the format:
`transaction_id,val1,val2,val3,...`

**Part 2: Root Cause Analysis & MRE**
By analyzing the reconstructed inputs and feeding them into `/app/legacy_aggregator`, deduce the root cause of the floating-point precision loss. (Hint: inspect the distributions of the numbers and how the legacy binary processes them).

**Part 3: Floating-Point Precision Repair**
You cannot recompile the legacy binary, but you can build a wrapper around it. Create an executable script at `/home/user/safe_aggregator.sh`. 
- It must take a single argument: the path to a file containing one floating-point number per line.
- It must preprocess the numbers and pipe them into `/app/legacy_aggregator` in a way that minimizes the floating-point precision loss (catastrophic cancellation/accumulation errors).
- It must output only the final aggregated number to `stdout`.

An automated verifier will test your `/home/user/safe_aggregator.sh` against a held-out test set of highly skewed floating-point numbers. The verifier will compare your script's output to a high-precision 64-bit float baseline. Your solution will be evaluated based on the absolute error.