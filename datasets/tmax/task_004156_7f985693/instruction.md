You are a data engineer tasked with building an ETL pipeline to analyze transaction networks. 

We have a dataset of transactions located at `/home/user/transactions.csv`. The file has the following header and format:
`tx_id,timestamp,sender,receiver,amount`

Your goal is to process this data to find the "influence score" of each sender based on a filtered subset of their most significant transactions. 

Please perform the following steps:
1. **Windowed Filtering**: For each `sender`, identify their top 2 transactions based on the `amount` (highest amount first). If there is a tie in the amount, break the tie by choosing the transaction with the lowest `tx_id`.
2. **Graph Analytics**: Treat the filtered transactions as a directed graph where edges go from `sender` to `receiver`. Calculate the "influence score" for each sender, which is defined as their out-degree (the number of **distinct** receivers they sent to) strictly within this filtered graph.
3. **Output**: Save the result to a file named `/home/user/influence_scores.csv` with the header `user,influence_score`. Sort the output in descending order of `influence_score`. If there is a tie in the score, sort by `user` in alphabetical ascending order.

You may use any programming language or command-line tools available in standard Linux environments (Python, bash, awk, sqlite3, etc.) to complete this task. Create and run a script to process the data and generate the output file.