You are an artifact manager curating a large repository of binary artifacts. Your pipeline relies on a proprietary legacy analyzer tool located at `/app/artifact_reader` to extract metadata and register artifacts. 

Recently, the pipeline has been freezing and crashing. We suspect a malicious actor is submitting malformed artifacts that exploit a vulnerability in `/app/artifact_reader`. When fed these "evil" artifacts, the tool either crashes with a segfault or gets caught in a continuous memory-allocation loop (a race condition with the system's OOM killer).

Your task is to write a robust Bash gatekeeper script, `/home/user/classifier.sh`, that inspects an artifact and determines if it is safe to process. 

**Requirements:**
1. **Entry Point**: You must create `/home/user/classifier.sh`. It will be invoked with a single argument: the path to an artifact file (e.g., `/home/user/classifier.sh /path/to/artifact.bin`).
2. **Behavior**: 
   - Exit with code `0` (success) if the file is SAFE (clean).
   - Exit with a non-zero code (e.g., `1`) if the file is MALFORMED or MALICIOUS (evil).
3. **Artifact Structure**: 
   - The first bytes of the file contain a JSON header, which is padded with null bytes.
   - The header can be encoded in standard UTF-8 OR in UTF-16LE (which will begin with the standard `FF FE` Byte Order Mark).
   - After the JSON header, the rest of the file is raw binary data.
4. **Investigation**: We have provided two directories of sample files:
   - `/home/user/artifacts/clean/` : Contains known good files that `/app/artifact_reader` processes successfully.
   - `/home/user/artifacts/evil/` : Contains known bad files that crash or hang `/app/artifact_reader`.
   
You must reverse-engineer the difference between the clean and evil files. Use `xxd`, `dd`, `iconv`, `jq`, and the `/app/artifact_reader` binary itself to understand the vulnerability. You will need to use streaming I/O commands to safely extract the header, convert the character encoding if necessary, and parse the structured JSON to perform boundary/safety checks against the file's actual size.

**Constraints:**
- Your gatekeeper script must be written primarily in Bash, though you may use standard command-line utilities (like `jq`, `iconv`, `wc`, `dd`, Python one-liners, etc.) inside it.
- Ensure your script handles files efficiently without loading multi-gigabyte files entirely into memory.