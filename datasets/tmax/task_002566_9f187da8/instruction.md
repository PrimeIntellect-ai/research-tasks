You are an integration developer responsible for testing and migrating our legacy API gateways to a new microservices architecture. 

We are introducing a new validation and schema migration layer. You must write a Bash script at `/home/user/api_filter.sh` that acts as a strict filter and transformer for incoming webhook requests. 

The script must take a single argument: the path to an incoming JSON file.
Example invocation: `/home/user/api_filter.sh request.json`

The incoming JSON files have the following structure:
```json
{
  "auth_token": "TOK-9a8b7c6d",
  "base_record": {
    "user_id": 1042,
    "role": "editor",
    "profile": {
      "status": "active"
    }
  },
  "record_patch": [
    { "op": "replace", "path": "/role", "value": "admin" }
  ]
}
```

Your script must perform the following pipeline in order. If any step fails or violates a rule, the script MUST immediately exit with a non-zero exit code (e.g., `exit 1`) and produce no output to standard out.

1. **Token Validation**: Extract the `auth_token` and validate it using the proprietary legacy validator tool provided at `/app/legacy_validator`. This is a stripped binary that we do not have the source code for. It takes the token as its first argument (e.g., `/app/legacy_validator TOK-9a8b7c6d`). If the binary returns a non-zero exit code, the token is invalid and you must reject the request.

2. **Patch Processing**: Extract the `record_patch` (which strictly follows RFC 6902 JSON Patch format) and apply it to the `base_record`. You may use Python, Perl, or Ruby one-liners invoked from within your Bash script to apply the patch (e.g., using the `jsonpatch` library if you install it, or writing your own minimal patch applier for standard ops).

3. **Security Check**: After the patch is applied, verify that the resulting record does NOT have the `role` set to `"admin"`. Any request attempting to escalate privileges to "admin" must be rejected.

4. **Schema Migration**: Transform the patched record into the new v2 schema:
   - Rename `user_id` to `account_uuid` (convert the integer to a string formatted as `UUID-<integer>`, e.g., `UUID-1042`).
   - Flatten the `profile` object. The `status` field inside `profile` should be moved to the root level of the record, and the `profile` object should be removed.
   - If `status` is `"active"`, change it to the boolean `true`. If `"inactive"`, change it to `false`.

5. **Output**: If the payload passes all checks and is successfully transformed, print the final v2 JSON record to `stdout` and exit with code `0`.

Ensure your script handles malformed JSON gracefully by rejecting it. Make sure `/home/user/api_filter.sh` is executable. You can use standard Linux utilities (`jq`, `python3`, etc.).