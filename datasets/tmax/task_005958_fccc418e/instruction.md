I am a technical writer organizing our legacy API documentation. I have a large, exported change log file located at `/home/user/docs/raw_changelog.dat`. Because it was exported from an old Windows system, the file is encoded in `UTF-16LE`.

The log contains multi-line text records separated by the exact line `===RECORD===`.

I need you to process this file and do the following:
1. Parse the multi-line records and find all records that contain the exact uppercase word `DEPRECATED` anywhere in their text.
2. Extract those matching records, strip any leading or trailing whitespace/newlines from each individual record's text, and save them to a new file at `/home/user/docs/deprecated_records.txt`. 
3. The output file MUST be encoded in standard `UTF-8`.
4. In the output file, append `\n===RECORD===\n` immediately after each extracted record (including the final one). Do not add any extra blank lines between the record text and the separator.
5. Once the output file is created, generate a SHA-256 checksum of `/home/user/docs/deprecated_records.txt` and save it to a manifest file at `/home/user/docs/manifest.txt`. The manifest file should use the standard `sha256sum` format (e.g., `<hash>  /home/user/docs/deprecated_records.txt` or `<hash>  deprecated_records.txt`).

Please write and run the necessary commands or scripts to accomplish this.