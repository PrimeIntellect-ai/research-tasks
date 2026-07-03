You are acting as a support engineer. A user has reported that their automated backup script, `/home/user/backup.sh`, is failing to back up certain files. They mentioned that the script seems to break whenever filenames contain spaces. 

Your task is to:
1. Examine and comprehend the existing `/home/user/backup.sh` script.
2. Fix the script so that it correctly handles filenames with spaces. The script should copy all `.txt` files from a source directory (provided as the first argument) to a destination directory (provided as the second argument) without skipping or mangling names.
3. Run the fixed script to back up the contents of `/home/user/data/` to `/home/user/backup_dir/`.
4. After successfully running the backup, generate a diagnostic log file at `/home/user/success.log` that lists the base names (just the filename, not the full path) of all the `.txt` files present in `/home/user/backup_dir/`. The list must be sorted alphabetically, with one filename per line.

Ensure that the script only uses standard bash built-ins and coreutils.