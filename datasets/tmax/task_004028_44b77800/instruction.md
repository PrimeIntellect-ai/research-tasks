You are an automation specialist for a financial tech firm migrating a legacy workflow. You need to build an automated data processing pipeline and a lightweight query service using only standard Linux CLI tools and Bash.

Your task is to process incoming data, generate cryptographic signatures using a legacy binary, and serve the results over a raw TCP connection.

Here are the requirements:

1. **Input Data Processing:**
   You have two data files in `/home/user/incoming/`:
   - `clients.json`: An array of JSON objects with keys `client_id` (string) and `status` (string, either "active" or "suspended").
   - `transactions.csv`: A CSV file with headers `tx_id,client_id,amount`.

2. **Database Merging:**
   - Bulk import both files into a new SQLite database located at `/home/user/finance.db`. You may use tools like `jq` to transform the JSON for easy SQLite ingestion.
   - Perform a join to filter out any transactions belonging to "suspended" clients. Only "active" client transactions are valid.

3. **Legacy Signature Generation:**
   - There is a stripped, proprietary binary located at `/app/tx_signer`.
   - This binary acts as an oracle for generating transaction signatures. It takes exactly two positional arguments: `tx_id` and `amount`.
   - Example usage: `/app/tx_signer TX123 50.00`
   - It outputs a single hex string to `stdout` (the signature).
   - You must generate a signature for every *valid* transaction identified in Step 2.

4. **Serve the Data (TCP Server):**
   - Create and run a persistent Bash-based TCP server listening on `127.0.0.1` port `9000`. You may use tools like `socat` or `nc` to handle the networking, routing connections to a bash handler script.
   - **Protocol:**
     - The client connects and sends a request in the format: `GET <client_id>\n`
     - The server must respond with a CSV-formatted list of all valid transactions for that `client_id`, followed by a final line containing exactly `END\n`.
     - The CSV response format for each line must be: `tx_id,amount,signature\n` (Do not include headers in the response).
     - If the client ID has no valid transactions or doesn't exist, simply output `END\n`.
     - The server must be able to handle multiple sequential requests.

Leave your server running in the background or foreground so that our automated test suite can connect to `127.0.0.1:9000`, issue protocol requests, and verify the processed data and signatures.