You are an incident responder investigating a suspected privilege escalation on a Linux server. 

A snapshot of the relevant files has been placed in `/home/user/investigation/`. 
Your tasks are to:
1. Scan the directory `/home/user/investigation/bin/` to identify a binary that has the SUID (Set Owner User ID) permission bit set.
2. Parse the security log at `/home/user/investigation/auth.log` to find the exact timestamp when this specific SUID binary was executed. The log format contains the execution event in a line containing `custom_suid_audit`.
3. Calculate the SHA256 checksum of the identified SUID binary.
4. Check if the calculated SHA256 hash matches the baseline hash recorded for this file in `/home/user/investigation/hashes.sha256`.

Once you have gathered this information, create a report file at `/home/user/report.txt` with exactly the following three lines (replace the placeholder values with your findings):

```
BINARY=<full_path_to_the_suid_binary>
TIMESTAMP=<Timestamp from the log, e.g., 'Jul 14 12:34:55'>
HASH_MATCH=<TRUE or FALSE>
```

Constraints:
- Do not modify the original log or binary files.
- The `TIMESTAMP` value should only include the Date and Time (e.g., "Jul 14 12:34:55").
- The `HASH_MATCH` value must be strictly `TRUE` if the computed hash matches the one in `hashes.sha256`, or `FALSE` if it does not match.