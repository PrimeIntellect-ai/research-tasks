You are an IT support technician acting on an escalated support ticket. A legacy internal tool called `csv_transformer` has started crashing with a Segmentation Fault when processing the latest customer data export.

Your task is to debug the tool, isolate the bad data, fix the code, and document your findings.

Here are the details of your environment and the ticket:
- **Source Code:** `/home/user/csv_transformer.c`
- **Data File:** `/home/user/data/customer_records.csv`
- **Compiled Binary:** `/home/user/csv_transformer` (Currently compiled with `gcc -g -o csv_transformer csv_transformer.c`)

**Ticket Instructions:**
1. **Debug & Isolate:** The program crashes somewhere inside the `customer_records.csv` file. Use standard debugging tools (like `gdb`) or delta debugging techniques to identify the exact line of data causing the crash.
2. **Create MRE:** Create a Minimal Reproducible Example input file at `/home/user/mre.csv`. This file must contain *only* the single line from `customer_records.csv` that triggers the crash (no headers, just the exact raw text of the offending line).
3. **Fix the Bug:** Modify `/home/user/csv_transformer.c` to prevent the crash. The program should simply skip any records where the parsed `id` is less than 0 or greater than 999, rather than crashing or causing memory corruption. Recompile the binary.
4. **Resolution Report:** Create a log file at `/home/user/ticket_resolution.txt` containing exactly two lines:
   - Line 1: The exact integer `id` value that caused the crash.
   - Line 2: The line number in the original `customer_records.csv` file where this record appeared (1-indexed).

Ensure that after your fix, running `./csv_transformer data/customer_records.csv` exits cleanly with a status code of 0.