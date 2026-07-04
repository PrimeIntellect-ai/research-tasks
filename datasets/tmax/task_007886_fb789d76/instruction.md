You are acting as a backup administrator managing a continuous archiving system. We have a system that writes Write-Ahead Log (WAL) files to `/home/user/wal_data/`. Because the writer process runs continuously, some files in this directory are actively being written to (incomplete), while others might be corrupted.

Your task is to write a C++ program that acts as a safe archiver. The program must parse the binary headers of all `.wal` files in `/home/user/wal_data/`, determine which files are fully written and intact, and generate a verified backup manifest.

**WAL File Binary Format (Little-Endian):**
- **Bytes 0-3:** Magic signature. Must exactly match the ASCII string `WAL!` (0x57, 0x41, 0x4C, 0x21).
- **Bytes 4-7:** Sequence Number (32-bit unsigned integer).
- **Bytes 8-15:** Payload Size (64-bit unsigned integer).
- **Bytes 16+:** The actual data payload.

**Validation Rules:**
A WAL file is considered "complete and valid" ONLY if:
1. It has the correct `WAL!` magic signature.
2. The actual size of the file on disk exactly equals `16 + Payload Size`. 
   - If the file is smaller, it means the writer is still appending data (racing write) and it must be skipped.
   - If the file is larger, it means it is corrupted and must be skipped.

**Your Objective:**
Write and compile a C++ program that scans `/home/user/wal_data/`. For every complete and valid `.wal` file, it should record the file in a manifest. 

The program must output a manifest file to `/home/user/backup_manifest.txt`.
The manifest must contain one line per valid file, **sorted in ascending order by Sequence Number**.
Each line must be formatted exactly as follows:
`[8-digit Sequence Number, zero-padded] [Filename] [Payload Size]`

Example of `/home/user/backup_manifest.txt`:
```
00000001 01.wal 100
00000002 02.wal 250
00000005 05.wal 0
```

Compile and run your C++ program to produce the manifest.