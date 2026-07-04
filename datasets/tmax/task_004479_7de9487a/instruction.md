We are experiencing cascading deadlocks in our distributed transaction coordinator. We have a reference binary that detects these deadlocks and selects a victim transaction to abort, but we need to migrate this logic to a maintainable script that we can embed in our monitoring stack. 

You need to write a program that acts as a deadlock detector, mimicking the exact behavior of our compiled oracle.

Here is what you need to do:
1. Examine the whiteboard notes saved at `/app/system_notes.png`. You will need to extract the `DEADLOCK_THRESHOLD_MS` value written on it. You can use `tesseract` to read the image.
2. Create an executable entry point at `/home/user/detector.sh`. This script can be written in Bash, Python, or a combination, but it must read a CSV from `stdin`.
3. The CSV will have no header and contains four columns: `tx_id` (integer), `waits_on_tx_id` (integer), `wait_duration_ms` (integer), and `tx_priority` (integer). This represents a directed graph of transactions waiting on locks held by other transactions.
4. Your script must process this graph to find deadlocks (cycles). A dependency edge is only active if `wait_duration_ms > DEADLOCK_THRESHOLD_MS` (the value you extracted from the image).
5. For every independent cycle detected among the active edges, you must select exactly one victim transaction to abort.
   - The victim is the transaction in the cycle with the **lowest** `tx_priority`.
   - If there is a tie in priority, select the transaction with the **shortest** `wait_duration_ms`.
   - If there is still a tie, select the transaction with the **highest** `tx_id`.
6. Output the `tx_id` of the selected victims, one per line, sorted in ascending numerical order. Do not output anything else.

To ensure your script is correct, it must be perfectly bit-exact equivalent to the reference implementation located at `/app/reference_detector` for any valid input graph. We will verify your script by fuzzing both your `detector.sh` and the reference binary with hundreds of random graphs.