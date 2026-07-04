You are assisting a compliance officer in auditing financial transaction systems. We need a lightweight, fast utility to flag suspicious accounts based on graph centrality and volume metrics.

Your task is to write and compile a Rust program that processes a transaction graph and flags specific nodes based on hidden compliance rules.

1. There is an image file located at `/app/compliance_rule.png`. This image contains the strictness parameters for our current audit. You will need to extract the text from this image (e.g., using `tesseract`) to find two variables: `MIN_IN_DEGREE` and `MIN_SUM`.
2. Create a Rust project and compile a binary to exactly `/home/user/audit_tool`.
3. The binary must read standard input (STDIN) until EOF. The input will be a CSV format (without headers) representing directed graph edges of transactions:
   `sender,receiver,amount`
   (where `sender` and `receiver` are strings of letters, and `amount` is a positive integer).
4. The program must build an internal graph model and calculate two metrics for every node in the network:
   - In-Degree: The number of *distinct* senders that have sent money to the node.
   - Total Inbound Volume: The sum of all `amount` values received by the node.
5. If a node meets or exceeds BOTH the `MIN_IN_DEGREE` and `MIN_SUM` thresholds extracted from the image, it should be flagged.
6. The program must print the names of all flagged nodes to standard output (STDOUT), one per line, sorted alphabetically. If no nodes are flagged, output nothing.

Make sure your Rust code handles malformed lines gracefully by ignoring them (though the test inputs will be well-formed). Build your binary in release or debug mode, but ensure the final executable is located exactly at `/home/user/audit_tool`.