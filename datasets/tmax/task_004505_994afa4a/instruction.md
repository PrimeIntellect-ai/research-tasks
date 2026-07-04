You are acting as a compliance officer auditing an internal database platform. A recent security incident occurred where audit logs were tampered with. We have two tasks for you to complete to secure the system and identify the attacker.

**Part 1: Video Evidence Analysis**
During the incident, an administrator was screen-recording their dashboard. The recording is saved at `/app/audit_session.mp4`. This video shows a scrolling execution log of database queries.
Your task is to analyze this video to find the exact `SESSION_ID` of the user who executed a `DROP TABLE` command against the `compliance_records` table.
Extract the frames, perform OCR (e.g., using `tesseract`), and find the session ID. 
Write the extracted session ID (just the string value, e.g., `A1B2C-3D4E5`) to `/home/user/malicious_session.txt`.

**Part 2: Query Audit Filter (Adversarial Corpus)**
The attacker exploited missing tenant isolation in our NoSQL analytics engine. We need to implement a strict query filter. 
We have extracted a sample of known-good queries to `/app/corpus/clean/` and known-malicious queries to `/app/corpus/evil/`. These files contain JSON representations of MongoDB aggregation pipelines.

By analyzing the structure of the `clean` vs `evil` pipelines, deduce the compliance rules. (Hint: Look closely at how `$match` stages are used for tenant isolation, and which collections are accessed in `$lookup` stages).

Create a bash script at `/home/user/query_auditor.sh` that takes a JSON file path as its first and only argument.
Your script must use standard CLI tools (like `jq`, `grep`, `awk`) to analyze the JSON pipeline.
- If the pipeline is compliant (clean), the script MUST exit with code 0.
- If the pipeline is non-compliant (evil), the script MUST exit with code 1.

Ensure your script is executable (`chmod +x /home/user/query_auditor.sh`). The automated test suite will run your script against a hidden holdout set of clean and evil queries.