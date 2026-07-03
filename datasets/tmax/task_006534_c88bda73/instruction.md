You are a bioinformatics analyst tasked with debugging and optimizing a sequence scoring tool. 

There is a Rust project located at `/home/user/motif_scorer`. It calculates an affinity score for a set of DNA sequences based on given nucleotide weights. However, the tool is currently unreliable: it uses multi-threading to process sequences and accumulates floating-point scores into a shared `Mutex<f64>`. Because floating-point addition is not associative and thread completion order is non-deterministic, the final score varies slightly between runs. 

Your tasks are to:

1. **Fix the Rust Code:** 
   Modify `/home/user/motif_scorer/src/lib.rs` to ensure deterministic floating-point accumulation. You must collect the individual sequence scores, sort them by their original index (their 0-based order in the FASTA file), and *then* sum them sequentially. After your fix, `cargo test` must pass reliably (the existing test runs the scoring 10 times and asserts they are all exactly identical).

2. **Optimize Weights:** 
   The tool takes nucleotide weights for A, C, G, and T. We want to find the optimal combination of weights that **maximizes** the total score for the sequences in `/home/user/data/promoters.fasta`. 
   *Constraints:* The weights must be non-negative (`w >= 0.0`) and sum to exactly `1.0` (`w_A + w_C + w_G + w_T = 1.0`).
   Write a script (e.g., Python using `scipy.optimize` or simple random search) that calls the compiled `motif_scorer` binary to find the optimal weights. 
   Write the optimal weights to `/home/user/best_weights.txt` as a single comma-separated line: `A,C,G,T` (rounded to 3 decimal places).
   Write the highest score achieved to `/home/user/max_score.txt` (rounded to 2 decimal places).

3. **Visualize the Optimization:**
   During your optimization search, keep track of the objective score at each evaluation step. Generate a line plot or scatter plot of these scores over the iterations and save it as `/home/user/optimization_trace.png`.

*Notes:*
- The `motif_scorer` CLI usage is: `target/release/motif_scorer <fasta_file> <w_A> <w_C> <w_G> <w_T>`
- You may use any Python libraries available or install them via pip.