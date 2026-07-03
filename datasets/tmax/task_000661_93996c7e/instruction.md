You are managing a legacy cluster. Periodically, the system dumps configuration state into compressed backup files. You need to extract database credentials from these backups to audit them.

In the directory `/home/user/legacy_configs/`, there are three gzipped configuration files:
- `node_A.cfg.gz`
- `node_B.cfg.gz`
- `node_C.cfg.gz`

These files have a quirk: the underlying text in the compressed stream is encoded in `UTF-16LE`, not standard UTF-8. 

Your task is to use a shell pipeline (using standard tools like `zcat`, `iconv`, `awk`/`sed`) to process these files. You must:
1. Process the files in alphabetical order by filename.
2. Decompress the stream without extracting the files to disk.
3. Convert the character encoding from `UTF-16LE` to `UTF-8`.
4. Find the line that starts with `DB_PASSWORD=`.
5. Transform the line to the format `<node_name>: <password>` (where `<node_name>` is the filename without `.cfg.gz`).
6. Append the results to a single log file at `/home/user/parsed_secrets.txt`.

For example, if `node_X.cfg.gz` contained `DB_PASSWORD=my_pass`, the line in the final log should be `node_X: my_pass`.

Write and execute the necessary commands to generate `/home/user/parsed_secrets.txt`. Make sure the final file is exclusively in UTF-8.