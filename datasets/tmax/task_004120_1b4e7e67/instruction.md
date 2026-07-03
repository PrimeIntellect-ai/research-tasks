You are a data scientist modeling GC-content distributions across genomic datasets. We rely on an open-source bash utility called `bash-fasta-density` to parse FASTA files, compute GC-content density estimates, and process sequences in parallel. 

The source code for this utility has been vendored at `/app/bash-fasta-density-1.0`. However, the primary script at `/app/bash-fasta-density-1.0/bin/calc_density.sh` contains a bug related to its parallel execution setup. When it attempts to process sequences using `xargs` for parallelization, it fails and produces no valid density output.

Your task is to:
1. Identify and fix the parallel execution bug within `/app/bash-fasta-density-1.0/bin/calc_density.sh` so that it correctly computes the statistics. You may use standard Bash features to fix this.
2. Create a wrapper script at `/home/user/run_density.sh` that takes a single FASTA file path as its first argument and directly invokes the fixed `/app/bash-fasta-density-1.0/bin/calc_density.sh` script on it. 
3. The wrapper script must be executable and print the final computed densities to standard output exactly as the fixed tool produces them.

Your solution will be tested against randomly generated FASTA files to ensure bit-exact equivalence with a reference implementation.