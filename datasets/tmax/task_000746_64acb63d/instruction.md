You are a bioinformatics analyst working with a legacy, highly optimized distributed graph constructor. The pipeline uses a proprietary executable to build De Bruijn graphs from DNA sequences and count the number of connected components. 

However, the provided binary (`/app/bin/debruijn_mpi`) is stripped, undocumented, and highly unstable. It routinely deadlocks or segfaults when processing specific sequencing artifacts. We need you to build a robust preprocessing and analysis pipeline in Bash.

Your objectives are:

1. **Write a Data Sanitizer:** 
   Create a Bash script at `/home/user/sanitize_reads.sh` that takes an input FASTA file as the first argument and writes a cleaned FASTA file to the second argument. 
   Through reverse engineering or testing the binary, you'll find it fails on sequences containing any 'N' (unknown nucleotides) or extremely long homopolymers (>20 consecutive identical nucleotides, e.g., 21 'A's). Your script must filter out the *entire* FASTA record (both the header line starting with '>' and the sequence line) if the sequence contains an 'N' or >20 consecutive identical nucleotides. Valid records must be preserved exactly as they are.

2. **Parallel Execution and Convergence Testing:**
   We need to determine the optimal $k$-mer size for a sample dataset located at `/data/sample_reads.fasta`. 
   The binary is executed via MPI and takes a k-mer size and an input file: 
   `mpirun -np 4 /app/bin/debruijn_mpi -k <kmer_size> <input.fasta>`
   The binary prints a single integer to stdout representing the number of connected components in the resulting graph. 
   
   Write a script at `/home/user/find_optimal_k.sh` that:
   - Sanitizes `/data/sample_reads.fasta` using your `sanitize_reads.sh` script, saving it to `/tmp/clean_sample.fasta`.
   - Iterates through odd $k$-mer sizes starting from $k=15$ upwards (15, 17, 19, ...).
   - Runs the MPI binary on `/tmp/clean_sample.fasta` using 4 processes.
   - Stops when the graph "converges", which we define as the number of connected components reaching exactly 1.
   - Writes only this optimal $k$ value to `/home/user/optimal_k.txt`.

Ensure your scripts are executable. The automated test suite will aggressively test your `sanitize_reads.sh` against internal datasets containing edge cases, so ensure the logic is strictly adherent to the filtering rules.