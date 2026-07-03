You are assisting a compliance officer auditing a financial transaction network. We need a high-performance C++ tool to process transaction records and identify suspicious money flow pathways based on strict compliance rules.

The compliance parameters (minimum transaction amount to consider, and the maximum allowed hops for a suspicious path) are documented in an image file located at `/app/compliance_rules.png`. You will need to extract these hidden parameters from the image (e.g., using OCR tools like `tesseract` which are available).

Your task:
1. Read the parameters from `/app/compliance_rules.png`.
2. Write a C++ program at `/home/user/audit.cpp` and compile it to `/home/user/audit`.
3. The program must read from standard input (stdin).
4. The input format is:
   - Line 1: `T`, the number of transactions.
   - Next `T` lines: `source destination amount` (integers, where `source` and `destination` are account IDs, and `amount` is the transaction value).
   - Next line: `Q`, the number of queries.
   - Next `Q` lines: `source destination` (integers representing a query to find a path).

For each query `source destination`, your program must compute the shortest path (minimum number of hops) from `source` to `destination` in the transaction graph, subject to the following rules:
- ONLY include transactions where `amount` is greater than or equal to the `MIN_AMOUNT` extracted from the image.
- The path length (number of hops) must NOT exceed the `MAX_HOPS` extracted from the image.
- Directed edges must be respected (money flows from source to destination).
- If multiple transactions exist between the same source and destination, a single valid transaction meeting the amount threshold is sufficient to establish an edge.

Output format:
- For each query, print a single line with the integer shortest path distance.
- If no path exists that satisfies the minimum amount and maximum hops constraints, print `-1`.

Compile your C++ program with `g++ -O3 -o /home/user/audit /home/user/audit.cpp`. We will test your binary against an automated fuzzer that will stream thousands of randomized test cases to ensure exact equivalence with our compliance oracle.