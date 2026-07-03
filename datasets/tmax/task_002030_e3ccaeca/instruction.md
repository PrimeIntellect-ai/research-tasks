You are an AI assistant helping a technical writer process and organize a large set of draft documentation. 

The writer has a directory of markdown files in `/home/user/docs_draft/`. They need an automated pipeline that transforms the text, extracts an index concurrently, and generates a manifest. You must implement this using Bash for the text transformation and Rust for the concurrent indexing and manifest generation.

Here are your instructions:

**Phase 1: Text Transformation (Bash & sed)**
1. Read the configuration file at `/home/user/doc_config.txt`. Each line contains a `sed` substitution command (e.g., `s/old/new/g`).
2. Apply all substitution commands from the config file to every `.md` file in `/home/user/docs_draft/` in-place. You must use `sed` (or `awk`) to do this.

**Phase 2: Concurrent Index Extraction (Rust & File Locking)**
1. Create a Rust project in `/home/user/indexer/`.
2. Write a Rust program that iterates over all `.md` files in `/home/user/docs_draft/`.
3. The program must process the files **concurrently** (e.g., using `std::thread`).
4. For each file, extract the title (the first line that starts with exactly `# `).
5. Append a line to `/home/user/docs_draft/index.txt` in the format: `Filename: Title` (e.g., `file1.md: # Welcome`).
6. **Crucial:** Because threads are writing to `index.txt` concurrently, you **must** use explicit file locking (e.g., using the `fs2` or `fs3` crate for cross-platform flock) to acquire an exclusive lock before writing and releasing it after. Do not rely on atomic appends.

**Phase 3: Manifest Generation (Rust)**
1. As the final step in your Rust program, after all threads have completed and the index is built, generate a SHA256 manifest of all files in `/home/user/docs_draft/` (all `.md` files AND the `index.txt`).
2. Save this manifest to `/home/user/docs_draft/manifest.sha256`. The format should exactly match the output of the `sha256sum` command (e.g., `[hash]  [filename]`). Order does not matter, but use just the filename (no directory path) in the manifest.

Run your scripts and the Rust program to leave the system in the requested final state.