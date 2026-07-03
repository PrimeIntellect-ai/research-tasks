You are tasked with recovering and cleaning up configuration backups for our legacy configuration manager. A previous version of our backup script had a bug where it followed symlinks recursively, leading to infinite loops. As a result, the backup archives contain multiple repeated entries of the same files.

Your objective is to process these archives, extract the unique configurations, update outdated server references, and generate a final consolidated configuration file.

All operations should take place within `/home/user/cfg_manager/`.

**Step 1: Bulk Renaming**
In `/home/user/cfg_manager/raw/`, there are several backup files named with the pattern `backup_cfg_<number>.dat`. 
Rename all of these files to `archive_<number>.cpk` within the same directory.

**Step 2: Binary Format Extraction and Deduplication**
Write a C program at `/home/user/cfg_manager/extractor.c` to parse these `.cpk` archives.
The `.cpk` (ConfigPak) binary format is defined as follows:
- **Global Header**: 
  - 8 bytes Magic Number: exactly the ASCII string `CFGPAK01`
  - 4 bytes Unsigned Integer (Little Endian): `num_entries`, the total number of file entries in the archive.
- **Entries** (repeated `num_entries` times):
  - 64 bytes string: The original filename, null-terminated and null-padded.
  - 4 bytes Unsigned Integer (Little Endian): `file_size`, the size of the configuration data.
  - `file_size` bytes of raw text data (the configuration content).

*The Infinite Loop Bug:* Because of the symlink bug, an archive may contain the same filename multiple times. Your C program must read the archive and extract the files, but it **must only save the FIRST occurrence** of any filename per archive. Subsequent entries with a filename that has already been extracted from that specific archive should be skipped/ignored.

Extract the valid (deduplicated) files into the directory `/home/user/cfg_manager/extracted/`. Save them using their original filenames as specified in the entry header.

Compile your C program using `gcc` and run it on all the `.cpk` files in the `raw` directory.

**Step 3: Text Transformation**
Our database server has moved. In the `/home/user/cfg_manager/extracted/` directory, find all extracted configuration files and use standard bash tools (like `sed`) to replace every occurrence of the string `db_host=legacy-db.local` with `db_host=db-cluster.aws.internal`.

**Step 4: Merging**
Finally, combine all the updated configuration files from `/home/user/cfg_manager/extracted/` into a single file at `/home/user/cfg_manager/final_config.txt`. 
Before the contents of each file, you must append a header line in the exact format:
`=== <filename> ===`
Ensure the files are appended in alphabetical order based on their filename.

**Constraints:**
- Ensure you create the `/home/user/cfg_manager/extracted/` directory before running your C program.
- Do not use any external C libraries, only standard libc.