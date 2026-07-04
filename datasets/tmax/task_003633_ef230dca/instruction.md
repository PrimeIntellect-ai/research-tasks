Hello! I am a computational biology researcher working on a new multiplex PCR assay. I need you to help me build a reproducible primer screening pipeline. 

First, I left a screenshot of our assay protocol in `/app/assay_protocol.png`. It contains the target sequence we are amplifying and the Monte Carlo simulation parameters we need to use for predicting primer dimer formation. Please extract the `TARGET_SEQUENCE`, `MC_ITERATIONS`, and `TEMP_THRESHOLD` from this image.

Second, I need you to develop a Python command-line tool `primer_filter.py` that processes a FASTA file of candidate primers and filters them. The tool must accept a primer if it is "safe" and reject it if it is "dangerous".
A primer is considered dangerous (and must be rejected) if:
1. It does not perfectly align (100% match) to a substring of the `TARGET_SEQUENCE`.
2. OR, it fails the Monte Carlo primer-dimer simulation. 

The Monte Carlo simulation for a primer should work as follows:
- Run `MC_ITERATIONS` random walks.
- In each iteration, randomly pair the primer sequence against itself (simulate two molecules colliding) by choosing a random overlap length between 4 and the length of the primer. 
- Calculate the complementary score of the overlapping region (A-T and C-G matches count as 1, mismatches/gaps count as 0). 
- Calculate the binding fraction: (complementary score) / (primer length).
- Average this binding fraction across all `MC_ITERATIONS`.
- If the average binding fraction is greater than or equal to the `TEMP_THRESHOLD`, the primer is likely to form dimers and must be rejected.

Your tool should be invokable exactly like this:
`python3 /home/user/primer_filter.py --input <path_to_fasta> --output <path_to_output_fasta> --target <TARGET_SEQUENCE> --mc-iters <MC_ITERATIONS> --thresh <TEMP_THRESHOLD>`

Finally, we have a test dataset of known good and bad primers.
- The "clean" primers (which your tool must preserve/accept) are located in `/app/corpora/clean/` (a directory of `.fasta` files).
- The "evil" primers (which your tool must reject/filter out completely) are located in `/app/corpora/evil/` (a directory of `.fasta` files).

Your goal is to ensure `primer_filter.py` achieves 100% acceptance on the clean corpus and 100% rejection on the evil corpus. Output the accepted primers in standard FASTA format. Write your script in `/home/user/primer_filter.py`.