You are a bioinformatics analyst processing a 1D spatial genomic signal (e.g., conservation scores along a chromosome sequence). 

You have been provided with a dataset at `/home/user/sequence_scores.txt` containing 1000 floating-point numbers, one per line, representing scores at genomic positions 0 through 999.

Your task is to build a reproducible Go pipeline that performs domain decomposition (mesh refinement) on this signal to isolate regions of high variance, and then computes bootstrap confidence intervals for the mean score of each resulting region.

Write a Go program at `/home/user/analyze.go` and a Makefile at `/home/user/Makefile` that fulfills the following requirements:

1. **Domain Decomposition (Mesh Refinement)**:
   - Start with an initial "mesh" of 10 equal-sized bins: [0, 100), [100, 200), ..., [900, 1000). The intervals are inclusive of the start index and exclusive of the end index.
   - For each bin, calculate the population variance of the scores (divide by N, not N-1). 
   - **Refinement rule**: If a bin's variance is strictly greater than `0.5`, refine it by splitting it into two equal-sized sub-bins (e.g., [100, 200) becomes [100, 150) and [150, 200)).
   - Only perform this refinement step *once* (maximum depth of 1). Sub-bins should not be further split, even if their variance remains > 0.5.

2. **Bootstrap Confidence Intervals**:
   - For every final bin in your mesh (both un-split and split bins, ordered by start position), calculate the 95% Bootstrap Confidence Interval for the mean.
   - Use exactly `1000` bootstrap iterations per bin.
   - For each iteration, sample N elements with replacement from the bin's data (where N is the number of elements in that bin), and calculate the mean of the sample.
   - To ensure reproducibility, you must initialize your random number generator for *each bin* individually right before the bootstrap loop. Use `math/rand.New(math/rand.NewSource(int64(Start)))` where `Start` is the start index of the bin. Use this localized RNG's `.Intn()` method to select random indices.
   - Sort the 1000 bootstrap means in ascending order. The lower bound of the 95% CI is the value at index 25 (0-indexed), and the upper bound is the value at index 974.

3. **Output & Reproducibility**:
   - The Go program must output the results to `/home/user/pipeline_output.tsv`.
   - The TSV must have a header: `Start\tEnd\tMean\tLower95\tUpper95`.
   - Format the `Mean`, `Lower95`, and `Upper95` values to 4 decimal places (e.g., `fmt.Sprintf("%.4f", val)`).
   - Your `Makefile` must have a default target `all` that compiles the Go code into an executable named `analyze`, and a target `run` that executes `./analyze`.

Ensure your logic strictly follows the random seeding and indexing instructions so your output matches the expected programmatic results.