You are an AI assistant helping a technical writer organize and back up documentation. The writer has an old legacy documentation backup that was chunked into multiple parts, and a folder containing the current working state of the documentation.

Here is the situation:
- The legacy documentation is stored as a split tarball in `/home/user/legacy_split/`. The files are named `docs.tar.gz.part_aa`, `docs.tar.gz.part_ab`, etc.
- The current documentation state is located in `/home/user/current_docs/`.
- All documentation files currently have the prefix `draft_` (e.g., `draft_intro.md`).

Your task is to create an incremental backup of only the updated or newly added files, while simultaneously converting their naming convention for production. 

Perform the following steps:
1. Reassemble and extract the legacy documentation from `/home/user/legacy_split/` into a directory named `/home/user/extracted_legacy/`.
2. Write a **Rust program** at `/home/user/backup_tool.rs` and compile it. This program must:
   - Compare the contents of `/home/user/current_docs/` against the legacy documentation (which will be found at `/home/user/extracted_legacy/legacy_docs/` after extraction).
   - Identify files that are either **new** in `current_docs/` or have **modified content** compared to their legacy counterparts.
   - Copy these new/modified files to a new directory at `/home/user/diff_docs/`.
   - During the copy, perform a bulk rename: replace the `draft_` prefix in the filenames with `prod_` (e.g., `draft_intro.md` becomes `prod_intro.md`).
3. After the Rust program has completed this, package the `/home/user/diff_docs/` directory into a new archive named `/home/user/diff.tar.gz`. Make sure you are archiving the directory itself so it extracts as `diff_docs/`.
4. Finally, split `/home/user/diff.tar.gz` into 100-byte chunks in the `/home/user/final_archive/` directory. Use the prefix `diff.tar.gz.chunk_` for the output parts (e.g., `diff.tar.gz.chunk_aa`).

Ensure your Rust program correctly handles file reading and comparison. Use standard shell commands (like `cat`, `tar`, and `split`) alongside your Rust utility to handle the archives.