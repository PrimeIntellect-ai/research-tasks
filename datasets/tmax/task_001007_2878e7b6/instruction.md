You are a bioinformatics analyst tasked with processing a large sequence dataset to estimate GC content distributions and test hypotheses about the sequence origins.

We have a custom, vendored sequence calculation tool located at `/app/seqcalc-1.0`. This tool reads FASTA sequences from standard input and outputs the GC content of each sequence to standard output. 

Your objectives are:
1. **Fix the Vendored Tool:** The `seqcalc` tool is designed to be highly parallel using OpenMP, but currently, it runs single-threaded and is far too slow for our pipeline. Investigate the source code and build system in `/app/seqcalc-1.0`, fix the issue preventing parallel execution, and recompile it.
2. **Process Scientific Data:** We have a large dataset of DNA sequences stored in HDF5 format at `/app/data/reads.h5`. A helper script `/app/bin/h5_to_fasta.py` is available; it takes the `.h5` file path as an argument and prints FASTA to stdout.
3. **Build the Bash Pipeline:** Write a Bash script at `/home/user/pipeline.sh` that does the following:
   - Streams the FASTA data from `/app/data/reads.h5` using the helper script.
   - Pipes the stream directly into your recompiled `seqcalc` tool.
   - Calculates the **mean** and **variance** of the resulting GC content values. You must do this using standard Bash utilities (like `awk`).
   - Writes the final output to `/home/user/stats_result.txt` in exactly this format:
     `Mean: <mean_value>, Variance: <variance_value>`
     (Round values to 4 decimal places).

**Constraints:**
- Your `/home/user/pipeline.sh` must be executable and autonomous.
- Because of strict performance budgets, your pipeline must process the entire dataset in under 4.0 seconds. If `seqcalc` is properly fixed to use multi-threading, this will be easily achievable.