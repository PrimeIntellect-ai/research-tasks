You are a data engineer investigating a series of complex financial transactions that resemble transaction deadlocks or circular money laundering schemes. Your data is split across a relational database (SQLite) and NoSQL exports (JSON Lines). 

You need to build an ETL and analytics script that maps these distinct data sources together, models them as a graph, and identifies fraudulent cycle patterns.

**Data Sources:**
1. **Relational Database**: `/home/user/data/financial.db` (SQLite3)
   - Table `users`: `user_id` (TEXT), `name` (TEXT)
   - Table `accounts`: `account_id` (TEXT), `user_id` (TEXT)
   *(Note: A single user can own multiple accounts.)*

2. **NoSQL Export**: `/home/user/data/transactions.jsonl`
   - A JSON Lines file where each line is a transaction.
   - Format: `{"tx_id": "t1", "from_account": "a1", "to_account": "a2", "amount": 100.0, "currency": "USD"}`

**Your Objective:**
Write a script in the language of your choice that processes this data to find all circular transaction chains of length exactly 3 at the **user level**. 

A user-level 3-cycle occurs when:
User A sends money to User B.
User B sends money to User C.
User C sends money to User A.
*(Note: These transfers can occur across any accounts owned by these users. Ensure A, B, and C are distinct users.)*

For each 3-cycle found:
1. Identify the three users involved by their `name`.
2. Calculate the total aggregate `amount` of the transactions that make up this specific cycle (the sum of the A->B, B->C, and C->A transactions). If multiple transactions exist between the same accounts, treat each distinct 3-transaction combination that forms a cycle as a separate cycle.

**Output Requirements:**
Create a JSON file at `/home/user/output/fraud_cycles.json`.
The file should contain a single JSON array of objects, where each object represents a detected 3-cycle.
Format:
```json
[
  {
    "users": ["Alice", "Bob", "Charlie"],
    "total_amount": 450.5
  }
]
```
- The `users` array in each object **must be sorted alphabetically** (e.g., `["Alice", "Bob", "Charlie"]`).
- The outer JSON array of cycles must be **sorted by `total_amount` in descending order**. If there's a tie, sort by the first username in the `users` array alphabetically.
- Eliminate duplicate cycles (i.e., A->B->C->A is the same cycle as B->C->A->B, it should only appear once in the final output).

Ensure the output directory exists before writing the file.