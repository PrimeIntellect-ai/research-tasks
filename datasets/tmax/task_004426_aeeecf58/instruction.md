You are acting as a configuration manager for a legacy web service. A faulty backup script recently ran on the server, creating recursive symlinks that lead to infinite loops. Additionally, the system's old configuration files need to be updated to a new format, encoding, and naming convention.

Your task is to create and run a Python script at `/home/user/update_configs.py` that performs the following operations:

1. Traverse the directory tree starting at `/home/user/configs`. You must explicitly detect and ignore any symlinks to avoid falling into infinite loops.
2. Identify all configuration files that end with the `.oldconf` extension.
3. Read each identified `.oldconf` file. Note that these legacy files are strictly encoded in `ISO-8859-1`.
4. Perform a bulk text edit on the content of each file:
   - Replace every occurrence of the exact string `DEBUG_LEVEL=1` with `DEBUG_LEVEL=3`.
   - Replace every occurrence of the exact string `ENVIRONMENT=staging` with `ENVIRONMENT=production`.
5. Write the modified content to a new file in the exact same directory, but change the file extension to `.newconf`.
6. The new `.newconf` files must be saved using `UTF-8` encoding.
7. Delete the original `.oldconf` files after successfully creating the `.newconf` files.

Ensure your script handles the directory traversal safely. Once the script is written, execute it so that the state of `/home/user/configs` is fully updated.