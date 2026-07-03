You are a bioinformatics analyst examining the GC content distributions from two different sequencing runs of a microbial community. You need to quantify the shift in the GC content profile to assess potential contamination or changes in the community structure.

You have two files containing the empirical probability density functions (PDFs) of the GC fraction for each run:
- `/home/user/run1_gc.tsv`
- `/home/user/run2_gc.tsv`

Both files are tab-separated and have two columns with a header: `GC_Fraction` and `Density`. The `GC_Fraction` values are identical in both files and are sorted in increasing order, but the step size between points may not be perfectly uniform (though they are aligned between the two files).

Your task is to compute the Total Variation Distance (TVD) between the two distributions using the Trapezoidal rule for numerical integration. The formula for the Total Variation Distance between two probability density functions $P(x)$ and $Q(x)$ is:

$$TVD = \frac{1}{2} \int |P(x) - Q(x)| dx$$

**Instructions:**
1. Using Bash and standard command-line text processing utilities (e.g., `awk`, `paste`, `bc`), calculate the integral of the absolute difference between the two densities using the Trapezoidal rule.
2. Multiply the result by 0.5 to obtain the TVD.
3. Write the final calculated TVD to a file named `/home/user/tvd_result.txt`.
4. The output in the file must contain *only* the final number formatted to exactly 4 decimal places (e.g., `0.1234`).

Ensure your method accurately implements the Trapezoidal integration formula:
$$\int f(x) dx \approx \sum_{i=1}^{n-1} \frac{f(x_{i+1}) + f(x_i)}{2} (x_{i+1} - x_i)$$