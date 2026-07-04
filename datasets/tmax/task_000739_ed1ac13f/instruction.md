You are acting as a Database Administrator tasked with building an automated deadlock detection tool for our distributed database system. You have two distinct objectives.

**Objective 1: Video Forensic Analysis**
We have a screen recording of our database monitoring dashboard during a recent outage, located at `/app/db_monitor.mp4`. At some point in the video, the dashboard flashes the text "DEADLOCK_ALERT" along with a transaction ID (e.g., "TX_999"). 
Analyze the video, identify the exact frame number where "DEADLOCK_ALERT" first appears, and extract the associated transaction ID. 
Write the result to `/home/user/video_analysis.json` in this format:
`{"frame_number": <int>, "transaction_id": "<string>"}`

**Objective 2: Deadlock Detector Script**
We need a robust script to detect deadlocks from JSON snapshot exports of our database's lock manager. 
Write a Python script `/home/user/deadlock_detector.py` that takes a single file path as an argument.
The input JSON files contain a document-based representation of transactions and the resource locks they hold or are waiting for.
Schema of input JSON:
```json
{
  "active_transactions": [
    {
      "tx_id": "T1",
      "holds_locks_on": ["Resource_A", "Resource_C"],
      "waiting_for_locks_on": ["Resource_B"]
    }
  ]
}
```
A deadlock occurs if there is a cycle in the waits-for graph (e.g., T1 waits for a resource held by T2, which waits for a resource held by T1). 

Your script must:
1. Parse the JSON.
2. Cross-map this document representation into a relational or graph structure.
3. Use a recursive algorithm (or recursive CTE if using SQLite in-memory) to detect any cycles.
4. Validate the output and print EXACTLY valid JSON to stdout: `{"status": "deadlock"}` if a cycle exists, or `{"status": "clean"}` if no cycle exists.

We will test your script against a hidden adversarial corpus of edge cases (deeply nested transaction trees, transitive waits, self-deadlocks, etc.). Your script must correctly classify 100% of the "evil" (deadlock) scenarios and 100% of the "clean" (deadlock-free) scenarios.