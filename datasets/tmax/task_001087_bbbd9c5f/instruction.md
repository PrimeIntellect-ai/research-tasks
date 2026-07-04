You are a bioinformatics analyst. You have been provided with a Rust project located at `/home/user/gc_bootstrap`.
This project reads a FASTA file of DNA sequences (`/home/user/sequences.fasta`), calculates the GC content for each sequence, and then uses bootstrap sampling to calculate a confidence interval for the mean GC content. 

However, there is a problem: the script occasionally produces slightly different results across multiple runs despite using a fixed PRNG seed (ChaCha8Rng initialized with seed 42). This non-reproducibility is due to the floating-point reduction order in the parallel Rayon iterator used for summing the bootstrap samples.

Your task:
1. Identify and fix the non-deterministic parallel floating-point reduction in `/home/user/gc_bootstrap/src/main.rs`. You should make the reduction sequential to guarantee strict bitwise reproducibility of the floating-point sum. Do NOT change the random seed, the number of bootstrap iterations, or the PRNG logic.
2. Compile and run the fixed Rust program.
3. Save the exact printed output (the overall bootstrap mean) to `/home/user/result.txt`.

Ensure `/home/user/result.txt` contains only the single floating-point number formatted exactly as the script outputs it.