You are a performance engineer optimizing a bioinformatics pipeline for primer design and sequence alignment. 

We have a proprietary tool, provided as a stripped binary at `/app/primer_match`, which calculates the optimal alignment score of a short primer sequence against a longer reference DNA sequence. The tool uses a sliding window approach without gaps (no insertions or deletions) and applies a proprietary 4x4 scoring matrix for the bases A, C, G, and T.

Currently, this binary is used in a shell loop for large datasets, which is unacceptably slow. Your task is to:
1. **Reverse-engineer the scoring matrix:** Interrogate the `/app/primer_match` binary. It accepts two arguments directly on the command line: `<reference_sequence>` and `<primer_sequence>`. It outputs a single integer representing the maximum alignment score found across all sliding windows of the reference where the primer was compared.
2. **Implement a fast replacement in Rust:** Write a highly optimized Rust program at `/home/user/fast_primer_match.rs`. 
3. Your program must read a single long continuous reference sequence from the file `/home/user/reference.txt` and a list of candidate primers (one per line) from `/home/user/primers.txt`.
4. For each primer, your program must calculate the maximum alignment score against the reference using the deduced scoring matrix (sliding window, no gaps).
5. The output must be written to `/home/user/scores.txt`, containing one integer score per line, strictly in the same order as the primers.
6. **Compile and optimize:** Compile your program to `/home/user/fast_primer_match`. You must ensure your reproducible computation pipeline is highly optimized. 

Your solution will be graded programmatically by a verifier that checks both the exact correctness of your scores and the execution speed. Your Rust implementation must achieve a massive speedup (at least 50x) compared to invoking the provided binary in a loop for every primer.