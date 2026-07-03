You are an automation specialist creating a robust ETL data pipeline. A legacy upstream system is aggressively retrying failed batches, resulting in duplicate records in our data stream. Furthermore, the upstream system occasionally suffers from data corruption, injecting malformed or malicious payloads into the data stream.

Your task is to write a fast data sanitization and deduplication filter in C.

**Step 1: Video Analysis for Configuration**
You have been provided a diagnostic video of the upstream server's fault indicator at `/app/fault_log.mp4`. 
Extract the frames of this video. Count the exact number of frames that are completely solid blue (RGB: 0, 0, 255). 
This integer count `N` represents the internal retry window of the upstream system in seconds, which you will need for Step 2.

**Step 2: Write the C Sanitizer**
Create a C program at `/home/user/sanitizer.c` and compile it to an executable at `/home/user/sanitizer`.
The program must read a continuous stream of CSV records from `stdin` and output the processed CSV to `stdout`.

Input CSV Format: `timestamp,vehicle_id,speed,license_plate`
*   `timestamp`: Integer (Unix epoch seconds).
*   `vehicle_id`: Integer.
*   `speed`: Float.
*   `license_plate`: String.

Your C program must perform the following operations in order:
1.  **Validation & Rejection:** Check the `license_plate` field. It must ONLY contain uppercase letters (`A-Z`), digits (`0-9`), and hyphens (`-`). If it contains any other characters (including spaces, lowercase letters, or special characters), **drop the entire record**.
2.  **Rolling Deduplication:** If a valid record has the same `vehicle_id` as a previously seen record, and its `timestamp` is within `N` seconds (inclusive) of the *most recent* accepted record for that `vehicle_id`, **drop the record**. (Assume records are fed mostly in order, but maintain a sufficient history buffer/hash map to track the latest timestamp per `vehicle_id`).
3.  **Data Masking:** For all accepted records, mask the `license_plate` by replacing every character with an asterisk (`*`), *except* for the last two characters, which must remain visible. (e.g., `ABC-1234` becomes `******34`).
4.  **Output:** Print the accepted, masked records to `stdout` in the exact same CSV format.

*Note: Your compiled binary `/home/user/sanitizer` will be automatically tested against a hidden adversarial corpus of "clean" files (which must be processed correctly without dropping valid rows) and "evil" files (which contain SQL injections, buffer overflow attempts, and illegal characters in the license plate, all of which must be dropped safely).*