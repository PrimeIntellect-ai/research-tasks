You are a bioinformatics analyst tasked with treating DNA sequences as 1D discrete signals to perform a basic pseudo-spectroscopy analysis. You need to write a Go program that reads a FASTA file, converts the sequences into numerical signals, and calculates specific signal properties using numerical integration and differentiation.

Write a Go program located at `/home/user/process.go` that does the following:

1. **Parse the FASTA file:** Read the file located at `/home/user/sequences.fasta`. A FASTA file contains sequence records, where each record starts with a header line beginning with `>` (e.g., `>seq1`), followed by one or more lines of sequence data (e.g., DNA bases like `A`, `C`, `G`, `T`). Note that a single sequence might be split across multiple lines, which should be concatenated.
2. **Convert to a 1D Signal:** For each sequence, convert the sequence of characters into an array of `float64` values (let's call this signal $S$ of length $N$) using the following mapping:
   - `A` = 1.5
   - `C` = 0.5
   - `G` = -0.5
   - `T` = -1.5
   - Any other character = 0.0
3. **Calculate Signal Energy (Integral):** Compute the definite integral $I$ of the signal $S$ using the trapezoidal rule, assuming a step size of $\Delta x = 1.0$.
   Formula: $I = \sum_{i=0}^{N-2} \frac{S_i + S_{i+1}}{2}$
4. **Calculate Numerical Derivative:** Compute the forward difference numerical derivative $D$ of the signal $S$. The resulting derivative array $D$ will have length $N-1$.
   Formula: $D_i = S_{i+1} - S_i$ for $i=0, 1, \dots, N-2$.
5. **Calculate Variation (Derivative Integral):** Compute the integral $DI$ of the *absolute value* of the derivative $D$ ($|D|$), again using the trapezoidal rule with $\Delta x = 1.0$.
   Formula: $DI = \sum_{i=0}^{N-3} \frac{|D_i| + |D_{i+1}|}{2}$
6. **Output Results:** Your Go program must write the results to a CSV file located at `/home/user/results.csv`.
   - The CSV should have the header: `ID,I,DI`
   - Each subsequent line should correspond to a sequence record in the order they appear in the FASTA file.
   - Extract the `ID` from the FASTA header by removing the leading `>` (e.g., if the header is `>seq1`, the ID is `seq1`).
   - Format the $I$ and $DI$ values to exactly 2 decimal places (e.g., `1.00`, `-0.50`).

To complete the task, compile and run your Go program so that `/home/user/results.csv` is generated successfully.