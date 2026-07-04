You are tasked with building a robust configuration management tracking tool. 

**Part 1: Video Telemetry Extraction**
You have been provided a telemetry artifact at `/app/telemetry.mp4`. This video encodes a legacy baseline configuration state.
- The video consists of exactly 120 frames (at 10 fps).
- Each frame is either completely black or completely white.
- A black frame represents a binary `0` and a white frame represents a binary `1`.
- Every 8 frames represents one ASCII character (Most Significant Bit first).
- Decode this binary sequence to reveal the baseline configuration string (which will be in the format `KEY=VALUE`).

**Part 2: Configuration Manager Script**
Create an executable script at `/home/user/config_manager.py` (or `.sh`, `.pl`, etc.) that applies configuration updates safely.
The script must take exactly one argument: the path to a `workspace` directory (which it should create if it doesn't exist).
It will read a sequence of operations from STDIN (one per line) and apply them to the workspace.

The workspace must have the following structure:
- `<workspace>/tmp/` - for temporary files
- `<workspace>/objects/` - stores configuration payloads
- `<workspace>/keys/` - stores symlinks to objects
- `<workspace>/snapshots/` - stores hard links of objects

**Operations to support:**
1. `WRITE <key> <encoding> <hex_payload>`
   - Decode the `<hex_payload>` to bytes.
   - Decode the bytes using the specified `<encoding>` (guaranteed to be one of: `UTF-8`, `UTF-16LE`, `ISO-8859-1`).
   - Convert the resulting text to a pure UTF-8 byte string.
   - Calculate the SHA-256 hash of this UTF-8 byte string.
   - **Atomically write** the UTF-8 bytes to `<workspace>/objects/<sha256_hash>`. (You MUST write to a file in `<workspace>/tmp/` first, then atomically rename/move it into the `objects` directory).
   - **Atomically create or update a symlink** at `<workspace>/keys/<key>` to point to `../objects/<sha256_hash>`. (Create a temp symlink and rename it over the target).

2. `ALIAS <new_key> <existing_key>`
   - Atomically create/update a symlink at `<workspace>/keys/<new_key>` pointing to the exact same target (the object file) as `<existing_key>`. If `<existing_key>` does not exist, do nothing.

3. `SNAPSHOT <key>`
   - If `<workspace>/keys/<key>` exists, create a **hard link** of the resolved object file into `<workspace>/snapshots/<key>_<unix_timestamp>`. (If multiple snapshots occur in the same second, you may append a counter).

**Execution Flow & Output:**
1. Your script must ALWAYS start by implicitly applying the baseline configuration extracted from the video as if it received the command: `WRITE <baseline_key> UTF-8 <hex_of_baseline_value>`.
2. It then processes all operations from STDIN.
3. Finally, it must print the resolved state of all keys to STDOUT. For every symlink in `<workspace>/keys/`, read the UTF-8 content of the object it points to.
4. Print each key and its content in the format `KEY:CONTENT`, sorted alphabetically by `KEY`.

Ensure your script is executable (`chmod +x`).