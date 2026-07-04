You are a security researcher analyzing a suspicious binary `/home/user/data_exfiltrator` that appears to process exfiltrated data and write it to a local SQLite database `/home/user/stolen_data.db`. 

When you run `./data_exfiltrator payload.bin`, it crashes (Segmentation fault) halfway through processing the file. This crash has left the database in a potentially corrupted state with an orphaned WAL file (`/home/user/stolen_data.db-wal`).

You have managed to decompile the data parsing library and reconstruct its source code in `/home/user/parser.c`. The main binary dynamically links to `/home/user/libparser.so`.

Your objectives are:
1. **Fix the parsing bug**: Identify the format parsing edge-case or buffer overflow in `/home/user/parser.c` that causes the crash. The `out_buf` in the calling binary is strictly allocated to 256 bytes. Modify `parser.c` to safely truncate any data that exceeds this limit, ensuring a null-terminator is always correctly placed, and preventing the segmentation fault.
2. **Recompile the library**: Recompile `parser.c` into `libparser.so` so that `data_exfiltrator` uses your fixed version. (The binary is already configured to look for `libparser.so` in `/home/user`).
3. **Recover the database**: Ensure any previously written records in the SQLite WAL file are fully recovered into `stolen_data.db`.
4. **Process the payload**: Run `./data_exfiltrator payload.bin` successfully to completion so that all records are parsed and inserted into the database.
5. **Timeline Reconstruction**: Query the `exfiltration_logs` table in the database to find the earliest (minimum) `timestamp` value. Then, search `/home/user/service.log` to find the log entry with that exact Unix timestamp to identify which service was targeted.
6. **Report**: Create a file at `/home/user/report.txt` containing the targeted service name and the total number of records successfully written to the database, in exactly this format:
```
Targeted Service: <service_name>
Total Records: <number>
```