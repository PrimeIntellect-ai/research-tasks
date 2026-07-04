You are a storage administrator managing a legacy high-frequency trading database system. The system's disk space is rapidly filling up due to uncompressed Write-Ahead Log (WAL) dumps. You need to calculate exactly how much space can be safely reclaimed.

We have an undocumented, custom WAL format. However, the previous administrator left a voice memo detailing the binary structure of these logs before they left. The audio file is located at `/app/voicemail.wav`. You will need to transcribe or listen to this audio file to understand the binary WAL format specification.

We also have a pre-compiled, stripped legacy binary at `/app/oracle_parser` that correctly parses these files and outputs the reclaimable space. However, this binary is deprecated, incredibly slow on large files, and cannot be used in our new pipeline. 

Your task is to write a highly efficient Python script at `/home/user/parse_wal.py` that replicates the behavior of the legacy binary. 

Requirements:
1. Extract the WAL format specification from `/app/voicemail.wav`.
2. Write a Python script at `/home/user/parse_wal.py`. The script must take exactly one command-line argument: the path to a WAL file.
3. The script must parse the binary file according to the specifications in the audio, compute the required metrics, and print the exact same string output as `/app/oracle_parser`.
4. Your implementation must be bit-exact equivalent in its standard output to `/app/oracle_parser` for ANY valid WAL file generated according to the specification. 
5. Use memory-mapped I/O (`mmap`) or efficient binary streaming in your Python script to ensure it can handle large files without exhausting RAM.

To test your script during development, you can generate your own dummy WAL files based on the specification and compare your script's output against `/app/oracle_parser`.

You do not need to install the script globally; simply ensure `/home/user/parse_wal.py` exists and is executable via `python3 /home/user/parse_wal.py <file>`.