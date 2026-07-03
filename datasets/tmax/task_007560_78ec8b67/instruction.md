You are a storage administrator tasked with reclaiming disk space and archiving a large database dump on a legacy system where standard compression tools (like gzip or tar) are strictly forbidden by company policy for data transport.

You must complete the following phases to optimize storage, compress the data using a custom algorithm, and prepare it for transport.

**Phase 1: Deduplication via Hard Links**
The directory `/home/user/db_dumps` contains 50 database dump files (`dump_1.sql` to `dump_50.sql`). Due to system glitches, many of these files are exact duplicates of one another.
Your task is to find all duplicate files and replace them with hard links to a single copy of that file, thereby reclaiming inode space. After this operation, no two files in the directory should have different inodes if their contents are identical.

**Phase 2: Custom Compression & Splitting**
There is a massive log file at `/home/user/massive_log.bin`. You must compress it using a custom "Base64-RLE" algorithm and split it into smaller chunks.
The custom compression algorithm works as follows:
1. Read the entire binary file and encode it into a single, continuous Base64 string (no newlines).
2. Perform Run-Length Encoding (RLE) on the Base64 string.
3. The RLE format must be exactly: `<count><character>` for every sequence of identical characters. Even single characters must have a count. 
   *Example: the Base64 string `aGVVVVb=` would become `1a1G1V4V1b1=`.* Wait, aGVVVVb= should be `1a1G1V4V1b1=`? No, `1a1G1V4V1b1=` is incorrect. It should be `1a1G1V4V1b1=`. Let's correct the example: `aGVVVVb=` -> `1a 1G 1V 4V 1b 1=`. Wait, `V` is repeated 4 times. So `1a1G1V4V...` is wrong. `aGVVVVb=` -> `1a1G4V1b1=`.

Save the resulting text as a single string. Then, split this compressed text into chunks of exactly 10,000 bytes each (the final chunk can be smaller).
Save these chunks in a new directory: `/home/user/archive_chunks/`. Name the chunks `chunk_00`, `chunk_01`, `chunk_02`, etc.

**Phase 3: Symbolic Linking**
Create a symbolic link at `/home/user/latest_archive` that points to the `/home/user/archive_chunks/` directory.

**Phase 4: Decompression & Merging Script**
Write a script in any language of your choice (e.g., Python, Bash) at `/home/user/decompress.sh` or `/home/user/decompress.py`.
This script must:
1. Traverse the `/home/user/latest_archive` symlink.
2. Read and merge all the chunk files in alphabetical order.
3. Decompress the Base64-RLE string back into the original binary data.
4. Save the restored binary data to `/home/user/restored_log.bin`.

When we run your script, `/home/user/restored_log.bin` must perfectly match the original `/home/user/massive_log.bin`.