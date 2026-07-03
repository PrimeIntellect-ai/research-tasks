You are tasked with writing a Bash script that processes a CSV file containing numerical count data (representing multi-dimensional arrays of categorical counts) and calculates a probability distribution distance metric. A previous data scientist attempted this but their pipeline kept failing with infinite values because of near-singular inputs (zero counts).

Your task is to write a script at `/home/user/jsd_matrix.sh` that:
1. Takes a single argument: the path to a CSV file (e.g., `/home/user/data_matrix.csv`). Each row contains comma-separated non-negative numbers representing counts of different categories.
2. The first row (Row 1) is the reference distribution.
3. For every subsequent row (Row 2 to N), compute the Jensen-Shannon Divergence (JSD) between the reference distribution (Row 1) and the current row.
4. **Laplace Smoothing:** To fix the near-singular input issue, add a pseudo-count of exactly `0.01` to every single cell in the matrix *before* calculating the probabilities.
5. Normalize each smoothed row so that it sums to 1.0. Let $P$ be the probability distribution of Row 1, and $Q$ be the probability distribution of the current row (Row $k$).
6. Calculate the JSD using the natural logarithm:
   $M_i = 0.5 \times (P_i + Q_i)$
   $JSD(P, Q) = 0.5 \times \sum ( P_i \times \ln(P_i / M_i) ) + 0.5 \times \sum ( Q_i \times \ln(Q_i / M_i) )$
7. **Analytical Validation:** If the calculated JSD is $\le 0.1$, it is considered `VALID`. If $JSD > 0.1$, it is `INVALID`.
8. Write the output to `/home/user/jsd_output.txt`. For each comparison, output a line in the format:
   `Row_<k>: <JSD> <VALID/INVALID>`
   where `<k>` is the row number (starting at 2), and `<JSD>` is formatted to exactly 6 decimal places.

Example output format in `/home/user/jsd_output.txt`:
```
Row_2: 0.000000 VALID
Row_3: 0.453210 INVALID
```

You must implement this logic in the Bash script (you may use `awk` heavily, which is standard in Bash processing). The script should be executable. 
To test your script, create a mock CSV file at `/home/user/data_matrix.csv` with some test counts, run your script, and ensure the output matches the required format.