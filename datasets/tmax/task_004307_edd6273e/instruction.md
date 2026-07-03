You are assisting a researcher who is organizing large quantities of numerical datasets. The researcher uses a proprietary, legacy compiled tool located at `/app/metric_oracle` to compute a "Dataset Similarity Score" to decide which datasets should be merged. 

Unfortunately, the source code for `/app/metric_oracle` was lost, and the researcher needs to integrate this exact metric into a modern, parallelized data-processing pipeline. 

Your task is to:
1. Treat `/app/metric_oracle` as a black box (or reverse-engineer it using standard tools). 
2. Analyze its inputs and outputs using statistical inference, sampling, and correlation benchmarking to deduce the mathematical function it computes.
3. Write a drop-in replacement script or executable at `/home/user/fast_metric`.

The `/app/metric_oracle` binary takes exactly two arguments. Each argument is a space-separated string of numbers of equal length $N$ (where $N \ge 2$). 
Example invocation:
`/app/metric_oracle "1.0 2.0 3.0" "4.0 5.0 6.0"`

Constraints and Requirements:
- Your replacement must be located exactly at `/home/user/fast_metric` and must be executable.
- Your replacement must take the exact same command-line arguments and produce the exact same standard output format (a single numeric string).
- Do not wrap the original binary; you must implement the logic natively in the language of your choice.
- Test your implementation robustly to ensure it matches the oracle's output exactly, including edge cases (e.g., zero variance).

The automated verifier will subject your `/home/user/fast_metric` to rigorous fuzz-testing against `/app/metric_oracle` with thousands of random numerical pairs to prove absolute equivalence.