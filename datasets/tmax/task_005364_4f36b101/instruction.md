You are a data analyst investigating potential financial fraud rings. You have been given two CSV dumps of relational data representing accounts and transactions. You need to map this relational data into a graph representation in C++ to find specific cyclic patterns.

The files are located at:
1. `/home/user/accounts.csv`
Format: `account_id,created_at,status`
2. `/home/user/transactions.csv`
Format: `tx_id,src_account,dst_account,amount,tx_date`

Your task is to write a standard C++17 program (`/home/user/find_cycles.cpp`) that reads these files, processes the data as a directed graph, and identifies specific "triangles" (cycles of exactly length 3, i.e., A -> B -> C -> A). 

A valid fraud cycle must meet ALL of the following conditions:
1. It involves exactly 3 distinct accounts forming a closed loop (A -> B -> C -> A).
2. All three accounts in the cycle must have the status `ACTIVE`.
3. At least one account in the cycle must have been created strictly after `2023-01-01`.
4. The total transaction volume of the cycle must be strictly greater than `10000.0`. 
   *Note on volume calculation:* If there are multiple transactions from Account X to Account Y, use ONLY the maximum single transaction amount from X to Y when calculating the cycle's total volume. (e.g., Volume = Max(A->B) + Max(B->C) + Max(C->A)).

Your program should output the detected cycles to a log file at `/home/user/fraud_cycles.log`.
Formatting rules for `/home/user/fraud_cycles.log`:
- One cycle per line.
- For each cycle, print the three `account_id`s separated by a single space.
- The three `account_id`s on each line must be sorted lexicographically (e.g., `ACC1 ACC2 ACC3`).
- If there are multiple cycles, sort the lines lexicographically based on the first account ID, then the second, then the third.
- If no cycles match the criteria, leave the file empty.

Compile your code using `g++ -std=c++17 -O3 /home/user/find_cycles.cpp -o /home/user/find_cycles` and execute it to generate the log file. Do not use any external non-standard libraries (like Boost) - rely only on the C++ Standard Library.