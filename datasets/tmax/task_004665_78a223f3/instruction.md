You are assisting a data researcher in organizing a large, noisy dataset of graph structures extracted from a NoSQL database. 

The researcher uses a proprietary, stripped legacy binary located at `/app/graph_oracle` to compute shortest paths and structural aggregations on these graphs. The binary takes a single argument: the path to a JSON file containing graph edges. 

Unfortunately, the database dump contains corrupted and "malicious" records (e.g., NoSQL injection artifacts, invalid node types, or impossible weights). When the binary encounters these anomalous files, it crashes or hangs. 

Your task is to:
1. Experiment with `/app/graph_oracle` using your own test JSON files to deduce the exact schema, types, and constraints the binary expects. Determine what specific data anomalies cause it to fail.
2. Write a Bash script at `/home/user/filter.sh` that takes a single file path as an argument.
3. Your script must parse the JSON (you may use `jq`) and validate it against the implicit rules you discovered.
4. If the JSON is perfectly clean and safe for the oracle, your script must exit with code `0`.
5. If the JSON contains any anomaly that would break the oracle, your script must exit with code `1` (or higher).

The test suite will evaluate your `/home/user/filter.sh` against two hidden datasets: a corpus of perfectly valid graph files, and a corpus of anomalous/malicious files. 

Constraints:
- Your solution must be written in Bash (using `jq`, `awk`, `sed`, or other standard coreutils).
- `/home/user/filter.sh` must be executable.
- Do not attempt to modify or patch the `/app/graph_oracle` binary.