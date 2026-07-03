**URGENT: 3AM PagerDuty Alert**
**Service:** ForensicLogAnalyzer
**Incident:** Production pipeline stalled; 100% CPU utilization detected.

You are the on-call engineer. The `ForensicLogAnalyzer` C++ service, which parses incoming endpoint telemetry to calculate threat risk scores, has completely stalled. It appears to be stuck in an infinite loop while processing the latest batch of logs at `/home/user/forensics/data/batch_42.csv`.

Furthermore, before the service stalled, the security team reported that the risk scores calculated for earlier entries were mathematically incorrect, severely skewing our dashboards.

Your tasks:
1. Navigate to `/home/user/forensics`. You will find `analyzer.cpp`, a `Makefile`, and the data directory.
2. **Isolate and Fix the Hang:** Use debugging techniques (e.g., delta debugging/test minimization on the CSV, or codebase inspection) to find out why the parser is hanging. Fix the infinite loop / recursion termination bug in `analyzer.cpp`.
3. **Fix the Scoring Formula:** The risk score is supposed to be calculated using the formula:
   `RiskScore = (BaseScore * 0.6) + ((EventCount / TimeWindow) * 0.4)`
   There is a bug in the implementation of this formula in `analyzer.cpp` causing inaccurate integer truncation. Fix it so the precision is maintained (returns a correct `double`).
4. Recompile the service using `make`.
5. Run the service on the failing log file: `./analyzer data/batch_42.csv /home/user/forensics/results.csv`

The final output must be written to `/home/user/forensics/results.csv`.