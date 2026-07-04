Wake up! It's 3:00 AM and you've just been paged. 

The nightly financial reconciliation job for the `recon-service` is completely broken. It's supposed to aggregate the balances of all our client accounts and their sub-accounts, but it's currently failing in multiple ways. 

Here is the situation reported by the L1 support team:
1. The service is currently hanging and timing out. The logs in `/home/user/app/logs/crash.log` show a massive stack trace from an earlier run that ended in a stack overflow.
2. Even when the developers tried to manually exclude certain accounts to bypass the crash, the final aggregated total was failing audit. The calculated total was off by a few fractions of a cent, which violates strict accounting rules.
3. The L1 team also noticed that the total included transactions that were still marked as 'PENDING', which violates our business logic.

Your environment is set up in `/home/user/app`.
The project is a Go module containing:
- `main.go`: The entry point (do not modify).
- `aggregator.go`: Contains the financial aggregation logic and recursion hierarchy.
- `db.go`: Contains the database querying logic.
- `data.db`: A local SQLite database containing the `accounts` and `transactions` tables.

Your task is to debug and fix the system so that it produces the perfectly accurate sum of all valid transactions.

Requirements:
1. **Loop Termination:** Diagnose and fix the infinite recursion / stack overflow issue in `aggregator.go`. Our account structure allows parent-child relationships, but there seems to be dirty data causing a cycle. Your code must detect and break cycles.
2. **Precision Loss:** The current aggregation uses `float32`, causing floating-point inaccuracies. You must modify the aggregation logic in `aggregator.go` to use exact integer arithmetic (cents) for accumulation. The database stores amounts in dollars (e.g., `10.50`). Convert these to cents (`int64`), sum them, and return the final dollar amount as a string formatted to two decimal places.
3. **Query Debugging:** Fix the query in `db.go` so that it ONLY fetches transactions where the `status` is `'SETTLED'`.

Once you have fixed the code, compile and run the application:
```bash
cd /home/user/app
go build -o recon-service .
./recon-service > /home/user/app/result.txt
```

The automated verification will check `/home/user/app/result.txt` for the exact expected string output (e.g., `Total: 12345.67`). Ensure there are no extra spaces or debug lines in `result.txt`—just the final "Total: X.YY" output.