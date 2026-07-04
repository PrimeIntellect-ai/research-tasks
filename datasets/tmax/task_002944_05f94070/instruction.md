A critical CI build is failing because our proprietary data ingestion tool, `/app/legacy_parser`, is crashing with a segmentation fault on certain new data feeds. The original source code for this parser is lost, and the binary is stripped. 

We had a junior developer working on a C++ sanitizer to filter out these malicious/malformed inputs, but they accidentally deleted their workspace. We managed to create a filesystem image of their working directory at `/app/recovered_workspace.img`.

Your task is to:
1. Extract the deleted `format_spec.txt` and the skeleton `detector.cpp` from the ext4 disk image `/app/recovered_workspace.img`.
2. Analyze the `/app/legacy_parser` binary (you can use GDB, `objdump`, etc.) to determine the exact conditions under which the buffer overflow occurs. 
3. Implement the missing logic in `detector.cpp` to parse the files according to `format_spec.txt` and identify the crash-inducing condition.
4. Compile your solution to `/home/user/detector`.

The detector must take a single file path as a command-line argument:
`./detector <path_to_data_file>`

It should exit with code `0` if the file is safe to process (clean), and exit with code `1` if the file will trigger the crash in the legacy parser (evil).

You must ensure your detector is highly accurate. It will be tested against a hidden suite of clean and evil files.