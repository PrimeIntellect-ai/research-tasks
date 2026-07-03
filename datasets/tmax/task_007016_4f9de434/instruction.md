You are an artifact manager responsible for curating binary repositories. We frequently receive compressed archives from third-party developers, and we need to ensure these archives are safe before extracting them into our system. 

Specifically, we are concerned about "Zip Slip" or path traversal vulnerabilities, where a compressed archive contains files with paths designed to overwrite system files outside the target extraction directory (e.g., paths containing `../` that resolve above the extraction root, or absolute paths like `/etc/passwd`).

You have received a new submission located at `/home/user/artifacts/release_v2.tar.gz`.

Your task is to write a Python script at `/home/user/scan_artifacts.py` that does the following:
1. Opens and reads the compressed tar stream `/home/user/artifacts/release_v2.tar.gz` directly without extracting it to disk.
2. Iterates through all members of the archive.
3. Identifies any member whose path represents a directory traversal attempt (i.e., absolute paths, or relative paths that would resolve outside of a base extraction directory).
4. Writes the exact, original path strings of these malicious members to a log file located at `/home/user/malicious_paths.txt`, with one path per line.

If there are no malicious paths, the file `/home/user/malicious_paths.txt` should be created but remain empty.
Do not extract the archive. Process it efficiently using Python's standard libraries. Run your script to generate the required output file.