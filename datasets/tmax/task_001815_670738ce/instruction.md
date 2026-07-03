You are an expert bioinformatics analyst. We need to perform a sequence motif discovery task on a newly sequenced dataset.

We have a dataset of 100 DNA sequences (each 200 bases long) located at `/app/sequences.fasta`. There is a conserved transcription factor binding site (a 15-base DNA motif) hidden with varying degrees of mutation across these sequences.

Your objective is to find the single 15-base DNA motif that maximizes the total alignment score across the entire dataset. 

**Scoring Rules:**
We are using a custom gapless local alignment scoring system. However, the exact match/mismatch penalties for this specific organism were sent as a screenshot from a recent paper. You will find this image at `/app/scoring_rules.png`. You will need to extract the scoring parameters from this image (e.g., Match score, Transition mismatch penalty, Transversion mismatch penalty).

**Fitness Function Definition:**
For a candidate 15-base motif $M$ and a single target sequence $S$:
1. Slide the 15-base motif across the 200-base sequence $S$.
2. At each window position, calculate the substitution score between $M$ and the 15-base window of $S$ using the rules from the image. 
3. The score for the sequence $S$ is the *maximum* window score found.
4. The total fitness of the motif $M$ is the sum of these maximum scores across all 100 sequences in the FASTA file.

**Task Requirements:**
1. The search space for a 15-mer is $4^{15}$ (over 1 billion) combinations. Brute-force evaluation of all possibilities against the dataset will be too slow to run in the given time frame. You must write an optimization algorithm in **C++** (e.g., Genetic Algorithm, Simulated Annealing, or a highly optimized stochastic hill climber) to find a high-scoring motif.
2. Setup your compilation environment, write the C++ code, and run your optimization.
3. Save the single best 15-base motif (e.g., `ACGTACGTACGTACG`) you discover to `/home/user/optimal_motif.txt`. The file should contain nothing but the 15 uppercase characters.
4. Save the execution log of your C++ program (showing your generations/iterations and fitness improvements) to `/home/user/optimization.log`.
5. You must achieve a total dataset fitness score of at least **5500**.