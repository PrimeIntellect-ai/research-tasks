You are a data analyst investigating a series of financial transactions. You have noticed a complex web of transactions, some of which form hierarchical chains that resemble dependency deadlocks in transaction processing systems. To untangle this, you need to construct a sophisticated data processing pipeline.

You are provided with two CSV files in your home directory:
1. `/home/user/accounts.csv` - Contains the organizational account hierarchy.
   Headers: `id,parent_id,name`
   (Note: `parent_id` is empty for root accounts).

2. `/home/user/transactions.csv` - Contains chronological transfers between accounts.
   Headers: `id,from_id,to_id,amount,ts`

Your task is to write a C++ program at `/home/user/analyze.cpp` that processes these files using an embedded SQLite database (`libsqlite3-dev` is available).

Your C++ program must:
1. Initialize an in-memory SQLite database.
2. Create two tables, `Accounts` and `Transactions`, and populate them with the data from the respective CSV files. Treat `amount` as a REAL and `ts` as a DATETIME or TEXT.
3. Execute a single, complex SQL query (using CTEs, Window Functions, and Joins) that does the following:
   a. Uses a **Recursive CTE** to find all accounts that are descendants of account `id = 1` (including account `1` itself).
   b. Calculates the chronological **rolling balance** for each of these descendant accounts over time based on the transactions. (When an account is `from_id`, its balance decreases by `amount`; when it is `to_id`, its balance increases by `amount`. Assume all balances start at 0).
   c. Uses **Window Functions** and aggregation to determine the **peak (maximum) rolling balance** achieved by each account at any point in its history.
   d. Filters the result to only include accounts whose peak rolling balance is **strictly greater than 1000**.
   e. Joins the results with the `Accounts` table to retrieve the account `name`.
4. Export the final query results to `/home/user/report.csv` with the headers: `account_id,name,max_balance`.
5. The output must be sorted by `max_balance` DESCENDING, and then by `account_id` ASCENDING.

Compile your program using standard tools (e.g., `g++ -std=c++17 /home/user/analyze.cpp -lsqlite3 -o /home/user/analyze`) and run it so that `/home/user/report.csv` is generated. 

Ensure the output CSV is strictly comma-separated without extra spaces, and includes the header row.