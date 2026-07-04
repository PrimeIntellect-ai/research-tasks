You are assisting an artifact manager who is trying to recover a corrupted repository backup. 

During our last backup process, a script followed a symlink into an infinite loop, causing it to repeatedly append the same data chunks to the backup archive before it finally crashed. 

The backup file is located at `/home/user/artifacts/corrupted_backup.bin`.

We need you to write a C++ program (`/home/user/recover.cpp`) to parse this custom binary chunked format, strip out the duplicate chunks, and reassemble the original file.

**Binary Format Specification:**
The file is a sequence of chunks. Every chunk has the following structure:
1. **Magic Bytes**: 4 bytes, ASCII characters `CHNK` (0x43 0x48 0x4E 0x4B)
2. **Chunk ID**: 4 bytes, Unsigned 32-bit Integer (Little-Endian)
3. **Payload Length**: 4 bytes, Unsigned 32-bit Integer (Little-Endian)
4. **Payload**: Raw byte data of size equal to the Payload Length.

**Recovery Logic:**
1. Because of the infinite loop, chunks repeat. You must extract the chunks and keep only the *first* occurrence of each Chunk ID.
2. After collecting all unique chunks, reassemble their payloads in ascending order of their Chunk IDs (0, 1, 2, ... N-1).
3. The concatenated payloads will form a valid JSON document. Save this recovered JSON document to `/home/user/artifacts/restored.json`.

**Final Extraction:**
Once you have the `restored.json` file, use standard Linux shell utilities to parse the JSON and extract the `sha256_checksum` value for the artifact with the `id` of `"linux-kernel-6.5-rc1"`.
Save ONLY the checksum string (no quotes, no extra whitespace) to `/home/user/artifacts/flag.txt`.