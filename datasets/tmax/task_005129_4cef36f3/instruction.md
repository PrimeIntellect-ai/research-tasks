You are acting as a storage administrator for a system that archives log data using a custom streaming format called `.zstrm`. You need to safely extract thousands of these streams concurrently, but the current extraction tools have significant issues.

Your task is to fix a vendored library, write a robust extraction script, and prepare the system for concurrent processing.

**Part 1: Fix the Vendored Package**
We have a Python package for parsing `.zstrm` files located at `/app/zstream-1.2.0`. It contains a severe "zip slip" vulnerability: it blindly trusts the file paths embedded in the archives, which could overwrite system files outside the target directory. 
Examine the package, specifically `/app/zstream-1.2.0/zstream/parser.py`. Fix the `get_safe_filename()` method so that it returns *only the base filename*, discarding any and all directory components (e.g., `../../etc/passwd` should become just `passwd`).

**Part 2: Write the Extraction Tool**
Create an executable Python script at `/home/user/safe_extract.py`. 
This script must:
1. Import the fixed `zstream` library (you may need to set your `PYTHONPATH`).
2. Read a `.zstrm` binary stream from standard input (`sys.stdin.buffer`). 
3. Use `zstream.StreamReader(sys.stdin.buffer)` to iterate over the archive. Each `record` yielded has `record.get_safe_filename()` and `record.compressed_data`.
4. Decompress the `compressed_data` using the standard `zlib` library.
5. Apply a bulk rename policy: Prefix every safely extracted base filename with `admin_` (e.g., if the safe filename is `system.log`, the new name is `admin_system.log`).
6. Append the uncompressed data to the corresponding file inside the `/home/user/extracted/` directory.

**Part 3: Concurrent Access Safety**
Because the system will pipe multiple streams to instances of your script concurrently (often containing fragments of the same file), your script **must** use file locking to prevent interleaved writes. 
Before appending to any file in `/home/user/extracted/`, you must open the file, acquire an exclusive lock using `fcntl.flock(fd, fcntl.LOCK_EX)`, write the uncompressed data, and release the lock. 

Ensure your script is executable. The automated verification will test your script by running numerous concurrent instances with heavily fuzzed archive streams containing malicious paths and overlapping files.