You are a performance engineer working for a biotechnology company. We have a prototype Rust application called `biocore_sim` located at `/home/user/biocore_sim`. This application analyzes a droplet microfluidics PCR experiment and simulates the corresponding biochemical kinetics. 

The application currently performs three main tasks:
1. **Video Extraction & Curve Fitting**: It shells out to `ffmpeg` to extract the average pixel intensity of the top-left 10x10 region for every frame of a thermocycling video located at `/app/reaction_video.mp4`. It then fits a logistic curve to this data to calculate the quantification cycle (Cq).
2. **ODE Simulation**: It uses the extracted temperature/intensity profile to drive a numerical Ordinary Differential Equation (ODE) solver, which models the expected DNA amplification concentration over time.
3. **Primer Alignment**: It performs a local sequence alignment of our target primer sequences against a reference genome located at `/app/reference.fasta`.

**The Problem:**
The application is currently unacceptably slow, taking over 45 seconds to process a single 5-second video clip and reference sequence. The biology team needs this to run in near real-time (under 1.5 seconds) to be deployed on edge devices. 

Your task is to:
1. Profile the Rust application in `/home/user/biocore_sim`.
2. Identify the severe performance bottlenecks in the codebase. (Hint: look for inefficient $O(N^2)$ algorithms, excessive memory allocations in inner loops, and unnecessarily small time-steps in the numerical solver).
3. Optimize the Rust source code. You may use external crates like `rayon` for parallelism or rewrite the naive implementations.
4. Ensure the optimized code produces mathematically equivalent results to the original implementation.
5. Compile your optimized code using `cargo build --release`.

**Execution & Output Specification:**
The program must be executable via:
`./target/release/biocore_sim /app/reaction_video.mp4 /app/reference.fasta /home/user/results.json`

The final output must be written to `/home/user/results.json` in the following format:
```json
{
  "cq_value": 15.42,
  "final_dna_concentration": 0.8543,
  "max_alignment_score": 142
}
```

The automated verifier will measure the wall-clock execution time of your release binary and check the accuracy of `results.json`. You must achieve an execution time of **less than 1.5 seconds**.