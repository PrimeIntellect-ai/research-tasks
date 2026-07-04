You are a backup administrator tasked with archiving an older storage server. However, some of the files on the server are corrupted or are temporary cache files that should not be backed up. 

You have been provided with a scanned snippet of the backup policy at `/app/policy_scan.png`. 

Your objectives are:
1. Extract the backup exclusion rules from the image `/app/policy_scan.png`.
2. Write a C++ program and compile it to `/home/user/backup_filter`. The program must take a single file path as a command-line argument. It must inspect the file and exit with code 0 if the file is safe to back up, and exit with code 1 if the file violates the backup policy (is "evil" or "corrupted").
3. Apply your filter to the directory `/home/user/raw_data`. For every safe file, copy it into `/home/user/safe_data/`, and rename it by appending the `.safe` extension (e.g., `document.txt` becomes `document.txt.safe`). 
4. Archive the entire `/home/user/safe_data/` directory into a compressed tarball at `/home/user/backup.tar.gz`.

Ensure your C++ program is robust and handles binary files appropriately when scanning for the conditions mentioned in the policy.