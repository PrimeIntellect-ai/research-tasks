You are a data analyst working with a massive dataset of simulated particle collisions. You need to process a large CSV file, calculate a derived mathematical metric for each particle, filter the results, and generate a summary report.

Because the dataset is large, you must process the data in parallel to save time.

**Environment Details:**
- **Data File:** `/home/user/data/particles.csv`
  - No header row.
  - Columns: `ID, X, Y, Z, Mass`
  - Size: 500,000 rows.
- **Config File:** `/home/user/config.env`
  - Contains two variables: `MULTIPLIER` and `THRESHOLD`.
- **Template File:** `/home/user/report.tmpl`
  - Contains placeholders: `{{THRESHOLD}}`, `{{COUNT}}`, and `{{SUM}}`.

**Your Task:**
1. Read the `MULTIPLIER` and `THRESHOLD` from `/home/user/config.env`.
2. For every row in the CSV, calculate the "Energy" metric using the formula:
   `Energy = Mass * MULTIPLIER * sqrt(X^2 + Y^2 + Z^2)`
3. Process the file using parallel data processing techniques (e.g., streaming chunks into `xargs -P`, `parallel`, or background bash jobs). 
4. Identify all particles where `Energy > THRESHOLD`.
5. Count the number of particles that exceed the threshold.
6. Calculate the sum of the `Energy` for all particles that exceed the threshold.
7. Generate a final report at `/home/user/final_report.md` by reading `/home/user/report.tmpl` and replacing:
   - `{{THRESHOLD}}` with the exact threshold value.
   - `{{COUNT}}` with the number of high-energy particles.
   - `{{SUM}}` with the sum of their energies, **rounded to exactly 2 decimal places** (e.g., `12345.67`).

Write a Bash script (e.g., `process.sh`) to perform these steps and execute it. 
Ensure the resulting `/home/user/final_report.md` is formatted exactly as the template with the correct values.