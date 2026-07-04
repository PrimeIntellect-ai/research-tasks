You are acting as a bioinformatics data analyst. We have a Go pipeline that estimates the local k-mer density across different genomic sequence chunks, reading pre-calculated sequence weights from `/home/user/reads.txt`.

Currently, the script `/home/user/kmer_density.go` runs concurrent workers to process these weights. However, we have a reproducibility problem: because the goroutines complete in a non-deterministic order and directly add to a shared floating-point accumulator (`totalDensity`), the final result varies slightly between runs due to floating-point addition associativity. This fails our numerical stability tests for reproducible pipelines.

Your task:
1. Inspect the `/home/user/kmer_density.go` script.
2. Modify the script to ensure the floating-point reduction (addition) is completely deterministic and reproducible. Specifically, the weights must be accumulated in the exact sequential order they appear in `/home/user/reads.txt`.
3. You may keep the concurrent processing of individual items (if any complex logic were there, though here it's just a multiplication), but the final summation must strictly follow the original input order.
4. Run your fixed Go script and redirect its standard output to `/home/user/stable_result.txt`.

Ensure your final result is printed to 12 decimal places (as it is in the original script). Do not change the mathematical operation (`v * 0.123456789`), only the order of summation.