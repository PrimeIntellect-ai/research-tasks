You have inherited a legacy data processing system. The previous developer left behind a stripped compiled binary located at `/app/legacy_cleaner` that extracts human-readable text from corrupted data streams, but the original source code is lost.

Your task is to reverse-engineer the exact behavior of `/app/legacy_cleaner` and write a replacement executable script or program at `/home/user/cleaner`. 
You may write your replacement in any programming language you choose, as long as it is self-contained and executable (make sure it has the appropriate shebang and `chmod +x`).

The `/app/legacy_cleaner` utility reads arbitrary data streams from `stdin` and prints the recovered, cleaned data to `stdout`. 

Investigate how the binary handles different inputs (including invalid, corrupted, or completely random data), processes the stream, and gracefully recovers from unexpected characters. Once you understand the underlying logic, implement `/home/user/cleaner` to be perfectly equivalent. It must produce bit-for-bit identical output to the legacy binary for any given input.

Requirements:
- Your solution must be located at `/home/user/cleaner` and be fully executable.
- It must read from `stdin` and write to `stdout`.
- It must not invoke `/app/legacy_cleaner` as a subprocess; you must completely reimplement the logic.