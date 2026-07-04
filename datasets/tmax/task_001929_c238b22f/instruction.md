You are a data analyst investigating a financial fraud ring. You have intercepted a voicemail from the lead investigator and a dataset of transaction logs (CSVs). 

First, transcribe the audio file located at `/app/voicemail.wav`. You can install python packages like `openai-whisper` or use any available tools in your environment to extract the spoken instructions. 

The audio will describe a specific graph pattern (a topological structure) that indicates fraudulent behavior in a transaction network.

You are given a set of sample CSV files in `/home/user/samples/`. Each CSV represents a directed graph of transactions with the following columns:
`source_account,target_account,amount,timestamp`

Your task is to create a Bash script at `/home/user/analyze_graph.sh` that takes a single argument (the path to a CSV file). The script must:
1. Analyze the graph schema and relationships represented in the provided CSV.
2. Determine if the graph contains the exact fraudulent pattern described in the audio file. You may use standard Linux utilities, `awk`, or CLI databases like `sqlite3` or `duckdb` within your Bash script to project the graph and perform the pattern matching.
3. Exit with code `1` (reject/evil) if the fraudulent graph pattern is detected.
4. Exit with code `0` (accept/clean) if the pattern is NOT detected.

Ensure your Bash script is highly optimized, as it will be evaluated against a massive corpus of hidden CSV files. It must cleanly handle the exact header format `source_account,target_account,amount,timestamp`.

Do not hardcode specific account IDs; you are looking for the structural graph pattern described in the audio. Make sure `/home/user/analyze_graph.sh` is executable.