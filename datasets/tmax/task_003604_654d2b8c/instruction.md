You are assisting a bioinformatics researcher who is running numerical simulations of DNA amplification (similar to a real-time PCR binding assay). The researcher wrote a C-based ODE integrator to model the reaction kinetics using MCMC sampling for the posterior estimation of binding affinities. 

However, the numerical integrator diverges due to wrong step-size adaptation whenever it encounters "stiff" regions in the sequence kinetics. These stiff regions are caused by specific "evil" sequences. The researcher has provided a video (`/app/stiff_ode_debug.mp4`) of the simulation's visual output, where the plot's step-size visibly collapses to zero (producing black frames) when these sequences are processed.

Your task is to create a C program that acts as a pre-simulation filter. It must parse a FASTA sequence, compute its statistical properties, and classify it as safe to simulate ("clean") or likely to cause divergence ("evil").

**Technical Requirements:**
1. Write a C program at `/home/user/sequence_filter.c` and compile it to `/home/user/sequence_filter`.
2. The program must accept exactly one argument: the absolute path to a `.fasta` file.
   Example: `/home/user/sequence_filter /app/corpus/clean/seq1.fasta`
3. The program must parse the FASTA file, extracting the nucleotide sequence (ignoring headers and newlines).
4. The program must evaluate the sequence based on the following criteria that cause ODE stiffness:
   - **G-Quadruplex Primer Match:** If the sequence contains the motif `GGGG` followed by exactly 1, 2, or 3 arbitrary nucleotides, followed by another `GGGG`, it is "evil".
   - **Probability Distribution Metric:** Calculate the Kullback-Leibler (KL) divergence of the overlapping 2-mer (dinucleotide) frequencies in the sequence relative to a perfectly uniform distribution (where each of the 16 possible 2-mers has probability 1/16). If the KL divergence is strictly greater than `0.20` nats, the sequence is "evil". (Note: To avoid log(0), add a pseudocount of 1 to all 2-mer counts before calculating probabilities).
5. **Output / Exit Code:** 
   - If the sequence is "evil", the program must exit with status code `1` (reject).
   - If the sequence is "clean" (none of the evil conditions are met), the program must exit with status code `0` (preserve).

**Testing:**
You have been provided with two directories of FASTA files:
- `/app/corpus/evil/`: Contains sequences known to cause integrator divergence.
- `/app/corpus/clean/`: Contains well-behaved sequences.
Your compiled executable will be tested against all files in these directories to verify that 100% of the evil corpus is rejected and 100% of the clean corpus is preserved.