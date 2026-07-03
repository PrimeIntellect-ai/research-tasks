You are an operations engineer triaging an incident with our data ingestion pipeline. A recent power failure corrupted our primary SQLite database, and simultaneously, a sensor calibration error caused it to record baseline values off by a billion.

Your objectives:
1. **Database Recovery**: The SQLite database located at `/home/user/sensor.db` has a corrupted file header. It contains a single table `measurements` with a column `value` (REAL). Recover the data from this corrupted database. Extract the reconstructed SQL schema and data dump to `/home/user/recovered.sql`.
2. **Numerical Instability Diagnosis & Fix**: We need to compute the *sample variance* of the values in the recovered database. Because the sensor recorded values around 1,000,000,000 with very small variations, our legacy scripts using the naive variance formula ($E[X^2] - (E[X])^2$) suffer from catastrophic cancellation and incorrectly output `0.0` or negative numbers. 
3. Write a short script in the language of your choice (Python, Perl, Ruby, etc.) to read the recovered values and compute the true sample variance using a numerically stable method (e.g., Welford's algorithm or a robust built-in library function).
4. **Final Output**: Save the correctly computed sample variance to `/home/user/variance.txt`, formatted to exactly 4 decimal places (e.g., `0.1234`).

Please use the terminal to perform the recovery, write your calculation script, and produce the requested output files.