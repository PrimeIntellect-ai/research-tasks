You are acting as a technical assistant for a compliance officer auditing a financial trading system. We have discovered that the primary trades database has a corrupted index that occasionally returns stale or ghost rows, compromising our audit results.

Your task is to write a C program that correctly queries the database and computes a compliance risk score for a given list of stock symbols, while avoiding the corrupted index.

Step 1: Instructions
We have recovered a voicemail from the database administrator explaining the exact compliance formula and how to avoid the database corruption. The audio file is located at `/app/audit_instructions.wav`. You will need to transcribe or listen to this audio to understand the exact mathematical aggregation required and how to bypass the corrupted index.

Step 2: Database
The SQLite database is located at `/app/trading.db`. It contains a table named `trades` with the schema:
`CREATE TABLE trades (id INTEGER PRIMARY KEY, symbol TEXT, price REAL, volume INTEGER, timestamp DATETIME);`
`CREATE INDEX idx_symbol ON trades(symbol);` -- THIS INDEX IS CORRUPTED

Step 3: Implementation
Write a C program at `/home/user/auditor.c` and compile it to `/home/user/auditor`. 
Your program must:
- Use the SQLite3 C API (`-lsqlite3`).
- Accept exactly one command-line argument: a comma-separated string of stock symbols (e.g., `"AAPL,GOOG,MSFT"`).
- Connect to `/app/trading.db`.
- Calculate the compliance risk score for each provided symbol based on the rules specified in the audio file.
- Print the final result to standard output strictly as a valid JSON array of objects, ordered alphabetically by symbol. For example:
  `[{"symbol":"AAPL","risk_score":150.25},{"symbol":"GOOG","risk_score":2800.10},{"symbol":"MSFT","risk_score":305.50}]`
- Do not print anything else to standard output. Format floating point numbers to exactly 2 decimal places in the JSON.

Ensure your code is robust. The automated verification system will test your compiled binary `/home/user/auditor` against a hidden reference oracle with hundreds of random symbol combinations to ensure bit-exact equivalence.