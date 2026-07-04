You are a support engineer tasked with analyzing diagnostic data from a customer whose system crashed. The customer provided a diagnostic package containing a custom log file, a proprietary parser codebase, and a telemetry database.

The package is located at `/home/user/case_1029`.

Your objectives are to fix the parser, extract the logs, recover the database, and provide a minimal reproducible example (MRE) of the crash.

**Step 1: Build the Parser**
The customer's parser is in `/home/user/case_1029/src`. There is a `Makefile`, but attempting to run `make` results in a linker error.
Identify the missing library dependency (hint: it uses CRC32 from a common compression library) and fix the `Makefile` to successfully build the `diag_tool` executable.

**Step 2: Fix the Parsing Edge Case**
If you run `./diag_tool ../data/customer_events.bin` using the unmodified source code, it will hang in an infinite loop. 
Review `src/parser.c`. There is a bug in how the program reads data blocks: if it encounters a truncated record (where the file ends before the expected `length` of bytes is reached), the `fread` return value is mishandled, causing an infinite loop.
Modify `src/parser.c` to gracefully break out of the loop if `fread` returns 0 (EOF) while trying to read the payload. Recompile the tool.

**Step 3: Extract the Logs**
Run your fixed `./diag_tool ../data/customer_events.bin` and save its standard output to exactly `/home/user/case_1029/parsed_logs.txt`.

**Step 4: Database Recovery**
The customer's telemetry database is located at `/home/user/case_1029/db/telemetry.db`. The application crashed mid-transaction, so critical diagnostic rows are trapped in the Write-Ahead Log (`telemetry.db-wal`).
Using `sqlite3` or any script of your choice, extract all rows from the `diagnostics` table and save the output to `/home/user/case_1029/db_dump.txt`.

**Step 5: Minimal Reproducible Example**
The original developers need an MRE to write tests. Write a script in any language (e.g., Python, Perl, Bash) at `/home/user/case_1029/make_mre.py` (or `.sh`, etc.) that, when run, generates a file named `/home/user/case_1029/mre.bin`.
This `mre.bin` file must be a minimal corrupted binary file that reliably triggers the infinite loop on the *original, unfixed* `parser.c`. It should consist of a single record with the correct magic header, a requested length, but fewer bytes of actual payload than the length specifies.

Complete all steps. Your success will be evaluated by checking the contents of `/home/user/case_1029/parsed_logs.txt`, `/home/user/case_1029/db_dump.txt`, and your MRE generator.