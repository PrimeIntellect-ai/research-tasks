You are a compliance officer auditing an older, undocumented permissions system. 

We have a legacy compiled binary located at `/app/legacy_audit` that calculates an "Access Exposure Score" for a given user. You pass it a User ID as a command-line argument, and it connects to the local SQLite database at `/home/user/audit.db` to print a single integer representing the exposure score.

Example:
`/app/legacy_audit 42` -> Outputs a number (e.g., `150`)

We suspect the binary is returning wildly incorrect (inflated) results due to a poorly written SQL query containing an implicit cross-join somewhere in its hierarchical role-resolution logic. However, for compliance reporting and backwards compatibility in our migration pipeline, we need to replicate this *exact* calculation bug-for-bug in Python.

Your task is to write a Python script at `/home/user/audit_repro.py` that takes a single user ID as a command-line argument (`sys.argv[1]`) and prints the exact same integer output as the `/app/legacy_audit` binary. 

Your script should:
1. Connect to `/home/user/audit.db`.
2. Execute the exact same (flawed) hierarchical query logic as the binary. 
3. Print only the resulting integer to standard output.

You may analyze the database schema and reverse-engineer, trace, or inspect the `/app/legacy_audit` binary using standard Linux tools to understand what query it is running under the hood. 

Ensure your Python script cleanly handles the user ID parameter and executes deterministically.