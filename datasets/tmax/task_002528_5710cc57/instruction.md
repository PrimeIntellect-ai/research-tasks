You are a performance engineer analyzing molecular dynamics outputs. We need to rapidly stream and analyze a large PDB (Protein Data Bank) file to compute statistical differences between two spatial domains. 

Your task is to write a highly optimized C program at `/home/user/fast_analysis.c` that does the following:
1. **Bioinformatics Parsing:** Read the file `/home/user/data.pdb` (containing 100,000 `ATOM` records). Extract the X and Z coordinates from standard PDB columns (X: cols 31-38, Z: cols 47-54).
2. **Domain Decomposition:** Divide the atoms into two domains: Domain 1 for atoms where X >= 0.0, and Domain 2 for atoms where X < 0.0.
3. **Linear Equation / Mean Calculation:** Compute the mean Z coordinate for Domain 1 ($\mu_1$) and Domain 2 ($\mu_2$).
4. **Statistical Hypothesis Comparison:** Perform a Z-test to compare the means of the Z coordinates of the two domains. Assume the population variance for both domains is exactly $\sigma^2 = 1.0$. Compute the Z-score using the formula:
   $Z = \frac{\mu_1 - \mu_2}{\sqrt{\frac{1}{n_1} + \frac{1}{n_2}}}$
   where $n_1$ and $n_2$ are the atom counts in Domain 1 and Domain 2, respectively.

Compile your program using `gcc -O3 /home/user/fast_analysis.c -lm -o /home/user/fast_analysis` and run it. 

Your program must write the computed Z-score to `/home/user/stat_result.txt` exactly in this format (rounded to 3 decimal places):
`Z-score: [value]`

Ensure your code is efficient and completes the parsing and calculation in a fraction of a second.