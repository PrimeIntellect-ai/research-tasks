You are a data scientist tasked with optimizing a slow, legacy data-cleaning pipeline. 

We currently use a proprietary, stripped binary located at `/app/legacy_filter` to clean and stratify incoming CSV data. This binary takes two arguments: an input CSV file and an output CSV file path:
`/app/legacy_filter <input.csv> <output.csv>`

The legacy binary is single-threaded and extremely slow. It performs two main operations:
1. Filters out anomalous rows based on a mathematical relationship between the numerical columns.
2. Performs stratified sampling by selecting a specific subset of the remaining rows per category.

Your objectives:
1. **Reverse Engineer:** Analyze `/app/legacy_filter` (using standard tools like `strings`, `objdump`, or black-box testing) to deduce its exact filtering and stratification logic. The input CSVs have headers: `id,category,v1,v2,v3`.
2. **Optimize with C++:** Write a parallel C++ program at `/home/user/fast_filter.cpp` that replicates the exact same logic but runs significantly faster. It must accept the same command-line arguments.
3. **Pipeline & Scheduling:** Write a bash script `/home/user/pipeline.sh` that compiles your C++ program and sets up a user cron job. The cron job should run every 5 minutes, executing the compiled `fast_filter` on any `.csv` files found in `/home/user/incoming/` and moving the outputs to `/home/user/processed/`.

Success is evaluated by a metric threshold: Your C++ program must produce the exact same output data as the legacy binary, but with a **speedup of at least 4.0x** when measured against a held-out test dataset of 5 million rows.