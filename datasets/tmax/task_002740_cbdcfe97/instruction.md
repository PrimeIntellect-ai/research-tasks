You are an incident responder and log analyst. We rely on a proprietary log analysis tool located at `/app/log_analyzer` to aggregate metric data from our complex multi-language systems. Unfortunately, we have lost the source code for this tool. It is a stripped binary, and we need to replace it with a maintainable script.

Your task is to write a replacement script at `/home/user/solution` (ensure it has execute permissions and a proper shebang, like `#!/usr/bin/env python3` or `#!/usr/bin/env ruby`). 

Your script must read data from standard input (`stdin`) and write the aggregated results to standard output (`stdout`), behaving exactly like the reference binary `/app/log_analyzer` for any given input.

Here is what we know about the log format and processing rules:
1. **Format**: The input is a Tab-Separated Values (TSV) stream with exactly 3 columns: `SessionID`, `Metadata`, and `Metrics`.
2. **Embedded Newlines**: The `Metadata` column often contains multi-line text. Multi-line text is always enclosed within `<<` at the start and `>>` at the end. Newlines inside `<<` and `>>` do not denote a new row.
3. **Filtering**: A row is strictly ignored if the `SessionID` does not consist of exactly 8 alphanumeric characters (regex: `^[A-Za-z0-9]{8}$`).
4. **Wide-to-Long Reshaping**: The `Metrics` column contains comma-separated key-value pairs (e.g., `speed:10,温度:25,Café:5`). Keys are multi-language Unicode strings, and values are integers.
5. **Normalization**: Before aggregating, metric keys must be Unicode-normalized using NFKC, converted to lowercase, and have all non-alphanumeric characters (including punctuation and symbols) stripped out using regular expressions. 
6. **Aggregation**: Sum the integer values for each normalized metric key across all valid rows.
7. **Output**: The tool outputs a strictly formatted JSON object (minified, no extra spaces) mapping the normalized keys to their total sums, with keys sorted alphabetically.

You can run `/app/log_analyzer` with various test inputs in your terminal to reverse-engineer any edge cases (e.g., handling of malformed rows, missing columns, or specific Unicode character behaviors) and ensure your script is bit-exact equivalent.

Once you are confident your script matches the binary's behavior, conclude your work. An automated fuzzer will test your `/home/user/solution` against `/app/log_analyzer` with thousands of randomized inputs to verify strict equivalence.