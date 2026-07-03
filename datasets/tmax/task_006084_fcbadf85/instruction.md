You are a bioinformatics analyst tasked with analyzing the local GC-content profiles of a set of DNA sequences to find optimal regions for primer design and to statistically compare wild-type (WT) vs. mutant (MUT) sequences.

A dataset of sequences is located at `/home/user/sequences.csv`. The CSV has no header and contains rows in the format: `SequenceID,Type,DNA_Sequence`. All sequences are exactly 100 bases long. Types are either `WT` or `MUT`.

Your task is to write a C program that processes this file to perform the following:
1. **Sliding Window GC-content**: For each sequence, calculate the GC-proportion $p_i$ in a sliding window of size $W=10$. The window index $i$ ranges from $0$ to $90$. $p_i$ is the number of 'G' or 'C' bases in the substring from index $i$ to $i+9$ (inclusive) divided by 10.0.
2. **Numerical Differentiation (Primer Boundary)**: For the sequence with ID `SEQ1`, calculate the forward difference $d_i = p_{i+1} - p_i$ for $i \in [0, 89]$. Find the smallest index $i$ that maximizes $d_i$. This represents the sharpest transition into a GC-rich region.
3. **Numerical Integration (Stability Index)**: For every sequence, compute the total stability index $S$ by integrating the GC-profile $p_i$ over the 91 windows using the Trapezoidal rule: 
   $S = \sum_{i=0}^{89} \frac{p_i + p_{i+1}}{2}$
4. **Statistical Hypothesis Comparison**: Compute the sample mean ($\mu$) and sample variance ($s^2 = \frac{1}{N-1}\sum (x_k - \mu)^2$) of the stability index $S$ for the WT group and the MUT group separately. Then, compute the Z-statistic (Welch's t-statistic format) to compare them:
   $Z = \frac{\mu_{WT} - \mu_{MUT}}{\sqrt{\frac{s^2_{WT}}{N_{WT}} + \frac{s^2_{MUT}}{N_{MUT}}}}$

Write your C code to `/home/user/analyze_seq.c`.
Compile it and run it. The program must write its results to `/home/user/analysis_output.txt` with exactly the following format (values rounded to 4 decimal places, index as an integer):

```
WT_MEAN_INTEGRAL: <value>
MUT_MEAN_INTEGRAL: <value>
Z_STATISTIC: <value>
SEQ1_MAX_DERIVATIVE_INDEX: <value>
```

Constraints:
- Only use standard C libraries (`stdio.h`, `stdlib.h`, `string.h`, `math.h`).
- Do not use any external bioinformatics libraries.