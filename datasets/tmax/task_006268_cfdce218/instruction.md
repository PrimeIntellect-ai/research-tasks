Wake up, you're on call! It's 3 AM and our critical Fraud Detection pipeline just went down. 

A junior engineer panicked and accidentally deleted the incoming data file (`/home/user/data/transactions.csv`), and now the emergency hotfix build is failing. We need you to recover the system, fix the build, correct a numerical bug, and generate the final report.

Here is what you need to do:

1. **Recover the Data**: The file `/home/user/data/transactions.csv` was deleted, but a stalled background process named `data_streamer.py` still holds it open. Find the file descriptor and recover the contents to `/home/user/recovered_transactions.csv`.
2. **Handle Corrupted Input**: The recovered data contains a few corrupted lines with null bytes (`\x00`) due to network glitches. Filter out any line containing null bytes and save the clean data to `/home/user/clean_transactions.csv`.
3. **Fix the Build**: The local Python package `/home/user/fraud_analyzer` is failing to install. Diagnose the build failure in the source code (there is a syntax error in `metrics.py`), fix it, and install the package using `pip install -e /home/user/fraud_analyzer`.
4. **Fix the Numerical Instability**: The function `calculate_variance` in `/home/user/fraud_analyzer/metrics.py` is implemented using a naive variance formula ($E[X^2] - (E[X])^2$). Because the transaction amounts are very large, this suffers from catastrophic cancellation, resulting in negative or zero variance. Rewrite the `calculate_variance` function to be numerically stable (you may use the standard library's `statistics.variance` or `statistics.pvariance`).
5. **Generate the Report**: Run the pipeline by executing `python /home/user/fraud_analyzer/run.py --input /home/user/clean_transactions.csv --output /home/user/report.json`.

**Verification Constraints**:
- `/home/user/clean_transactions.csv` must contain only valid text lines.
- The package `fraud_analyzer` must be successfully installed.
- `/home/user/report.json` must be generated successfully and contain the correct, numerically stable variance of the transaction amounts.

Work fast. The company is losing money every minute this pipeline is down!