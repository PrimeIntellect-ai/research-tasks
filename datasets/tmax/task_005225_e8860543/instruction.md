You are an AI assistant helping a data science researcher organize and analyze a dataset of document embeddings. 

The researcher has a set of research papers represented as dense numerical vectors and wants to find similar papers using a custom script, as well as benchmark the performance of this search.

Your task is to write two Bash scripts:

**1. Similarity Search Script (`/home/user/search.sh`)**
Write a Bash script that calculates the Cosine Similarity between a query vector and a dataset of document vectors.
- Usage: `./search.sh <query_csv> <dataset_csv> <top_k>`
- The `query_csv` contains a single line with comma-separated floating-point numbers representing the query vector (e.g., `0.12,0.55,-0.23,0.88,0.11`).
- The `dataset_csv` contains multiple lines. Each line represents a document. The first column is the `DocID` (a string), followed by the vector components, all comma-separated (e.g., `doc_001,0.10,0.50,-0.20,0.90,0.15`).
- The script must calculate the cosine similarity between the query vector and each document vector. Cosine similarity is defined as the dot product of the vectors divided by the product of their Euclidean norms.
- The output should be printed to standard output and must contain exactly `<top_k>` lines, representing the most similar documents.
- Output format: `DocID,similarity_score`. The similarity score must be formatted to exactly 4 decimal places. Sort the output in descending order of similarity. If there's a tie in similarity, preserve the original dataset order.
- The script must be written in Bash (you are strongly encouraged to use `awk` within the bash script for the mathematical computations).

**2. Benchmarking Script (`/home/user/benchmark.sh`)**
The researcher needs to understand how the search script's execution time scales with dataset size.
- Usage: `./benchmark.sh <query_csv> <dataset_csv>`
- The script must benchmark the execution time of `./search.sh` for `top_k=5` using subsets of the `dataset_csv`.
- Specifically, it should test on the first 100, 200, 300, 400, and 500 lines of `dataset_csv` (using `head`).
- For each subset, measure the wall-clock execution time of `search.sh` in seconds (you can use `date +%s.%N` before and after the call, or the `time` command parsed appropriately).
- Write the results to `/home/user/benchmark_results.csv` in the format: `number_of_lines,execution_time_in_seconds` (e.g., `100,0.045`).

**Dataset Location:**
Assume the researcher has already placed the files at:
- Query file: `/home/user/data/query.csv`
- Dataset file: `/home/user/data/dataset.csv` (contains exactly 500 lines)

**Constraints:**
- Ensure both scripts are executable.
- Do not use Python, R, or any other non-Bash scripting language for the core computations. You must use standard Linux utilities (Bash, awk, sed, grep, head, bc, etc.).