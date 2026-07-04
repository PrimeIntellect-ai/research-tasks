You are an AI assistant acting as an artifact manager for a binary repository system. 

The build system deposits binary artifacts into `/home/user/artifacts/` and records their lifecycle (approval for production or revocation) in a custom Write-Ahead Log (WAL) located at `/home/user/repo_state.wal`.

Your objective is to write and execute a Python script that parses the binary WAL file, determines the final "active" state of all artifacts, extracts embedded configuration strings from the active artifacts, and compiles them into a single summary report.

**1. Parse the WAL File (`/home/user/repo_state.wal`)**
The WAL file is a custom binary file with the following format:
*   **Header**: The first 4 bytes are the magic string `ARTL` (ASCII).
*   **Records**: Following the header is a sequence of records. Each record consists of:
    *   **Opcode**: 1 byte. `0x01` means ADD (artifact is active). `0x00` means REMOVE (artifact is revoked/inactive).
    *   **ID Length**: 1 byte (unsigned 8-bit integer) representing the length of the Artifact ID.
    *   **Artifact ID**: A string of ASCII characters of length equal to "ID Length".

The log is append-only and sequential. An artifact might be added, then removed, then added again. You must determine the *final* state of each unique Artifact ID after processing the entire log. Only artifacts whose final state is ADD (active) should be processed.

**2. Extract Configurations from Active Artifacts**
For every active artifact, there is a corresponding binary file at `/home/user/artifacts/<Artifact_ID>.bin`.
These are compiled binary blobs, but they contain embedded configuration strings in plain ASCII. 
*   Read the binary file.
*   Extract all ASCII strings that exactly match the pattern: `CONF_[A-Z_]+=[0-9]+` (e.g., `CONF_MAX_RETRIES=5`). 

**3. Generate the Output Report**
Create a text file at `/home/user/active_configs.txt`.
Write the extracted configuration strings to this file.
*   Format each line as: `<Artifact_ID>: <CONFIG_STRING>`
*   Sort the lines alphabetically first by `<Artifact_ID>`, and then by `<CONFIG_STRING>`.

**Requirements:**
*   Implement your solution in Python. 
*   You may write your script in `/home/user/curate.py` and run it.
*   The final output must strictly follow the sorting and formatting requirements.