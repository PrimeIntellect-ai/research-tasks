You are acting as an automated configuration manager. We have a repository of system configuration backups in `/home/user/config_backups/`, and a multi-line change log located at `/home/user/change_history.log`. 

Your task is to write a Bash script named `/home/user/audit_configs.sh` that analyzes the logs, validates the binary headers of the configuration files, and outputs a final audit report.

Here are the specific requirements:

1. **Parse the Multi-line Log**:
   The file `/home/user/change_history.log` contains change records separated by `---`. Each record looks like this:
   ```
   Ticket: TKT-XXXX
   Author: <name>
   Files:
    - file1.bin
    - file2.bin
   Status: <status>
   ```
   You need to extract the `Ticket` ID and the list of `Files` associated with it. Note that the files listed are relative to the `/home/user/config_backups/` directory. Ignore tickets where `Status` is `Rejected`.

2. **Binary Header Extraction and Validation**:
   For every file listed under an *Approved* or *Pending* ticket, you must verify its integrity. A valid configuration backup file must start with the exact 4-byte magic signature: `CF FA ED FE` (in hexadecimal). You must read exactly the first 4 bytes of the file to check this.
   If the file does not exist, treat it as "Missing".
   If the file exists but lacks the correct magic bytes, treat it as "Corrupt".
   If the file exists and has the correct magic bytes, treat it as "Valid".

3. **Output Generation**:
   Your script must generate a CSV file at `/home/user/verified_changes.csv` with the following header exactly:
   `Ticket,Filename,Status`
   
   Append a row for every file parsed from the valid tickets in the log.
   The `Status` column must be one of: `Valid`, `Corrupt`, or `Missing`.
   Sort the final CSV by `Ticket` ascending, then by `Filename` ascending.

4. **Execution**:
   Once you have written `/home/user/audit_configs.sh`, make it executable and run it to produce the `/home/user/verified_changes.csv` file.

Ensure your Bash script makes efficient use of standard stream redirection, handles multi-line parsing correctly, and properly extracts the binary header without loading entire binary files into memory.