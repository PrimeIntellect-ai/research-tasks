You are an AI assistant helping a systems compliance officer investigate a severe deadlock incident in a legacy financial database. The incident brought down concurrent transactions, and we need to automatically trace the exact deadlock cycles for regulatory auditing.

You are provided with:
1. `/app/locks.csv`: A very large snapshot of transaction locks at the time of the crash. It has no headers. The columns are `waiting_tx_id, holding_tx_id, timestamp`. This represents a directed edge where `waiting_tx_id` is blocked by `holding_tx_id`.
2. `/app/alert_screenshot.png`: An image of the pager alert received by the compliance officer. 

Your tasks:
1. **Extract the Target:** Use OCR (e.g., `tesseract`, which is preinstalled) on `/app/alert_screenshot.png` to read the target transaction ID that triggered the alert. Look for the text following "AUDIT_NODE:".
2. **Implement an Analyzer in Rust:** Create a new Rust project in `/home/user/deadlock_analyzer`. Write a high-performance Rust application that:
   - Takes three command-line arguments: `<input_csv_path> <target_tx_id> <output_json_path>`
   - Reads the CSV file and constructs a directed dependency graph.
   - Finds the *shortest* deadlock cycle (directed cycle) that includes the `<target_tx_id>`.
   - Projects this cycle and exports it as a strictly formatted JSON array of strings (the transaction IDs in order, starting with `<target_tx_id>`) to the `<output_json_path>`. For example: `["TX_123", "TX_456", "TX_789"]` (do not duplicate the start node at the end of the array).
3. **Performance Requirement:** The graph projection and cycle detection must be heavily optimized. Our automated verifier will run your compiled binary against a massive, hidden graph of 2 million edges. Your program must execute in under 0.5 seconds on this hidden dataset.
4. **Final Deliverable:** Build your Rust project in release mode. Leave the compiled executable at `/home/user/deadlock_analyzer/target/release/deadlock_analyzer`. Run it once on the provided `/app/locks.csv` and write the output to `/app/cycle.json`.