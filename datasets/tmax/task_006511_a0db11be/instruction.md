You are an IT support technician. A ticket has been escalated to you regarding the nightly log ingestion pipeline.

The ingestion script located at `/home/user/app/ingest.py` processes a batch of binary log files from the `/home/user/logs/` directory and inserts the parsed records into an SQLite database (`/home/user/app/logs.db`). 

However, the script is currently failing midway through the batch. It terminates with a generic `Fatal Error: Parsing failed` message, without indicating which file or record caused the crash. 

The developer provided the following specification for the custom binary log format:
- **Header:** 
  - Magic Bytes: `LOGS` (4 bytes)
  - Record Count: Unsigned Short, Big-Endian (2 bytes)
- **Records (repeated `Record Count` times):**
  - Timestamp: Unsigned Int, Big-Endian (4 bytes)
  - Status Code: Unsigned Byte (1 byte)
  - Message Length: Unsigned Byte (1 byte)
  - Message Body: UTF-8 String (`Message Length` bytes)
  
**Edge Case Specification:** 
If a record was marked as deleted by the upstream system, the `Message Length` byte is set to `0xFF` (255). Deleted records contain **no Message Body** (0 bytes to read for the message) and **must be completely skipped** (they should not be inserted into the database).

Your tasks:
1. Diagnose the issue to find out why the script is crashing.
2. Repair the format parsing logic in `/home/user/app/ingest.py` to handle the edge case according to the specification.
3. Run the repaired script so that it successfully processes all binary files in `/home/user/logs/` and populates `/home/user/app/logs.db`.
4. Query the database to find the total count of successfully ingested records that have a `status` of `1`.
5. Write this single integer count to `/home/user/app/status_1_count.txt`.

Do not modify the database schema or the target directory structures.