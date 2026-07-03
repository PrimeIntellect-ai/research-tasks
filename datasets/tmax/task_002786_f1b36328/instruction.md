You are a data engineer debugging an ETL pipeline. We have a daily transaction log file formatted as JSON Lines, representing money transfers between accounts.

The raw data is located at `/home/user/data/logs.jsonl`. 

Your task is to write a purely Bash-based ETL script (using standard tools like `jq`, `awk`, `join`, `sort`, etc.) to perform a graph traversal and aggregation over this NoSQL-style data. 

Specifically, you must:
1. Filter the JSON Lines to include only transactions where `"status"` is exactly `"SUCCESS"`.
2. Treat the successful transactions as directed edges in a graph where `"src"` is the source account, `"dst"` is the destination account, and `"amount"` is the edge weight.
3. Find all valid **2-hop paths** starting from the account `"ROOT"`. A 2-hop path consists of exactly two successful transactions: `ROOT -> X` and `X -> Y`.
4. For each 2-hop path, calculate the total amount transferred (i.e., `amount(ROOT -> X) + amount(X -> Y)`).
5. For each destination account `Y` reachable in exactly 2 hops from `"ROOT"`, find the **maximum** total amount among all possible 2-hop paths from `"ROOT"` to `Y`.
6. Output the results to a CSV file at `/home/user/data/max_2hop.csv` with the format `Destination,MaxTotalAmount`. The file must have a header exactly as shown, and the rows must be sorted alphabetically by the `Destination` account name.

Constraints:
- Do not use Python, Perl, or any non-Bash programming languages. You must rely on standard shell tools (`bash`, `jq`, `awk`, `grep`, `sort`, etc.).
- Ensure your output file `/home/user/data/max_2hop.csv` contains the correct calculations.

Example intermediate logic:
If ROOT -> A (50) and A -> C (20), total = 70.
If ROOT -> B (30) and B -> C (60), total = 90.
The max 2-hop total for C would be 90.