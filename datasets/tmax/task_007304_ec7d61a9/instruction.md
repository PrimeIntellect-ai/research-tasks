You are a storage administrator managing a Linux file server. A failing block device was recently rescued using a low-level carving tool. The recovered chunks of data are located in `/home/user/recovered_data/`. The files are simply named `chunk_01`, `chunk_02`, etc., and they are missing their file extensions. Furthermore, the recovery process extracted many exact duplicate files, which are wasting valuable disk space. 

Your task is to analyze, organize, deduplicate, and report on these recovered files using only standard Bash tools (coreutils, awk, sed, etc.). Python, Perl, and other scripting languages are not allowed.

Perform the following operations:

**Phase 1: Binary Header Extraction and Renaming**
Read the first 4 bytes (the "magic number") of every file in `/home/user/recovered_data/`. Based on these bytes, rename each file in-place to append the correct extension. 
Use the following signature mappings (represented in hexadecimal):
- `89 50 4e 47` -> append `.png`
- `25 50 44 46` -> append `.pdf`
- `ff d8 ff e0` -> append `.jpg`
- `7f 45 4c 46` -> append `.elf`
If a file does not match any of these signatures, do not append any extension.

**Phase 2: Deduplication via Hard Links**
To save disk space, find all identical files (based on their actual content/hash) within `/home/user/recovered_data/`.
For each group of identical files:
1. Identify the "canonical" file: the one that comes first alphabetically by its new filename (e.g., `chunk_01.png` comes before `chunk_03.png`).
2. Replace all other identical files in the group with **hard links** pointing to the canonical file. The filenames of the duplicates must remain exactly the same as they were after Phase 1.

**Phase 3: Organization via Symbolic Links**
Create a new directory `/home/user/by_type/`.
Inside this directory, create subdirectories for each extension found (e.g., `/home/user/by_type/png/`, `/home/user/by_type/pdf/`).
Inside each subdirectory, create **symbolic links** pointing to the **canonical** files only (do not create symlinks for the duplicates). The symlink name should match the canonical file's name.

**Phase 4: Text Transformation & Reporting**
Create a report at `/home/user/recovery_summary.txt`.
The report must contain exactly one line for each canonical file that has at least one hard link (i.e., files that had duplicates).
The format for each line must be exactly:
`<canonical_filename> has <total_number_of_hard_links> links`
Sort the lines in the report alphabetically by the canonical filename.

Example line:
`chunk_01.png has 2 links`

**Constraints:**
- Do not use Python, Ruby, Perl, or any non-Bash scripting language.
- Ensure you are working entirely within `/home/user/`.