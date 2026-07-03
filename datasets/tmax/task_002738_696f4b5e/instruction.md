You are a DevOps engineer analyzing server latency logs after a severe system crash. 

The system was running a metrics collection service that saved request latencies to a SQLite database. During the power failure, the database file at `/home/user/metrics.db` became corrupted. 

We have a Bash script located at `/home/user/calc_metrics.sh` that is supposed to extract the latencies from this database and compute the sample variance of the `latency` column in the `requests` table.

However, there are two issues you must solve:
1. **Database Corruption**: The script currently fails because `/home/user/metrics.db` is corrupted. You need to perform forensic recovery on the database to extract the raw data and recreate a healthy database at `/home/user/recovered_metrics.db`.
2. **Numerical Instability**: The `/home/user/calc_metrics.sh` script currently uses a naive, single-pass formula to calculate the variance (`E[x^2] - (E[x])^2`) via `awk`. Because the baseline timestamps/latencies are extremely large numbers with small variations, this naive formula suffers from catastrophic cancellation (floating-point precision limits), resulting in a calculated variance of 0 or a wildly incorrect number. 

Your task:
1. Recover the database and save the healthy version to `/home/user/recovered_metrics.db`.
2. Diagnose and fix the formula implementation in `/home/user/calc_metrics.sh` so it points to the recovered database and calculates the sample variance using a numerically stable algorithm (such as Welford's online algorithm or a two-pass algorithm).
3. Run the fixed script. The script must output ONLY the final calculated sample variance, formatted to exactly two decimal places, into `/home/user/variance_report.txt`.

Ensure all operations are done within `/home/user`. Do not use root/sudo privileges.