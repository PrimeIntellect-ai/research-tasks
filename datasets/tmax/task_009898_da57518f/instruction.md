You are assisting a bioinformatics analyst. We have a Rust project located at `/home/user/gc_analyzer` that processes a large DNA sequence from `/home/user/data/genome.fasta`. 

Currently, the program computes the GC-content density profile using a sliding window (window size = 100 base pairs, step = 100). It then integrates these values (sums them up) to find the total GC mass. However, the analyst noticed that the total integral yields slightly different results on every run. This is because the code uses a parallel reduction (`rayon`) on floating-point numbers, and the non-associativity of floating-point addition combined with unpredictable thread scheduling causes non-reproducible results.

Your task is to fix this bug and extend the program with additional statistical analyses.

Specifically, you need to modify `/home/user/gc_analyzer/src/main.rs` to accomplish the following:
1. **Fix Reproducibility:** Modify the integration step so that the sum of the GC ratios is perfectly deterministic. You can do this by performing the final reduction sequentially, or by using a stable summation algorithm.
2. **Curve Fitting:** Compute a simple linear regression ($y = mx + c$) of the windowed GC ratios ($y$) against the window index ($x$, starting at $0$).
3. **Bootstrap Confidence Intervals:** Calculate the 95% bootstrap confidence interval for the mean of the windowed GC ratios. Use exactly 10,000 resamples. To ensure determinism in testing, you must use the `rand_chacha::ChaCha8Rng` seeded with the exact value `42`. Use the percentile method (2.5th and 97.5th percentiles).
4. **Visualization:** Use the `plotters` crate to generate a line plot of the windowed GC ratios versus the window index. Save this plot as an SVG file at `/home/user/output/gc_plot.svg`.
5. **Output Generation:** Write the calculated statistics to a JSON file at `/home/user/output/results.json` with the following exact keys (all values as standard JSON numbers):
   - `total_gc_integral`: The deterministically summed GC ratios.
   - `regression_slope`: The slope $m$ from the linear regression.
   - `regression_intercept`: The intercept $c$ from the linear regression.
   - `bootstrap_ci_lower`: The 2.5th percentile of the bootstrap distribution.
   - `bootstrap_ci_upper`: The 97.5th percentile of the bootstrap distribution.

You can run `cargo add plotters serde_json rand rand_chacha` if needed.
Ensure `/home/user/output` exists. Finally, build and run the binary so the outputs are generated.