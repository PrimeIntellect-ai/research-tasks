You are a performance engineer optimizing a bioinformatics workflow. 

We have a Rust application located in `/home/user/mutator` that reads a FASTA file (`/home/user/data/sequence.fasta`), performs a Monte Carlo simulation to evaluate mutation frequencies, and outputs a statistical hypothesis comparison (p-value) to `/home/user/results/output.txt`.

Currently, the Rust application is incredibly slow and produces statically biased results. The original developer made a classic error: they placed the FASTA file parsing and the Random Number Generator (RNG) initialization *inside* the main simulation loop. This causes severe I/O bottlenecks and resets the RNG seed on every iteration, ruining the Monte Carlo simulation's statistical validity.

Your task:
1. Fix the Rust code in `/home/user/mutator/src/main.rs`. Move the FASTA file reading/parsing and the `ChaCha8Rng` instantiation *outside* of the `for` loop so the file is read only once and the RNG advances correctly across iterations. Do not change the random seed value (`[42; 32]`) or the number of iterations (`10000`).
2. Compile the optimized Rust application using `cargo build --release`.
3. We have a Jupyter Notebook at `/home/user/workflow.ipynb` that orchestrates the pipeline. It runs the Rust binary and analyzes the results. Execute this notebook headlessly using `jupyter nbconvert --execute --to notebook --inplace /home/user/workflow.ipynb`.

A successful run will complete in a fraction of a second and generate a final processed report at `/home/user/results/summary.txt` containing the corrected p-value.