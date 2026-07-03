You are tasked with building a robust configuration tracking daemon in C that monitors a directory for changes, converts text encodings, and safely appends records to a binary journal using file locking.

Please perform the following steps:

1. Create a watch directory `/home/user/configs` and a journal file `/home/user/config_journal.bin`.
2. Write a C program at `/home/user/tracker.c` that does the following:
    - Uses `inotify` to monitor `/home/user/configs` for `IN_CLOSE_WRITE` events.
    - When a file is written and closed, read its entire contents.
    - Assume the input file is encoded in `ISO-8859-1`. Use the `iconv` API to convert the file's content to `UTF-8`.
    - Acquire an exclusive write lock on `/home/user/config_journal.bin` using `fcntl` (to handle potential concurrent accesses).
    - Append a binary record to the journal file.
    - Release the lock.
3. The binary record appended to the journal MUST be exactly 292 bytes long and structured as follows:
    - `filename`: 32 bytes, null-padded string (just the base name of the file).
    - `content_length`: 4 bytes, `uint32_t` representing the length of the converted UTF-8 content in bytes.
    - `content`: 256 bytes, null-padded string containing the UTF-8 converted text.
    *Note: Truncate the content if it exceeds 256 bytes. Do not include struct padding; write the fields packed.*
4. Compile the program into an executable named `/home/user/tracker` (e.g., `gcc tracker.c -o tracker`).
5. Run the tracker in the background.
6. To test your tracker, simulate configuration updates by creating two files in `/home/user/configs`:
    - `/home/user/configs/app.conf`: Write the byte sequence `0x43 0x61 0x66 0xe9 0x0a` (which is "Café\n" in ISO-8859-1).
    - `/home/user/configs/user.conf`: Write the byte sequence `0x4e 0x69 0xf1 0x6f 0x0a` (which is "Niño\n" in ISO-8859-1).
    *(Hint: You can use `printf` with octal/hex escapes to create these files).*
7. Wait 2 seconds to ensure the events are processed.
8. Kill the background tracker process.
9. Generate a canonical hex dump of the binary journal to `/home/user/journal_dump.txt` using the command: `hexdump -C /home/user/config_journal.bin > /home/user/journal_dump.txt`

Ensure all paths are strictly followed and the binary structure is exactly 292 bytes per record.