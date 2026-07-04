As a storage administrator, you are facing a critical disk space shortage on a legacy database server. The culprit is a massive accumulation of Write-Ahead Log (WAL) files that contain a large amount of obsolete, redundant diagnostic data. 

We need to reclaim space by writing a highly efficient log compactor in C++ that filters out these obsolete records.

First, you need to determine which records are obsolete. The previous administrator left a screenshot of the system policy in `/app/policy_screenshot.png`. Use an OCR tool (like `tesseract`, which is preinstalled) to read this image. It contains the specific `Transaction Type` (hex) and `Status Code` (hex) that define an obsolete record.

Next, write a C++ program at `/home/user/wal_compactor.cpp` and compile it to `/home/user/wal_compactor`. 

Your program must implement the following CLI signature:
`/home/user/wal_compactor <input_wal_path> <output_wal_path>`

The WAL binary format is as follows:
1.  **File Header:** 8 bytes containing the magic string `WALv1\0\0\0`.
2.  **Records:** A sequence of records tightly packed back-to-back.
    Each record consists of:
    *   `length` (uint32_t, little-endian): The total length of this record *including* this 4-byte length field.
    *   `tx_type` (uint8_t): The transaction type.
    *   `status` (uint8_t): The status code.
    *   `payload` (byte array): The remainder of the record (size is `length - 6`).

Your program must read the input WAL file, validate the magic header, and stream the records to the output WAL file. It must **silently drop** any record where `tx_type` AND `status` exactly match the obsolete values you extracted from the screenshot. All other records must be written to the output file exactly as they appear in the input. If the input file is missing the magic header or is truncated, the program should exit with code 1. Otherwise, exit with code 0 on success.

For performance, use efficient streaming I/O or memory-mapped files (e.g., `mmap`).

Once compiled, an automated fuzzing verifier will test your `/home/user/wal_compactor` binary against a highly optimized, secret reference implementation using thousands of randomly generated WAL files to ensure bit-exact output equivalence.