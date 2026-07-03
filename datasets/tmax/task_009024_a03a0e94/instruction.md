I am a researcher running a simulation pipeline that evaluates biological sequence alignments. I have a Rust project located at `/home/user/repro_eval` that reads alignment scores from an HDF5 file (`/home/user/data.h5`), converts these scores into probability distributions, and calculates the Kullback-Leibler (KL) divergence between them.

However, I'm facing a reproducibility crisis. Every time I run `cargo run`, the final computed KL divergence value printed to standard output changes very slightly (e.g., at the 10th decimal place). This floating-point drift is ruining my reproducible computation pipeline. 

I suspect the issue is due to the floating-point reduction order. The data is grouped using a standard hash map before summation, which means the order of summation is non-deterministic between runs, leading to non-associative floating-point rounding differences.

Your task:
1. Identify the source of the non-determinism in `/home/user/repro_eval/src/main.rs`.
2. Fix the Rust code so that the floating-point reduction order is strictly deterministic and reproducible across multiple runs, without changing the mathematical logic.
3. Compile and run the project.
4. Redirect the deterministic output (which should just be the single floating-point number) to `/home/user/repro_eval/final_output.txt`.

Please ensure you are using a deterministic collection or sorting the keys before reduction.