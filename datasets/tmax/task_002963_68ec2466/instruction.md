You are an AI assistant helping a compliance officer audit a financial network for potential money laundering. The officer suspects that malicious actors are using circular transaction loops to obfuscate funds.

You have been provided a dataset of transactions in `/home/user/transactions.csv`. The file has the following columns: `tx_id, sender, receiver, amount, timestamp` (where timestamp is in `YYYY-MM-DD` format).

Your task is to write a Python script (save it anywhere, but run it to produce the final output) that performs the following analysis:
1. **Knowledge Graph Pattern Matching**: Identify all directed 3-cycles of accounts (e.g., an account sequence A -> B -> C -> A where transfers exist in those directions).
2. **Data Pipeline & Filtering**: For each identified 3-cycle, extract all transactions where *both* the sender and the receiver are members of that specific 3-cycle.
3. **Windowed Aggregation**: For these isolated transactions of each 3-cycle, calculate the maximum rolling 7-day sum of transaction amounts. A 7-day window starting on date `D` includes all transactions from date `D` up to `D + 6 days` (inclusive).
4. **Flagging**: If the maximum 7-day rolling sum for a 3-cycle is strictly greater than `10000`, the cycle must be flagged.

Write the flagged 3-cycles to a file named `/home/user/flagged_cycles.csv`. 
The file should have no header and follow this exact format for each flagged cycle:
`Account1,Account2,Account3,Max_7_Day_Sum`

Rules for the output file:
- The three accounts in each row must be sorted alphabetically (e.g., `A,B,C` not `B,A,C`).
- The rows should be sorted alphabetically by the first account name.
- The `Max_7_Day_Sum` should be an integer.

You must write and execute the Python code to process the data and generate `/home/user/flagged_cycles.csv`.