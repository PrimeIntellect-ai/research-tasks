You are helping a technical writer process documentation archives received from external contributors. The writer is cautious because some archives might be improperly formatted or contain accidental security risks like "Zip Slip" payloads (files attempting to extract outside the intended directory using path traversal like `../`).

You have a nested archive located at `/home/user/docs_receipt.tar.gz`.

Please perform the following steps:
1. Extract `/home/user/docs_receipt.tar.gz` to find a nested archive named `bundle.zip`.
2. Inspect `bundle.zip` without extracting it fully. Identify the exact internal path of the file that contains a path traversal vulnerability (a file path starting with `../`). Write this exact malicious path to `/home/user/malicious_path.txt`.
3. Safely extract *only* the file named `changelog.log` from `bundle.zip` to `/home/user/`.
4. `changelog.log` contains multi-line commit records separated by lines containing exactly `---`. Parse this file to find the single multi-line record that contains the phrase "Updated security protocols".
5. Save this exact multi-line record (without the `---` separators, but keeping all of its lines) to `/home/user/target_record.txt`.
6. The technical writer uses a custom "compression" format for storing sensitive records. Take the exact contents of `/home/user/target_record.txt`, Base64-encode it (as a single continuous string, standard base64), and then gzip the resulting base64 string. Save the final gzipped file to `/home/user/record_custom.gz`.

All files should be created inside `/home/user/`.