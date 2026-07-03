You are assisting a technical writer who organizes documentation and release artifacts for an embedded 3D printer controller project.

We have received an automated release archive at `/home/user/incoming/release_data.tar`, but our security scanner flagged it as potentially containing a "Zip Slip" directory traversal attack (it contains files that attempt to extract outside the intended directory). 

Your objective is to complete the following multi-phase task:

**Phase 1: Safe Extraction**
1. There is an extraction script at `/home/user/scripts/extract.py`. It is currently vulnerable to directory traversal. Modify it using Python so that it safely extracts `/home/user/incoming/release_data.tar` into `/home/user/docs_target`. Any file in the archive that attempts to escape `/home/user/docs_target` (e.g., via `../`) must be skipped entirely.
2. Run the fixed script to extract the archive.

**Phase 2: Metadata Search and Domain Parsing**
Using the safely extracted files in `/home/user/docs_target`, write a Python script `/home/user/scripts/analyzer.py` (and use any shell commands needed) to gather the following data:
1. **ELF Analysis:** Find all ELF executable files in the extracted directories that are larger than 5KB. Use `readelf` (or a Python library) to find their Entry Point address.
2. **GCode Analysis:** Find all `.gcode` files. Parse them to calculate the total extrusion value (the sum of all numeric values following the `E` parameter in `G0` or `G1` commands). Assume absolute extrusion (you just need to find the maximum E value reached in each file, or sum them if they are relative—assume absolute for this task, so just find the maximum E value in the file).
3. **Multi-line Log Parsing:** Find the `compile.log` file. Extract all multi-line "FATAL" records. A record starts with `[YYYY-MM-DD]` and a log level. A multi-line FATAL record continues until the next timestamped line. 

**Phase 3: Report Generation**
Using stream redirection and your script, generate a final Markdown report at `/home/user/docs_target/release_summary.md` with exactly this format:

```markdown
# Release Summary

## ELF Binaries
- [Filename]: Entry Point [0x...]

## GCode Artifacts
- [Filename]: Max Extrusion [X.XX]

## Fatal Errors
[Insert exact text of all FATAL log records, including their subsequent lines, separated by a blank line]
```

Ensure the malicious files from the tarball did *not* extract outside `/home/user/docs_target`. Do not run as root. You may install standard Python tools like `pyelftools` if needed.