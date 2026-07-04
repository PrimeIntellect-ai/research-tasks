You are a bioinformatics researcher attempting to design an optimal DNA primer for an assay. You have a target DNA sequence and a background DNA sequence. You also have a list of candidate 10-mer (10-nucleotide) primers.

Your goal is to evaluate the candidate primers based on sequence alignment counts and their structural statistics (GC content) to optimize the assay's signal-to-noise ratio. You must find the candidate primer that maximizes a custom score function.

**Files provided:**
1. `/home/user/target.seq`: A text file containing the target DNA sequence on a single line.
2. `/home/user/background.seq`: A text file containing the background genomic sequence on a single line.
3. `/home/user/candidates.txt`: A text file containing candidate 10-mer primers, one per line.

**Scoring Rules:**
For each candidate primer, calculate its score using the following steps:
1. **Target Alignment ($N_T$):** The number of *exact, non-overlapping* occurrences of the primer in `target.seq`.
2. **Background Alignment ($N_B$):** The number of *exact, non-overlapping* occurrences of the primer in `background.seq`.
3. **Statistical Filter:** You must strictly ignore any candidate where $N_T \le N_B$. These primers do not provide a positive statistical signal.
4. **GC Penalty:** Calculate the GC content percentage of the 10-mer. (e.g., if there are 4 'G's and 'C's combined in the 10-mer, the GC content is 40%). The penalty is the absolute difference between the GC content percentage and 50%. 
   *Penalty* = $|GC\% - 50|$
5. **Final Score Calculation:** 
   *Score* = $(N_T \times 20) - (N_B \times 5) - Penalty$

**Objective:**
Using only Bash built-ins, coreutils, and standard CLI tools (`awk`, `grep`, `sed`, `tr`, `bc`, etc.), calculate the score for all candidates. Find the primer with the highest score. 

Once you identify the optimal primer, write the sequence of the winning primer and its score (separated by a single space) to `/home/user/optimal_primer.txt`. 
*Format Example for the output file:*
`ATGCATGCAT 45`

*Note: In the event of a tie for the highest score, select the primer that appears alphabetically first.*