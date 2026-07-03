I am a backup administrator tasked with archiving a massive legacy filesystem. We have a strict validation protocol for our custom `.bkp` archive files. 

Currently, we use a legacy, stripped binary located at `/app/legacy_validator` to check if an archive is valid and safe to store. However, this binary is painfully slow and cannot scale to our multi-terabyte drives. 

I need you to reverse-engineer the logic of `/app/legacy_validator` by treating it as a black-box oracle (or inspecting it with tools like `strings`, `xxd`, `objdump`), and write a fast, drop-in replacement script.

Here is your environment:
1. **The Oracle:** `/app/legacy_validator <filepath>` exits with `0` if a file is safe, and `1` if it is corrupted or malicious.
2. **The Corpora:** I have provided sample files to help you deduce the validation rules.
   - `/home/user/corpus/clean/` contains valid, safe archives.
   - `/home/user/corpus/evil/` contains invalid or malicious archives.
3. **The Target Directory:** `/home/user/incoming/` contains thousands of newly uploaded files of various types, modification dates, and states.

**Your Tasks:**
1. **Create the Filter:** Write a script at `/home/user/fast_filter.sh` that takes a single file path as its first argument. It must mimic the exact classification logic of the legacy validator. It must exit `0` for clean files and `1` for evil files. You may write this in Bash, Python, or Awk.
2. **Find and Classify:** Use your script and file metadata tools to search the `/home/user/incoming/` directory. Find all files that are:
   - Formatted as valid `.bkp` files (according to your filter), AND
   - Were modified within the last 7 days.
3. **Log the Results:** Write the absolute paths of all matching, safe files from the `incoming` directory to `/home/user/clean_backups.log`, one path per line, sorted alphabetically.

Make sure your `/home/user/fast_filter.sh` is perfectly accurate against the provided corpora, as it will be tested against a hidden holdout set of evil and clean archives!