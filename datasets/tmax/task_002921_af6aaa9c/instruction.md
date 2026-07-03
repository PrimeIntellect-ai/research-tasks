You are a performance engineer optimizing a bioinformatics pipeline. We have a large FASTA file located at `/home/user/sequences.fasta` containing DNA sequences. 

Your task is to write a script (you may use a combination of Bash, Awk, and Python) to process this file and perform the following statistical and linear algebra operations:

1. **FASTA Parsing & Matrix Construction**:
   - Parse the FASTA file (ignoring header lines starting with `>`).
   - Treat the sequence lines as one continuous sequence (i.e., the last character of a sequence line transitions into the first character of the next sequence line, but do NOT bridge across different headers—assume each header starts a new independent sequence).
   - Count the frequencies of all 16 overlapping dinucleotides (AA, AC, AG, AT, CA, ..., TT).
   - Construct a 4x4 transition matrix $M$ where rows represent the first nucleotide and columns represent the second nucleotide. The row/col order must be A, C, G, T.

2. **Matrix Decomposition & Convergence Testing**:
   - Convert the count matrix $M$ into a right-stochastic transition probability matrix $P$ by dividing each element by its row sum.
   - Use Power Iteration to find the stationary distribution vector $\pi$ (such that $\pi P = \pi$). 
   - Initialize $\pi_0 = [0.25, 0.25, 0.25, 0.25]$. 
   - Iterate $\pi_{n+1} = \pi_n P$. Stop when the L2 norm of the difference between successive vectors is strictly less than $10^{-7}$ (i.e., $||\pi_{n+1} - \pi_n||_2 < 10^{-7}$). Record the number of iterations required.

3. **Statistical Hypothesis Comparison**:
   - We want to test the null hypothesis that the outgoing transitions from the nucleotide 'A' are uniformly distributed (i.e., $1/4$ probability for each of A, C, G, T).
   - Using the raw transition counts from the 'A' row of matrix $M$, perform a Chi-square goodness-of-fit test against the expected uniform frequencies.
   - Calculate the p-value.

Output your results to a JSON file at `/home/user/analysis.json` with the exact following keys:
- `"stationary_distribution"`: A list of 4 floats representing $\pi$ for [A, C, G, T].
- `"iterations_to_converge"`: An integer for the number of power iterations performed.
- `"row_A_chi2_pvalue"`: A float representing the p-value of the Chi-square test.

Ensure your code is efficient and accurate.