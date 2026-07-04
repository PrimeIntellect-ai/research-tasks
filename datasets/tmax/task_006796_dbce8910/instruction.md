You are an artifact manager responsible for curating a local repository of binary archives. We have a staging directory containing several application packages that need to be reviewed and promoted.

Your task is to process the archives located in `/home/user/artifacts/` and prepare them for production.

Here are the requirements:
1. **Analyze Archives:** The directory `/home/user/artifacts/` contains several `.zip` and `.tar.gz` files. Each archive contains a text file named `manifest.txt` and a binary file named `data.bin`.
2. **Transform Metadata:** For every archive, read `manifest.txt`. Look for the key-value pair `STATUS=...`. 
    - If the status is `STATUS=staging`, you must update it to `STATUS=production`.
    - If the status is anything else (e.g., `STATUS=development`), you must leave it completely unchanged.
3. **Repackage Atomically:** 
    - Create a new directory `/home/user/curated_artifacts/`.
    - For archives that required a status change, create a *new* archive of the same format and name in `/home/user/curated_artifacts/` containing the updated `manifest.txt` and the original `data.bin`. Do not extract and leave temporary files cluttering the working directory; ensure you manage temporary files properly and write the final archive atomically.
    - For archives that did *not* require a status change, simply copy the original archive into `/home/user/curated_artifacts/` without modifying it.
4. **Generate Report:** Create a summary report at `/home/user/curation_report.txt`. The report must contain exactly one line per archive processed, in alphabetical order by the archive filename. The format of each line must be exactly:
    `[Modified] filename` (if the status was updated)
    `[Unchanged] filename` (if the status was not updated)

Ensure that your final curated archives are valid `.zip` or `.tar.gz` files (matching their original format) and that no binary data in `data.bin` is corrupted during the extraction and repackaging process. You may use any combination of bash, awk, sed, or Python to complete this task.