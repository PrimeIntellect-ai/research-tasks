You are assisting a technical writer who aggregates documentation submissions from various open-source communities. The writer receives documentation bundles as nested archives (zips inside tarballs, etc.) but has been running into issues with malformed submissions, malicious filesystem artifacts, and broken extraction tools.

Your objective is to fix their extraction tool and then write a robust Bash classifier to filter incoming documentation bundles.

**Phase 1: Fix the Extraction Tool**
We have a vendored package at `/app/vendored/doc-unpack-1.2.0` that the writer uses to extract complex nested documentation archives. 
Currently, the tool is broken. The `Makefile` and the main extraction script (`bin/unpack.sh`) have a deliberate misconfiguration (a corrupted environment variable and a broken pipeline for multi-part archives). 
1. Identify and fix the perturbation in `/app/vendored/doc-unpack-1.2.0`. 
2. Ensure you can successfully build and run it. The known-good code path requires running `make install` to place the binary at `/usr/local/bin/doc-unpack`.

**Phase 2: Build the Classifier**
Write a Bash script at `/home/user/filter_docs.sh` with the following signature:
`bash /home/user/filter_docs.sh <input_corpus_dir> <output_dir>`

The `<input_corpus_dir>` will contain multiple documentation bundles (which are `.tar.gz` files containing heavily nested zip files, metadata, and multi-line changelogs).

Your script must:
1. Iterate over every archive in the `<input_corpus_dir>`.
2. Extract the archive into a secure, temporary directory using the fixed `doc-unpack` tool.
3. Use metadata-based file searches to inspect the extracted contents.
4. Accept the bundle (by copying the entirely extracted directory structure into a subdirectory of `<output_dir>` named after the archive's base name) ONLY IF it is completely clean. 
5. Reject the bundle (do not copy it to `<output_dir>`) if it contains any "evil" attributes.

A bundle is considered **EVIL** (must be rejected) if ANY of the following are true:
- It contains any symlinks pointing to absolute paths outside the extraction directory.
- It contains any file ending in `.md` or `.txt` that has executable permissions.
- It contains a `metadata.json` file that is invalid JSON.
- Its `changelog.log` contains multi-line record blocks where the `Author:` field attempts to execute a subshell (e.g., contains `$(` or backticks).

A bundle is considered **CLEAN** (must be preserved) if:
- It safely extracts without absolute symlinks.
- Markdown and text files have standard read/write permissions (no execute bits).
- `metadata.json` is perfectly valid JSON.
- Multi-line logs contain standard alphanumeric text.

**Validation**
There are two corpora located at `/app/corpora/clean/` and `/app/corpora/evil/`. 
Your script will be tested against both. To succeed, your script must achieve a 100% preservation rate of the clean corpus, and a 100% rejection rate of the evil corpus.