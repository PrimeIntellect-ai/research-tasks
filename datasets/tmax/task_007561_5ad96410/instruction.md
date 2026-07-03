You are assisting a compliance officer auditing an internal financial system. You have been provided with a raw log of transactions, but the underlying data model has been lost. You need to reverse-engineer the transaction graph, materialize it in memory, and perform an analytical query to identify suspicious behavior.

The transaction log is located at `/home/user/transactions.txt`. Each line contains space-separated values representing a single transaction:
`TxID Timestamp SenderID ReceiverID Amount`

Write a C program at `/home/user/compliance_check.c` that does the following:
1. **Data Model & Graph Materialization**: Parse the log and build an in-memory directed graph of transactions (Sender -> Receiver). 
2. **Windowed Aggregation**: For each `SenderID`, sort their outgoing transactions chronologically by `Timestamp`. Calculate a "windowed aggregate": the maximum sum of `Amount` across any sliding window of up to 3 consecutive outgoing transactions. If a sender has fewer than 3 transactions, simply sum all of them.
3. **Graph Filtering**: Filter the graph to only include `SenderID`s who have sent transactions to at least 2 *distinct* `ReceiverID`s (out-degree to distinct nodes >= 2).
4. **Sorting and Pagination**: Sort the remaining `SenderID`s by their calculated maximum 3-transaction sliding window sum in descending order. If there is a tie, sort by `SenderID` ascending.
5. **Output**: Write the top 3 results (pagination) to `/home/user/flagged_users.log`.

The output file `/home/user/flagged_users.log` must contain exactly the top 3 senders in the following format:
```
<SenderID> <Distinct_Receivers> <Max_3_Tx_Sum>
```

Constraints:
- Do not use external libraries other than standard C library (`stdio.h`, `stdlib.h`, `string.h`, etc.).
- The C code must compile cleanly with `gcc /home/user/compliance_check.c -o /home/user/compliance_check`.
- Execute your program and ensure `/home/user/flagged_users.log` is generated with the correct contents.