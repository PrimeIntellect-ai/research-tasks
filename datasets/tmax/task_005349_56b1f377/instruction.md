You are a data engineer tasked with optimizing a critical ETL pipeline that processes graph database query results. Our upstream graph database (using Cypher) periodically dumps unpaginated, raw node and edge data into a massive CSV file. Your job is to create a high-performance C program that filters, sorts, and paginates this data.

Currently, we have a slow Python reference implementation (`/home/user/slow_reference.py`) that takes too long to run. We need a C equivalent (`/home/user/graph_etl`) that uses the `libcsv` library to process the data much faster.

However, the source for `libcsv` (vendored at `/app/libcsv-3.0.3`) has a bug in its build configuration introduced during a recent botched migration. 

Your tasks are:
1. Identify and fix the deliberate perturbation in the vendored `libcsv-3.0.3` package at `/app/libcsv-3.0.3`. Build and install it locally so your C program can link against it.
2. Write a C program at `/home/user/graph_etl.c` that compiles to `/home/user/graph_etl`.
3. Your C program must accept the following command-line arguments:
   `--input <file> --filter-label <string> --sort-prop <string> --limit <int> --offset <int> --output <file>`
4. The input CSV (`/home/user/graph_results.csv`) has the format: `node_id,label,properties_json`.
   Example: `101,Person,{"age": 35, "score": 8.5}`
5. Your program must:
   - Use the fixed `libcsv` to parse the input.
   - Filter rows to include only those where the `label` exactly matches `--filter-label`.
   - Parse the `properties_json` (you may use basic string searching or a lightweight JSON parser if you prefer) to extract the numeric value of `--sort-prop`.
   - Sort the filtered results in descending order based on the extracted numeric property.
   - Apply the `--offset` and `--limit` for pagination.
   - Write the resulting rows (preserving the exact original CSV formatting for those rows) to the specified `--output` file.
6. The compiled C program must achieve a significant speedup over the Python reference script.

We will test your implementation by running it on a large dataset and measuring the execution time relative to the Python version. Create a script `/home/user/run_benchmark.sh` that times both tools and verifies the outputs match.