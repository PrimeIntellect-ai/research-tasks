You are a performance engineer tasked with debugging a scientific pipeline. 

We have a Python script located at `/home/user/spectral_primer_score.py`. This script is designed to evaluate the viability of a target primer against a database of DNA sequences. For each sequence in the database, it calculates a simple alignment score with the primer, and multiplies it by the dominant frequency peak (found via FFT) of that sequence's corresponding spectral signal. Finally, it sums all these values to produce a single aggregate score.

To speed up the pipeline, a colleague parallelized it using Python's `multiprocessing`. However, they introduced a bug: the aggregate floating-point score is slightly different on every run! This is a classic floating-point reduction order issue caused by non-deterministic aggregation.

Your tasks are:
1. Identify and fix the non-determinism in `/home/user/spectral_primer_score.py` so that it always produces the exact same floating-point result on every run. You must preserve the parallel execution (do not remove `multiprocessing.Pool`), but ensure the reduction (summation) happens in a deterministic, reproducible order (e.g., the original order of the sequences in the FASTA file).
2. Run your fixed script.
3. Save the final deterministic aggregate score (just the number) to `/home/user/deterministic_score.txt`.

Ensure the script can be executed via `python3 /home/user/spectral_primer_score.py`.