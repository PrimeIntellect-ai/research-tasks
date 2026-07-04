You are a backup administrator tasked with safely archiving data from an actively written Write-Ahead Log (WAL) used by a custom database. 

The database continuously appends binary records to the WAL located at `/home/user/db.wal`. Because the database process might be appending to the file while you read it, your archiving script must gracefully handle potentially incomplete records at the end of the file. You are advised to use memory-mapped I/O (mmap) or standard file operations, but you must only process fully written, complete records.

**File Format Specification for `/home/user/db.wal`:**
- **Header**: The first 4 bytes are the magic string `WAL!` (ASCII).
- **Records**: Following the header, records are packed consecutively. Each record consists of:
  1. `TXID`: 4 bytes, Unsigned Integer, Little-Endian.
  2. `LENGTH`: 4 bytes, Unsigned Integer, Little-Endian.
  3. `PAYLOAD`: Variable length ASCII string of exactly `LENGTH` bytes.

**Your Task:**
Write and execute a script (in Python, Ruby, Perl, or any available scripting language) that reads `/home/user/db.wal` and does the following:
1. Validates the `WAL!` header.
2. Iterates through the binary records. If you encounter an incomplete record at the end of the file (e.g., the remaining bytes are fewer than 8, or fewer than the parsed `LENGTH`), safely stop reading and ignore the partial record.
3. Filters the records, keeping ONLY those where the `TXID` is exactly divisible by `3`.
4. Applies a custom Run-Length Encoding (RLE) compression to the `PAYLOAD` of the filtered records. The payloads consist of repeated characters. Your custom compression must convert consecutive identical characters into `<count><character>`. For example, a payload of `AAAAAABBBCC` becomes `6A3B2C`.
5. Writes the compressed payloads, one per line, to `/home/user/archive.rle`. 

Ensure the output file `/home/user/archive.rle` is created with the exact compressed strings for all valid, matching records.