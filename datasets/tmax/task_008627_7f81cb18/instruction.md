You are a bioinformatics analyst working on a computational pipeline that calculates the "mutation potential" across a large genomic sequence.

In your workspace, there is a script located at `/home/user/integrate_mutation.py`. This script reads a sequence from `/home/user/raw_sequence.txt`, divides it into chunks, and uses Python's `multiprocessing` to calculate a numerical integration (using the Trapezoidal rule via `numpy.trapz`) over a cumulative GC-content signal for each chunk. 

Currently, the script has a reproducibility bug. Because floating-point addition is commutative but not associative, accumulating the chunk integrals in the unpredictable order they complete (via `imap_unordered`) causes the final sum to vary slightly at the lower decimal places across different runs.

Your task is to:
1. Fix `/home/user/integrate_mutation.py` so that it produces exactly reproducible results. 
2. Ensure the parallel workers still compute the chunk integrals, but the final accumulation into `total_integral` MUST be done in the strict sequential order of the original chunks (Chunk 0, then Chunk 1, then Chunk 2, etc.).
3. Use a standard left-to-right summation (e.g., a standard `for` loop over the sorted results, or Python's built-in `sum()` on the ordered list of results) to combine the chunk integrals.
4. Run the fixed script to process the sequence. The script is already designed to write the final float value to `/home/user/final_result.txt` formatted to 12 decimal places. Ensure this file is created successfully.

Do not change the mathematical logic inside the `process_chunk` function, only fix the parallel orchestration and aggregation logic in `main()`.