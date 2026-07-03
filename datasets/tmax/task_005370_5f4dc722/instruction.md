You are a data engineer tasked with optimizing a critical ETL pipeline that processes large graph datasets representing network traffic. 

We have a massive raw edge list located at `/home/user/data/raw_edges.csv`. The file format is `source_ip,destination_ip,timestamp,bytes_transferred`.
We also have a proprietary, stripped analytics binary located at `/app/net_scorer`. This binary acts as an oracle: it reads comma-separated graph edges from standard input and outputs an anomalous connection score for each edge based on a proprietary rolling-window algorithm.

Currently, our baseline script (`/home/user/baseline_etl.sh`) processes the graph very slowly because it does not properly batch, index, or sort the data, and it poorly interacts with the oracle. 

Your task is to write a highly optimized Bash script at `/home/user/fast_etl.sh` that performs the following pipeline strictly using Bash built-ins, standard coreutils (like `awk`, `sort`, `head`, `tail`), and the `/app/net_scorer` binary:

1. **Filtering & Sorting:** Filter out any edges where `bytes_transferred` is less than 100. Sort the remaining edges primarily by `source_ip` (lexicographically) and secondarily by `timestamp` (numerically, ascending).
2. **Pagination/Windowing:** For each `source_ip`, keep ONLY the 10 most recent edges (highest timestamps). Discard the rest.
3. **Scoring:** Pass these filtered and windowed edges to the `/app/net_scorer` binary. The binary expects input exactly in the format `source_ip,destination_ip,timestamp,bytes_transferred` (one per line) and will output `source_ip,destination_ip,score`.
4. **Analytical Aggregation:** Calculate the total accumulated score for each `source_ip`.
5. **Output:** Write the top 25 `source_ip`s with the highest total accumulated scores to `/home/user/top_sources.txt`, formatted as `source_ip,total_score`, sorted descending by total score.

Constraints:
- The raw dataset is large. You must design an efficient processing strategy (e.g., using `sort` effectively, avoiding bash `while read` loops in favor of `awk` where possible) to minimize execution time.
- You must output exactly 25 lines in `/home/user/top_sources.txt`.
- Your script `/home/user/fast_etl.sh` must be executable and produce the correct output.

An automated test will measure the execution time of your `/home/user/fast_etl.sh` script against a stringent performance threshold, as well as verifying the exact correctness of `/home/user/top_sources.txt`.