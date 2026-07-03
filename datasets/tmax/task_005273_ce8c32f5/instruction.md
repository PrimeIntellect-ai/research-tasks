You are assisting a compliance officer auditing a company's internal systems. You have been provided with an export of the system's NoSQL access logs in JSONL (JSON Lines) format, located at `/home/user/audit_logs.jsonl`. 

Because this is a NoSQL dump, the schema is somewhat flexible. You will need to inspect the file to understand the exact structure, but generally, each line represents an event.

The compliance officer suspects unauthorized access to financial records and needs a specific summary report. 

Write a Python script to process `/home/user/audit_logs.jsonl` and perform the following analysis pipeline:
1. **Filter** for all events where `action` is "ACCESS" and the `resource.type` is "financial_record".
2. **Aggregate** these events to count the total number of accesses per `user_id`.
3. **Filter** the aggregated results to only include users with 3 or more accesses.
4. **Cross-reference**: For these remaining users, determine if they EVER had an event where `action` was "GRANT" and the `metadata.granted_by` field was exactly `"admin_007"`. (Note: Not all events have a `metadata` block).
5. **Sort** the final list of users by their `access_count` in descending order. If there is a tie, sort by `user_id` in ascending alphabetical order.
6. **Format and Save**: Write the results to `/home/user/suspicious_users.json` strictly adhering to the following JSON schema:

```json
{
  "results": [
    {
      "user_id": "<string>",
      "access_count": <integer>,
      "granted_by_admin_007": <boolean>
    }
  ]
}
```

Ensure your Python script completely generates the `suspicious_users.json` file. The output must be valid JSON matching the exact schema and sorting requirements above.