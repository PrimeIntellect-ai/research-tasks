You are an AI assistant helping a technical writer manage a chaotic, continuously building documentation pipeline. 

Multiple documentation generators are writing files concurrently, and you need to process these files on the fly, verify legacy archives, split the data into manageable chunks, generate a checksum manifest, and feed everything into a local search indexing service.

There is a service manager script at `/app/start_services.sh` that you must run first. It will launch three local services in the background:
1. **Active Doc Writer:** Continuously writes new documentation lines to `/home/user/raw_docs/active_draft.md`. It simulates a long-running build process.
2. **Legacy Archiver:** Periodically drops legacy documentation archives (`.tar.gz`) into `/home/user/legacy_docs/`. Some of these archives simulate network corruption and will be invalid.
3. **Indexer Sink:** A mock indexing service listening for raw text data on TCP port `9000`, and exposing a metrics HTTP endpoint on port `9001`.

Your task is to write a Python script (and any necessary shell commands) to perform the following workflow:

**Phase 1: Process Active Documents**
- The file `/home/user/raw_docs/active_draft.md` is continuously growing. Read this file as it grows (similar to `tail -f`).
- Safely split the incoming text into chunks of exactly 500 lines. 
- Save these chunks in `/home/user/processed_docs/` as `chunk_0001.md`, `chunk_0002.md`, etc.

**Phase 2: Process Legacy Archives**
- Watch the `/home/user/legacy_docs/` directory for `.tar.gz` files.
- Verify the structural integrity of each archive (e.g., using `tar` or python's `tarfile`). Ignore any corrupted archives.
- Extract valid archives, merge their `.md` contents, and chunk them using the same 500-line rule, continuing the naming sequence (e.g., `chunk_0003.md`).

**Phase 3: Manifest Generation & Streaming**
- For every complete chunk generated, compute its SHA256 checksum.
- Append the filename and checksum to `/home/user/processed_docs/manifest.txt` in the format: `[SHA256]  [filename]`.
- Pipe or stream the contents of the completed chunks into the Indexer Sink on TCP port `9000`. You can send the data by opening a socket to `localhost:9000` and sending the raw lines.

**Constraints & Requirements:**
- The `start_services.sh` script will run for exactly 3 minutes before stopping the generators. Your script should process the data concurrently.
- You must send as many valid lines as possible to port 9000.
- Do not lose lines or send partial lines from `active_draft.md` during the rotation/chunking process.
- Create `/home/user/raw_docs/`, `/home/user/legacy_docs/`, and `/home/user/processed_docs/` before starting the services.

The system will evaluate your success based on a completeness metric calculated by the Indexer Sink. Once you have processed all available data, inform the user.