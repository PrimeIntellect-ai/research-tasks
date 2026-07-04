You are a storage administrator tasked with reclaiming disk space on a legacy Linux server. You have found a large backup archive at `/app/legacy_backup.tar.gz` that contains an uncompressed audio memo (`admin_memo.wav`) and a multi-line audit log (`storage_audit.log`).

Your objective is to extract the important segment of the audio memo and discard the rest, saving disk space.

Please perform the following steps:
1. Verify the integrity of `/app/legacy_backup.tar.gz` and extract its contents.
2. The `storage_audit.log` file is encoded in UTF-16LE. It contains multi-line event records.
3. Write a Rust program (`/home/user/parser.rs`) that reads the extracted log file, handles the character encoding conversion to UTF-8, and parses the multi-line records to find the single event with `Type: AudioMemo`. 
4. Extract the `KeepStart` and `KeepEnd` time values (in seconds) from that specific multi-line record.
5. Use a tool of your choice (e.g., `ffmpeg` or `sox`) to trim `admin_memo.wav` so it only contains the audio between `KeepStart` and `KeepEnd`.
6. Save the resulting trimmed audio file to `/home/user/optimized_memo.wav`.

Ensure your Rust code compiles and runs successfully, and that the final audio file is correctly trimmed and formatted as a WAV file.