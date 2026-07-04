You are a storage administrator managing disk space on a Linux server. An application has been dumping a mix of valid text logs and corrupted binary memory dumps into a single spool directory, `/home/user/storage_spool/`. You need to identify the corrupted files, rename them, and safely generate a space usage report.

Please write and execute a Python script to perform the following operations:

1. **Identify and Rename Corrupted Files (Binary/Text Reading & Bulk Renaming):**
   - Iterate through all files in `/home/user/storage_spool/`.
   - Read each file to determine if it is a binary dump. For this task, a file is strictly considered "binary" if it contains one or more null bytes (`\x00`). 
   - If a file is binary, rename it by appending the `.bak` extension (e.g., `file.dat` becomes `file.dat.bak`).
   - Leave the valid text files (those without any null bytes) with their original names.

2. **Generate a Usage Report (Atomic Write):**
   - Calculate the total combined size (in bytes) of all the valid text files remaining in the directory (do not include the `.bak` files in this calculation).
   - Write this single integer value to a report file located at `/home/user/text_size_report.txt`.
   - **Crucial Requirement:** The report must be written atomically to prevent monitoring tools from reading a partial file. You must write the integer to a temporary file named `/home/user/text_size_report.txt.tmp` first, flush/close it, and then rename it to `/home/user/text_size_report.txt` replacing the destination if it exists.

Ensure your script handles everything programmatically. You can run the script via the terminal.