You are an operations engineer triaging an incident. A system service relies on a Python package to parse binary log files, but the service is currently down.

You have the source code for the package in `/home/user/app/`.
When trying to install the package using `pip install -e /home/user/app`, the build fails due to a configuration error.

Additionally, the main script `/home/user/app/parser.py` crashes with an unhandled exception when processing certain edge-case corrupted logs.

Your tasks are:
1. Diagnose and fix the build failure in `/home/user/app/setup.py` so the package can be installed successfully. Install the package.
2. Analyze `/home/user/app/parser.py`. It reads a sequence of records from a binary file. Each record starts with a 4-byte little-endian integer (the length of the payload), followed by the payload itself. The script crashes when the remaining file data is shorter than the declared length of the payload.
3. Fix the format parsing edge-case in `parser.py`: Wrap the payload unpacking step in a `try...except` block to catch the `struct.error`. When this error is caught (i.e., when a malformed/truncated record is encountered), append the exact string `MALFORMED_RECORD_AT_OFFSET_<offset>\n` to the file `/home/user/failures.txt` (where `<offset>` is the byte index where the current record's 4-byte length field started), and then immediately `break` out of the parsing loop to stop processing the corrupted file.
4. Run the fixed parser on the provided corrupted log file: `python /home/user/app/parser.py /home/user/data/input.bin`.

Verify your fix by ensuring that `/home/user/failures.txt` contains the correct failure logs and the script no longer crashes.