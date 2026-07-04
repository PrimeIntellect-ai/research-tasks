You are assisting a technical writer in preparing a documentation package for open-source release. The documentation consists of various debug logs that contain interleaved snippets of GCode, ELF binary headers, and SQLite WAL (Write-Ahead Log) excerpts.

Our company policy requires that no proprietary information is leaked in these logs. You need to create a Python script at `/home/user/sanitizer.py` that acts as a classifier/detector for these logs.

**Requirements for `/home/user/sanitizer.py`:**
1. **Invocation:** The script must take exactly one argument: the absolute path to a log file.
   `python3 /home/user/sanitizer.py <filepath>`
2. **Classification:** It must parse the multi-line log records and **reject** (exit with code 1) the file if it contains ANY of the following proprietary markers:
   - Proprietary GCode: Any `M` command in the range `M8000` to `M8999` inclusive.
   - Forbidden ELF sections: An ELF section dump that mentions our proprietary section name. You must discover this specific section name by analyzing the video artifact located at `/app/tutorial.mp4`. The name is clearly visible in a terminal window shown around the 2-second mark of the video. (Hint: you can use `ffmpeg` and `tesseract` to extract and read it).
   - Proprietary WAL entries: Any WAL excerpt containing the exact string `"PROPRIETARY_TX"`.
   If the file contains none of these, it must be considered **clean** and the script must exit with code 0.
3. **Audit Logging & Concurrency:** Regardless of the outcome, the script must append exactly one line to `/home/user/audit.log` in the following format:
   `[<ISO8601_TIMESTAMP>] <filepath> <REJECTED|CLEAN>`
   Our CI pipeline will test your script by running it against hundreds of files **concurrently**. To prevent multi-line log records from being interleaved or corrupted, you MUST implement strict file locking (`fcntl.flock`) when appending to `/home/user/audit.log`.

There are sample files provided for you to test against if you wish to create them, but the final evaluation will run your script against a hidden adversarial corpus consisting of an `evil/` directory (which must all be rejected) and a `clean/` directory (which must all be accepted). Ensure your parsing is robust.