You are a storage administrator managing a legacy backup system. You need to recover a critical file from an old backup archive.

The backup is located at `/home/user/backup.tar.gz`.
Inside this archive, you will find a multi-part split tarball (files like `split.tar.aa`, `split.tar.ab`, etc.). 
When these parts are correctly combined and extracted, they will yield two files:
1. `base.rle`: The base backup, which is compressed using a custom binary Run-Length Encoding (RLE) format.
2. `update.patch`: An incremental backup, provided as a standard unified diff.

**Custom RLE Format Details:**
The `.rle` file is a binary file consisting of continuous 2-byte pairs:
- The first byte is an unsigned 8-bit integer representing the repetition count (from 1 to 255).
- The second byte is the literal data byte to be repeated.
For example, the byte `\x04` followed by the byte `A` means the letter 'A' should be repeated 4 times ("AAAA").

**Your Task:**
1. Extract the nested, multi-part archives from `/home/user/backup.tar.gz`.
2. Write a Python script to decompress `base.rle` into a plain text file named `base.txt`.
3. Apply `update.patch` to `base.txt` to incorporate the incremental backup changes.
4. Save the completely restored, patched file exactly to `/home/user/final_restored.txt`.

Ensure `/home/user/final_restored.txt` contains the final, correct data.