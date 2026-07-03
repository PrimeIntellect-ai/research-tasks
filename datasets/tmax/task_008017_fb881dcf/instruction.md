You are acting as a data scientist in a bioinformatics lab. We are trying to fit a Position Weight Matrix (PWM) model to a multiple sequence alignment of proteins to score new sequences. 

However, our current bash script (`/home/user/calc_pwm.sh`) is failing. It parses a FASTA file of aligned sequences to calculate the empirical probability distribution of amino acids at each position. Because some positions are highly conserved (e.g., every sequence has an 'A'), the frequencies of other amino acids at that position are exactly 0. When the script calculates the log-odds score (which uses `log2(p / background)`), it attempts to compute `log2(0)` and produces `-inf` values. This is akin to a model failing on a near-singular input distribution.

Your task is to fix this pipeline entirely within Bash (using coreutils like `awk`, `sed`, `grep`, etc.).

**Instructions:**
1. **Fix the Model Script:** 
   Modify the script `/home/user/calc_pwm.sh` so that it uses Laplace smoothing (pseudocounts). 
   The new formula for the probability $p_{i,a}$ of amino acid $a$ at position $i$ should be:
   $$p_{i,a} = \frac{\text{count}(i, a) + 1}{N + 20}$$
   where $N$ is the total number of sequences in the alignment, and $20$ is the standard number of amino acids.
   The log-odds score is then:
   $$S_{i,a} = \log_2 \left( \frac{p_{i,a}}{0.05} \right)$$
   (We assume a uniform background frequency of 0.05 for all 20 standard amino acids).

2. **Generate the Smoothed PWM:**
   Run your fixed script on the reference dataset `/home/user/alignment.fasta`.
   The script must output the matrix to `/home/user/smoothed_pwm.txt`. 
   The output format must be a tab-separated table where each row corresponds to a position (1-indexed), the first column is the position index, and the subsequent 20 columns are the scores for the amino acids in alphabetical order (A, C, D, E, F, G, H, I, K, L, M, N, P, Q, R, S, T, V, W, Y). 
   Format the scores to exactly 3 decimal places.

3. **Score the Target Sequence:**
   Parse the target sequence from `/home/user/target.fasta`. Note that FASTA sequences may span multiple lines.
   Calculate the total alignment score for this sequence using your `/home/user/smoothed_pwm.txt` model. The total score is the sum of the log-odds scores for the specific amino acids found at each position in the target sequence.
   Write the final numeric score (rounded to 3 decimal places) to `/home/user/target_score.txt`.

**File Locations:**
- Input alignment: `/home/user/alignment.fasta`
- Original script: `/home/user/calc_pwm.sh`
- Target sequence: `/home/user/target.fasta`
- Expected matrix output: `/home/user/smoothed_pwm.txt`
- Expected score output: `/home/user/target_score.txt`