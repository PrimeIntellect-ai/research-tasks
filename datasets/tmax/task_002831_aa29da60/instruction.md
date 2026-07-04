You are a storage administrator managing automated file intake. Clients upload tar archives to an incoming directory, and an automated system extracts them. Recently, a security audit revealed that the extraction tool is vulnerable to a "Zip Slip" directory traversal attack—malicious archives can overwrite system files outside the target directory. 

You must secure the system by patching the extraction utility and creating a robust incoming-watcher.

1. **Fix the Vendored Package**: 
   The extraction tool `minitar` (version 0.1) is located at `/app/minitar-0.1`. It is written in C. The source code currently lacks checks for path traversal. Modify the C code so that it safely sanitises archive extraction:
   - If an archive contains ANY entry with a path that attempts to escape the current working directory (e.g., contains `../` components, or starts with `/`), the program MUST reject the archive.
   - On rejection, the program must print exactly `REJECT: <archive_name>` to standard output, extract nothing, and exit with status code `1`.
   - On safe (clean) archives, the program must extract the contents, print exactly `ACCEPT: <archive_name>` to standard output, and exit with status code `0`.
   - Compile the fixed code using the existing `Makefile` and ensure the binary is at `/app/minitar-0.1/minitar`.

2. **Test Corpora**:
   You are provided with two corpora for testing:
   - `/app/corpora/evil/`: Contains malicious `.tar` archives (attempting traversal).
   - `/app/corpora/clean/`: Contains safe `.tar` archives.
   Ensure your compiled `minitar` correctly accepts 100% of the clean corpus and rejects 100% of the evil corpus.

3. **Automated File Watching and Manifest Generation**:
   Write a shell script at `/app/watch_and_extract.sh` that sets up the intake pipeline:
   - Monitor the directory `/app/incoming/` for new `.tar` files.
   - When a new archive is detected, extract it using your fixed `minitar` (e.g., `./minitar -x -f <file>`).
   - If the archive is successfully extracted (exit code 0), compute the SHA-256 checksum of every extracted file and append the results to `/app/extraction_manifest.txt` in the format `<sha256>  <filename>`.
   - Redirect any standard error output from `minitar` to `/app/extraction_errors.log`.
   - The script should run continuously (you can assume `inotify-tools` is installed).