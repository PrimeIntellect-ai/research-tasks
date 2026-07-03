You are a storage administrator tasked with recovering critical disk space on a Linux server without losing important production data. The system has automatically generated a visual alert image located at `/app/disk_alert.png`.

Your objectives are as follows:

1. **Identify the Target**: Use OCR (e.g., `tesseract`) to read the alert image at `/app/disk_alert.png`. It contains the name of a specific storage volume (e.g., `VOL-XXX`) that is critically low on space.
2. **Locate and Extract**: Find the backup archive for this specific volume inside `/app/storage/backups.tar`. The `backups.tar` file contains multiple compressed `.tar.gz` files. Extract *only* the inner archive corresponding to the target volume identified in step 1.
3. **Analyze and Sort**: The extracted volume contains many poorly named binary files.
   - Some files are standard Linux ELF executables. Bulk-rename these files to sequentially numbered files (`elf_001.bin`, `elf_002.bin`, etc.) and move them to `/home/user/elf_backup/`.
   - Other files are custom Write-Ahead Logs (WAL). You must identify them by their 4-byte magic signature at the start of the file: `WAL\0` (ASCII 'W', 'A', 'L', followed by a null byte).
4. **C Implementation for WAL Compaction**: To recover space, you must write a highly efficient C program (e.g., `compact_wal.c`) to parse the identified WAL files and strip out useless debugging data.
   - **WAL Format**:
     - **Header**: 4 bytes Magic (`WAL\0`), followed by 4 bytes Version (uint32, little-endian).
     - **Records**: A continuous stream of records until EOF. Each record consists of:
       - 1 byte `Type` (`0x01` = Data, `0x02` = Index, `0x03` = Debug).
       - 4 bytes `Length` (uint32, little-endian, representing the size of the payload).
       - `Payload`: `Length` bytes of binary data.
   - **Compaction**: Your C program must read each WAL file, discard any record of Type `0x03` (Debug), and write the preserved Magic, Version, and non-debug records to a new output file.
5. **Final Integration**: Run your compiled C program on all the WAL files you identified. Save the newly compacted WAL files in `/home/user/wal_clean/` with sequentially numbered names (e.g., `clean_001.wal`, `clean_002.wal`, etc.).

Your final metric of success is the total file size of the directory `/home/user/wal_clean/`. Our verification script will check the size to ensure all Debug records were successfully purged without corrupting the Data and Index records.