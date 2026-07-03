You are an expert database administrator and C developer. We are processing CSV files containing financial transfer requests. When these transfers are loaded concurrently into our graph database (Neo4j) using Cypher, we frequently encounter transaction deadlocks. 

This happens because concurrent transactions attempt to lock the same `Account` nodes in different orders (e.g., Transaction 1 locks Account A then Account B; Transaction 2 locks Account B then Account A).

To prevent this, you need to write a C program that acts as a query-to-pipeline chain tool. It will read CSV data, optimize the execution plan by establishing a strict locking order, and output safe Cypher queries.

An image containing the required Cypher query template and the specific node alias naming convention has been provided at `/app/cypher_template.png`. You must extract this template (you can use `tesseract`). 

Your task:
1. Extract the Cypher query structure from `/app/cypher_template.png`.
2. Write a C program at `/home/user/query_builder.c` and compile it to `/home/user/query_builder`.
3. The executable must read CSV data from `stdin` and print the resulting Cypher queries to `stdout`.
4. The CSV input format is: `TxID,FromAccount,ToAccount,Amount` (where accounts are strings and amount is an integer).
5. For each row, output exactly one Cypher query.
6. **Deadlock Prevention Rule:** In the `MATCH` clause of the Cypher template, the accounts MUST be listed in ascending lexicographical order of their Account IDs. The lexicographically smaller Account ID must always be matched as `n1`, and the larger as `n2`. The `SET` clause must correctly map the deduction to the `FromAccount` and the addition to the `ToAccount`, referencing `n1` or `n2` appropriately.
7. If `FromAccount` and `ToAccount` are identical, do not output any query (skip the row).

For example, if the CSV contains:
`TX001,ZETA,ALPHA,100`

And the template (hypothetical, read the image for the real one) is:
`MATCH (n1:Account {id: '<node1>'}), (n2:Account {id: '<node2>'}) SET ...`

Because `ALPHA` < `ZETA`, `n1` must be `ALPHA` (which is the ToAccount) and `n2` must be `ZETA` (which is the FromAccount). The SET clause must deduct from `n2` and add to `n1`.

Do not use any external C libraries beyond standard libc. Ensure your program handles up to 1024 characters per line. The automated verifier will pipe hundreds of random CSV lines into your executable and test for strict bit-exact equivalence with our reference implementation.