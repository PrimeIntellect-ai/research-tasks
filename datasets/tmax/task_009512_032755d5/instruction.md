You are an AI assistant acting as a bioinformatics analyst. Your task is to process two DNA sequence files, calculate a statistical distance metric between their nucleotide distributions, and use that distance to solve a nonlinear equation modeling a hypothetical mutation parameter.

You have been provided with two FASTA files:
1. `/home/user/data/seq1.fasta`
2. `/home/user/data/seq2.fasta`

Write a C program that performs the following steps:
1. **Parse the FASTA files**: Read both files and calculate the occurrence of each of the four standard DNA bases (A, C, G, T) for each sequence. Ignore any characters that are not A, C, G, or T (e.g., ignore whitespace, newlines, and FASTA header lines starting with '>'). Ignore case.
2. **Calculate Probability Distributions**: Convert the counts into discrete probability distributions $P$ (for `seq1.fasta`) and $Q$ (for `seq2.fasta`). For example, $P(A) = \text{count}(A) / \text{total\_bases}$.
3. **Calculate Bhattacharyya Distance**: Compute the Bhattacharyya distance ($D_B$) between distributions $P$ and $Q$. The formula is:
   $D_B = -\ln \left( \sum_{i \in \{A,C,G,T\}} \sqrt{P(i) \cdot Q(i)} \right)$
4. **Solve Nonlinear Equation**: The distance $D_B$ is related to a mutation factor $k$ by the nonlinear equation:
   $k^3 + 2k - D_B = 0$
   Implement a numerical method (e.g., Newton-Raphson or Bisection) in your C program to find the single real root $k$ for this equation. Start your search around $k=0$.

**Requirements:**
- Save your C code as `/home/user/analyze.c`.
- Compile it to an executable named `/home/user/analyze` (ensure you link the math library with `-lm`).
- Run your program and have it output the final results to `/home/user/analysis_result.txt` in the EXACT format below (all floating-point values rounded to 6 decimal places):

```
Seq1 Dist: A=0.000000, C=0.000000, G=0.000000, T=0.000000
Seq2 Dist: A=0.000000, C=0.000000, G=0.000000, T=0.000000
Bhattacharyya Distance: 0.000000
Mutation Factor k: 0.000000
```
*(Replace `0.000000` with the actual calculated values)*

Ensure the entire workflow is completed using the Linux terminal and C.