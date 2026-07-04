You are an artifact manager tasked with curating a corrupted binary repository. A legacy system was writing binary artifacts to a text-based log stream using base64 encoding. Unfortunately, a naive log rotation script split these logs strictly by line count, meaning that many multi-line artifact records have been sliced across multiple log files. 

You need to write a Python script to reconstruct these binary artifacts, split them into standardized chunks, and generate a secure manifest.

The raw log files are located in `/home/user/artifacts_raw/`. They are named `repo.log.001`, `repo.log.002`, etc.

**Log Format:**
When read in sequential order, the concatenated logs contain records in the following format:
```
BEGIN_ARTIFACT <artifact_name>
DATA:
<base64_string_line_1>
<base64_string_line_2>
...
END_ARTIFACT
```
*Note: Because of the naive log rotation, a `BEGIN_ARTIFACT` block might start in one file and end in another.*

**Your Tasks:**
1. **Parse and Merge:** Write a Python script to parse the multi-line records across all the log files (processing them in alphabetical order). Merge the base64 payload for each artifact.
2. **Format Conversion:** Decode the base64 data back into the raw binary artifacts.
3. **Chunking:** Save the reconstructed binary files, but split each artifact into chunks of exactly 512 KB (524,288 bytes). The last chunk will likely be smaller.
   - Save the chunks in the directory `/home/user/artifacts_bin/`.
   - Name the chunks `<artifact_name>.part<N>` where `<N>` is a zero-padded 3-digit integer starting at `000` (e.g., `core_engine.bin.part000`, `core_engine.bin.part001`).
4. **Manifest Generation:** Generate a JSON manifest at `/home/user/manifest.json` containing the SHA-256 checksums of every generated chunk.

**Manifest Format Requirements:**
`/home/user/manifest.json` must exactly follow this structure:
```json
{
  "artifact_name_1": {
    "artifact_name_1.part000": "<sha256_hash>",
    "artifact_name_1.part001": "<sha256_hash>"
  },
  "artifact_name_2": {
    "artifact_name_2.part000": "<sha256_hash>"
  }
}
```
Ensure `/home/user/artifacts_bin/` is created and the final manifest is placed at `/home/user/manifest.json`.