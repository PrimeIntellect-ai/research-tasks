We are migrating away from a legacy data processing system. Our analysts currently use a compiled binary tool that processes transaction CSV files to calculate an "anomalous score" for each transaction. However, the original source code was lost, and we suspect the binary contains a logical flaw (likely an implicit cross-join or incorrect analytical window aggregation) that makes its output mathematically peculiar.

Your task is to reverse-engineer the exact behavior of this binary and implement a Python replacement that produces bit-exact identical output.

The legacy binary is located at `/app/legacy_reporter`.
It is a stripped binary. You can interact with it by passing a CSV file path as the first argument:
`/app/legacy_reporter /path/to/data.csv`

The input CSV files always have the following headers:
`txn_id,user_id,timestamp,amount`
- `txn_id`: Integer
- `user_id`: Integer
- `timestamp`: Integer
- `amount`: Float

The binary outputs a JSON array to standard output. 

Your objective:
1. Probe the `/app/legacy_reporter` binary using black-box testing with crafted CSV files to deduce its exact aggregation logic and output schema.
2. Write a Python script at `/home/user/processor.py` that takes the path to a CSV file as its first argument and prints the identical JSON output to standard output.
3. Your Python implementation must map the CSV records, perform the analytical aggregation (replicating any "bugs" or quirks in the binary's logic), and validate/format the output schema exactly as the binary does.

Your script will be tested against the binary using a fuzzer with dozens of randomly generated CSV files to ensure bit-exact equivalence.