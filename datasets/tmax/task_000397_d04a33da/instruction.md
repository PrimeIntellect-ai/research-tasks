You are an operations engineer triaging a crashed containerized C application that processes financial sensor data. The application uses a custom Write-Ahead Log (WAL) to store state, but the container crashed unexpectedly, leaving a corrupted WAL file. Furthermore, there have been reports of data precision loss in some records.

Your goal is to investigate the container logs, write a C program to recover the uncorrupted records from the WAL, and identify which record suffered from floating-point precision loss.

Here is the environment you are given:
- `/home/user/app.log`: The captured standard output and error logs from the crashed container.
- `/home/user/wal.dat`: The binary WAL file left behind.
- `/home/user/wal_struct.h`: The C header file defining the WAL binary structures.

The `wal_struct.h` defines the file format:
1. A 8-byte header (`struct WAL_Header`).
2. A sequence of 48-byte records (`struct WAL_Record`).

Your tasks are:
1. **Container Log Inspection:** Review `/home/user/app.log` to determine which record ID caused the segmentation fault.
2. **Database Recovery:** Write a C program at `/home/user/recover.c` that parses `/home/user/wal.dat`. It must read the header, and then iterate through the records. You must SKIP the corrupted record (the one whose ID caused the crash) and successfully read the rest.
3. **Precision Loss Tracking:** While parsing the valid records, compare the `original_val` (a `double`) and the `stored_val` (a `float`). Identify the record ID where the absolute difference between `original_val` and `stored_val` is strictly greater than `0.01`.
4. **Reporting:** Your C program (or a shell script you write) must generate a final report at `/home/user/recovery_report.txt` with exactly the following format:

```
Recovered IDs: [comma-separated list of valid record IDs in order, e.g., 1,2,5]
Precision Loss ID: [The ID of the record with precision loss]
```

Constraints:
- Do not include the corrupted record ID in the "Recovered IDs" list.
- All code must be written in C (compiled with `gcc`) or standard bash shell commands.