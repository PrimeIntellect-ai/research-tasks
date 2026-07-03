You are acting as a storage administrator managing a Linux server that automatically receives and extracts log archives. Recently, there has been a security concern regarding "zip slip" style vulnerabilities, where malicious archives contain symbolic or hard links that point outside the intended extraction directory.

Your task is to write a Python script at `/home/user/validate_archive.py` that safely inspects an incoming tarball without extracting it, identifying any dangerous links.

The system is set up as follows:
- An archive is located at `/home/user/storage/incoming.tar`.
- A configuration file is located at `/home/user/storage/config.ini`.

The configuration file is in standard INI format and contains a `[Paths]` section with a `SafeDirectory` key. This key defines the absolute path where the archive *would* be extracted.

Your Python script `/home/user/validate_archive.py` must perform the following actions:
1. Parse `/home/user/storage/config.ini` to determine the `SafeDirectory`.
2. Open `/home/user/storage/incoming.tar` and acquire a shared file lock (`fcntl.LOCK_SH`) on the file descriptor to ensure the archive isn't modified by incoming transfers while you read it.
3. Stream the contents of the tarball (do not extract it and do not load the entire file into memory).
4. Inspect every member of the archive. Identify any symbolic links or hard links that, if extracted into `SafeDirectory`, would point to a location *outside* of `SafeDirectory` (e.g., due to absolute paths or excessive `../` sequences).
5. Write the exact archive member names of these dangerous links to a log file at `/home/user/storage/unsafe_members.txt`, with one member name per line, sorted alphabetically.

Constraints:
- Only use standard Python libraries.
- You must handle the locking explicitly in the script before iterating through the tar archive.
- Assume all paths are evaluated on a POSIX system. 

Run your script to produce the output file `/home/user/storage/unsafe_members.txt` so your work can be verified.