You are acting as a compliance officer auditing a financial system for suspicious activity. We have exported a snapshot of the transaction network. We suspect there are "transaction deadlocks"—circular funding loops designed to obscure money flows—as well as potential exposure pathways from a known sanctioned entity to our internal accounts.

Your task is to analyze this transaction graph using only Bash and standard Linux command-line utilities (like `awk`, `grep`, `join`, `sort`, etc.). You must write a shell script at `/home/user/audit_graph.sh` that processes `/home/user/transactions.csv`.

**Data Format:**
The file `/home/user/transactions.csv` has the following CSV format (with a header):
`tx_id,src_account,dst_account,amount,timestamp`

**Objectives:**
1. **Detect 3-Node Cycles (Transaction Deadlocks):** Find all exact 3-node transaction cycles (where Account A sends to Account B, Account B sends to Account C, and Account C sends back to Account A). Record the sorted list of accounts involved in any such 3-node cycle.
2. **Shortest Path Exposure:** Find the shortest path distance (number of edges) from the sanctioned account `ACC_888` to the executive account `ACC_001`. (Assume all edges are directed and have a weight of 1).

**Output Requirements:**
Your script `/home/user/audit_graph.sh` must execute without user interaction and produce a report file at `/home/user/compliance_report.txt` with exactly the following format:

```text
CYCLES:
<comma-separated list of account IDs involved in 3-node cycles, sorted alphabetically>
EXPOSURE_DISTANCE:
<integer representing the shortest path distance from ACC_888 to ACC_001>
```

For example, if the cyclic accounts are ACC_010, ACC_011, and ACC_012, and the distance from ACC_888 to ACC_001 is 4, the output should be:
```text
CYCLES:
ACC_010,ACC_011,ACC_012
EXPOSURE_DISTANCE:
4
```

Make sure your script `audit_graph.sh` has executable permissions. You may create temporary files in `/home/user/` during your script's execution if needed. Do not use Python, Perl, or any other scripting languages; stick strictly to Bash and coreutils/awk/sed.