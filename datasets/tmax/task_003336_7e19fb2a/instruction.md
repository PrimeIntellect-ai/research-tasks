You are an artifact manager tasked with curating binary repositories. We need a reliable pipeline to process incoming artifact bundles, validate them, extract metadata, and move them to their final curated destination. 

However, our pipeline has been failing because some uploaded artifacts are "evil"—they contain malicious infinite symlink loops designed to crash backup scanners, or corrupted JSON metadata.

Your task has two main parts:

1. **Fix the Vendored Package:**
   We require you to use the `filelock` library to safely coordinate concurrent writes to an audit log. The source code for `filelock-3.12.2` is pre-vendored at `/app/vendor/filelock-3.12.2`. No internet access is available. 
   Unfortunately, a recent manual patch broke it. The Unix file locking implementation contains a deliberate syntax error/typo in the open flags (a non-existent `os.O_EXCLL` instead of `os.O_EXCL`). 
   - Locate the typo in the vendored `filelock` source, fix it, and install the package locally so your scripts can use it.

2. **Develop the Curation Script:**
   Write a Python script at `/home/user/curate.py` with the following CLI signature:
   `python /home/user/curate.py --input <input_dir> --output <output_dir> --log <log_csv_file>`

   The `<input_dir>` will contain several subdirectories, each representing a single artifact bundle.
   For each artifact bundle in the input directory, your script must:
   - Search for a `meta.json` file inside the bundle (it could be nested in subdirectories).
   - Carefully avoid infinite symlink loops during your search! If a symlink loop is detected, or if `meta.json` is missing or contains invalid JSON, the bundle is considered **EVIL** and must be entirely rejected (skipped).
   - If valid, parse `meta.json` to extract the `UUID` and `version` fields.
   - Consider the bundle **CLEAN**. Rename/move the entire artifact bundle directory to `<output_dir>/<UUID>_v<version>`.
   - Append a record to the `<log_csv_file>` in the format: `UUID,version,original_dir_name`. 
   - **Crucial**: You must use the fixed `filelock` package to lock the log file during writing, as we may run multiple instances of your script concurrently in production.

**Testing and Verification:**
To help you develop, we have provided two training corpora:
- `/app/corpus/clean/`: Contains perfectly valid artifact bundles.
- `/app/corpus/evil/`: Contains bundles with symlink loops or malformed metadata.
You can test your script against these.

When you are finished, the automated verifier will evaluate `/home/user/curate.py` against hidden test corpora. To pass, your script must:
- Successfully process 100% of the hidden clean corpus (all moved to output, logged accurately).
- Reject 100% of the hidden evil corpus (nothing moved to output, nothing logged, script does not crash or hang).