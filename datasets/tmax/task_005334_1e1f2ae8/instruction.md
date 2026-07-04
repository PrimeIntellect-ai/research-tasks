You are an IT Support Technician handling an escalation ticket (Ticket #402) for the forensic investigations team. 

The team uses a custom C utility, `parser.c`, to recover deleted files from a proprietary filesystem dump format. However, the tool is currently hanging indefinitely when processing a recent dump file (`fs_dump.bin`). The original developer noted that the program "works fine on small dumps but loops infinitely on dumps with many records due to an integer overflow in the loop counter."

Additionally, the forensic team wants to validate the integrity of the dumps. They requested that you add an assertion to `parser.c` to ensure that no recovered file claims a data length of 10,000 bytes or more.

Your objectives:
1. Debug and modify `/home/user/ticket_402/parser.c` to fix the infinite loop preventing the extraction of records. (Use `gdb` if necessary to inspect the loop variables).
2. Add an assertion (`assert(...)`) immediately after the `data_len` is read from the file to ensure `data_len < 10000`. 
3. Recompile the fixed `parser.c` and run it against `/home/user/ticket_402/fs_dump.bin`. This will extract a previously deleted SQL file to the current directory.
4. The recovered SQL file contains a query intended to be run against `/home/user/ticket_402/company.db`. However, the forensic team noted: "The query in the deleted file returns all administrators. We need you to debug and modify the query so it ONLY returns administrators who have the `is_deleted` flag set to 1."
5. Execute the corrected SQL query against `company.db`.
6. Save the output of the database query to `/home/user/ticket_402/final_result.txt` (just the raw output rows).

All files are located in `/home/user/ticket_402/`. Ensure your final fixed C code is saved as `parser.c` and is successfully compiled and run before completing the task.