You are acting as a technical assistant to a compliance officer auditing an internal trading system for a security incident. You need to complete three main objectives:

**Objective 1: Audio Artifact Extraction**
A whistleblower left an automated voicemail on our compliance hotline detailing the incident. The audio file is located at `/app/whistleblower.wav`. 
You must transcribe this audio file to find the specific "Target Employee ID" mentioned in the report.

**Objective 2: Cross-Query Aggregation & Schema Validation**
Using the Target Employee ID identified in the audio, you must aggregate data from two different data sources to build an audit profile.
1. **Relational Database**: A SQLite database at `/app/trading/users.db` contains two tables: `employees` (employee_id, name, department_id) and `departments` (department_id, department_name, risk_level). You need to perform a join to extract the employee's name, department name, and risk level.
2. **NoSQL Datastore**: A collection of trade execution logs is stored as a JSONL file at `/app/trading/executions.jsonl`. You must simulate a NoSQL aggregation pipeline to calculate the `total_trade_volume` (sum of the `amount` field) and count the `number_of_flagged_trades` (where the boolean field `is_flagged` is true) for this specific employee.

Write a script (in Python, Node.js, or your preferred language) that performs this cross-query aggregation. The script must generate a final JSON report saved to `/home/user/audit_report.json`. This output MUST strictly validate against the following schema requirements:
- `employee_id` (string)
- `name` (string)
- `department_name` (string)
- `risk_level` (integer)
- `total_trade_volume` (float)
- `number_of_flagged_trades` (integer)

**Objective 3: Adversarial Payload Validator**
The internal API endpoint used to query these logs has been under attack. We need a payload validator to block malicious parameterized query payloads.
Create an executable script at `/home/user/query_validator.py`. 
- The script should accept a file path as its first CLI argument.
- The file will contain a JSON object representing a query payload.
- Your script must parse the JSON and analyze the string values inside the `filters` object for common SQL injection patterns (e.g., `' OR '1'='1`, `UNION SELECT`, `--`, `; DROP`).
- If the payload is malicious (contains SQLi), the script must print "REJECT" and exit with status code `1`.
- If the payload is clean, the script must print "ACCEPT" and exit with status code `0`.
- The verifier will test your script against two distinct corpora of payloads: an evil corpus containing malicious queries, and a clean corpus containing legitimate complex queries.