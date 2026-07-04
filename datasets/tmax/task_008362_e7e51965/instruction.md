You are a data analyst working on an A/B test for an e-commerce platform. You only have access to standard Linux utilities (Bash, awk, sed, grep, join, sort, bc) and must perform the entire analysis without using Python, R, or Perl.

You are given three CSV files located in `/home/user/`:

1. `/home/user/users.csv`
   Columns: `user_id,country,signup_date`
   Contains user demographic data.

2. `/home/user/impressions.csv`
   Columns: `user_id,variant`
   Contains records of which ad variant (`A` or `B`) was shown to each user. (Each user appears exactly once).

3. `/home/user/clicks.csv`
   Columns: `user_id,timestamp`
   Contains records of users who clicked the ad. (A user appears at most once).

Your task is to write and execute a Bash script (`/home/user/analyze.sh`) that performs the following ETL and statistical analysis:

1. **Filter and Join**:
   - Keep only users from the country `US`.
   - Join the US users with the `impressions.csv` data to find out which variant they saw.
   - Join with `clicks.csv` to determine if they clicked the ad (if a `user_id` from the impressions data is present in `clicks.csv`, it's a click).

2. **Compute Summary Statistics**:
   - $N_A$: Total number of US users who saw variant A.
   - $C_A$: Total number of US users who saw variant A and clicked.
   - $P_A$: Click-through rate for variant A ($C_A / N_A$).
   - $N_B$: Total number of US users who saw variant B.
   - $C_B$: Total number of US users who saw variant B and clicked.
   - $P_B$: Click-through rate for variant B ($C_B / N_B$).

3. **Calculate 95% Confidence Interval**:
   - Calculate the difference in proportions: $D = P_A - P_B$
   - Calculate the Standard Error (SE) for the difference of two independent proportions:
     $SE = \sqrt{ \frac{P_A(1 - P_A)}{N_A} + \frac{P_B(1 - P_B)}{N_B} }$
   - Calculate the 95% Confidence Interval limits using the Z-value for 95% confidence (1.96):
     Lower Bound ($LB$) = $D - 1.96 \times SE$
     Upper Bound ($UB$) = $D + 1.96 \times SE$

4. **Output Requirements**:
   - Write the final output to `/home/user/results.txt`.
   - The file must contain exactly these lines with the calculated values rounded to exactly 4 decimal places (using standard rounding, e.g., 0.12345 -> 0.1235). $N_A$, $C_A$, $N_B$, and $C_B$ must be integers.

Format of `/home/user/results.txt`:
```
N_A: [value]
C_A: [value]
P_A: [value]
N_B: [value]
C_B: [value]
P_B: [value]
Diff: [value]
SE: [value]
CI_Lower: [value]
CI_Upper: [value]
```

**Constraints**:
- You must write a script to compute this automatically. Do not manually count lines.
- Only Bash, `awk`, `bc`, `join`, `sort`, `grep` and standard coreutils are permitted.
- The CSV files have headers. Make sure to ignore or strip them during processing.