Wake up, you are on-call. It is 3:00 AM and a critical authentication service just went down.

You investigate and find that the main SQLite database located at `/home/user/data/prod.db` has been corrupted due to a storage failure. Attempting to read it yields a "file is not a database" or "database disk image is malformed" error. 

We urgently need to recover the VIP access codes stored inside this database. 

Your tasks:
1. Use SQLite forensic recovery techniques to extract the surviving data from the corrupted `/home/user/data/prod.db` and restore it into a new database file.
2. We have a standard extraction script at `/home/user/scripts/extract_secrets.py` that processes the recovered database and extracts the `secrets` table. Run it against your recovered database: `python3 /home/user/scripts/extract_secrets.py <path_to_recovered_db>`.
3. The extraction script seems to be crashing with an error. The original author left the company, but we know it has a boundary condition or off-by-one bug. Debug and fix the Python script.
4. Run the fixed script so that it successfully outputs the recovered secrets to `/home/user/recovery_output.txt`.

The final `/home/user/recovery_output.txt` should contain the extracted secrets, with one record per line in the format:
`ID:SECRET_CODE`

Do not modify the target output file path in the script, only fix the logical bug preventing it from completing.