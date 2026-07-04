You are a performance engineer tasked with debugging a critical analytics pipeline. The system processes high-frequency sensor measurements. Last night, the server experienced a hard crash, leaving our local SQLite database corrupted, though the Write-Ahead Log (WAL) file survived. 

Additionally, before the crash, analysts reported that the variance calculation for the sensor values was outputting `0.0` or occasionally negative numbers, which is mathematically impossible given the data variance.

Your objectives:
1. **Database Recovery**: You have been provided with the remains of the database at `/home/user/sensor.db` and its WAL file `/home/user/sensor.db-wal`. Recover the data and restore it into a new, uncorrupted database file located precisely at `/home/user/recovered.db`.
2. **Numerical Instability Diagnosis & MRE**: The original script calculated sample variance using the standard naive formula: `(sum(x^2) - (sum(x)^2 / N)) / (N - 1)`. The data consists of very large numbers with small fractional differences, causing catastrophic cancellation (numerical instability) in standard floating-point operations. Write a Minimal Reproducible Example (MRE) in Python at `/home/user/mre.py`. This script must:
   - Connect to `/home/user/recovered.db`.
   - Read all `value` entries from the `measurements` table.
   - Calculate the variance using the naive, unstable approach.
   - Calculate the variance using a numerically stable approach (e.g., Welford's algorithm or Python's built-in robust libraries).
3. **Fix and Log Result**: Run your numerically stable calculation on all the `value` rows in the recovered database. Calculate the sample variance (Bessel's correction applied, delta degrees of freedom = 1). Write ONLY the final, stable sample variance, rounded to exactly 4 decimal places, into `/home/user/final_variance.txt`.

Ensure all file paths match exactly. Do not use root privileges.