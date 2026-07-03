You are a performance and forensic engineer investigating a faulty distributed billing processor for a cloud service. 
The billing script `/home/user/billing_processor.py` processes log files from different services (Authentication and Data transfer) and calculates the final cost for each user, along with the total revenue.

However, the current script has several bugs that you need to diagnose and fix:
1. **Concurrency Bug**: The script processes multiple log files in parallel using threads to speed up I/O, but it calculates the total revenue incorrectly due to a race condition.
2. **Log Timeline Reconstruction**: The events are not globally sorted by time before being processed. Users are erroneously penalized (charged a $10.00 unauthorized action fee) because their data transfer events are processed before their LOGIN events. You need to ensure all events across all log files are merged and sorted chronologically before the billing logic evaluates them.
3. **Formula Implementation Correction**: The tiered pricing formula for data uploads is implemented incorrectly. The correct formula is:
   - Login fee: $1.50
   - Uploads: $0.05 per MB for the first 100 MB, and $0.02 per MB for any additional MB beyond 100 MB.
   - Downloads: $0.10 per MB flat.
   - The current script has a logic error in calculating the upload cost for amounts over 100 MB.

Your task:
1. Identify and fix the race condition in `/home/user/billing_processor.py`.
2. Fix the log processing logic so all events are correctly sorted by timestamp before calculating user sessions and costs.
3. Correct the upload cost formula.
4. Run the fixed script. It should read logs from `/home/user/logs/` and generate a JSON file at `/home/user/final_billing.json`.

The final JSON file must have the following exact format:
```json
{
  "total_revenue": 123.45,
  "users": {
    "user1": 50.00,
    "user2": 73.45
  }
}
```

Constraints:
- You must write your fixes in Python.
- Do not change the overall parallel file reading architecture (threads), just fix the safety issues.
- You must output to `/home/user/final_billing.json`.