You are an artifact manager curating a binary repository pipeline. We have a stripped proprietary binary packing tool located at `/app/bin/packer`. This tool takes a directory and packs it into our custom `.pck` format.

However, `/app/bin/packer` has a known flaw: it blindly follows symbolic links. If it encounters a symlink loop, it will eagerly resolve it up to a hardcoded depth limit of 1000, resulting in massively bloated output files (often >500MB) before it eventually finishes. 

Your objective is to write a Python script `/home/user/curate.py` (and execute the necessary bash commands) to safely prepare the repository and pack it, minimizing the final output size.

Here is the workflow you must automate:
1. **Extract**: Extract the incoming archive `/app/incoming/raw_artifacts.tar.gz` to a new directory `/app/staging`.
2. **Parse & Filter**: Parse the multi-line log file `/app/logs/audit.log`. Records are multi-line, starting with `BEGIN RECORD` and ending with `END RECORD`. You must find all records where `Status: VULNERABLE` or `Status: DEPRECATED`. Extract the `Filename:` field from these records and permanently delete those files from `/app/staging`.
3. **Link Management**: Scan `/app/staging` for symbolic links. Detect any symlinks that form an infinite loop OR point to targets outside of `/app/staging`. Remove these invalid/looping symlinks so the packer doesn't bloat the archive. Preserve valid hard links and valid, non-looping symlinks.
4. **Pack**: Execute the black-box packer. Standard stream redirection must be used to save the packer's stdout to `/app/logs/packer_out.log`. 
   The packer syntax is: `/app/bin/packer <source_dir> <output_file>`
   You must pack `/app/staging` into `/app/final_artifact.pck`.

A successful execution will result in `/app/final_artifact.pck` being optimally small (only containing the clean, non-duplicated, non-vulnerable binaries). Ensure you execute your script so the final `.pck` file is generated.