You are assisting a configuration manager in auditing and normalizing historical server configurations that have drifted over time. 

You have been provided with a nested backup archive located at `/home/user/config_backups.tar.gz`. This archive contains several layers of compression that you must navigate and extract.

Your task consists of the following phases:

1. **Extraction and Navigation**:
   Extract the contents of `/home/user/config_backups.tar.gz` into the directory `/home/user/extracted/`. 
   Inside the root of the first archive, you will find directories for different servers (e.g., `server_alpha`, `server_beta`). Each of these directories contains a `backup.zip` file. Inside each `backup.zip` is a `data.tar.bz2` archive. Extract all of these nested archives so that the raw `.conf` files inside `data.tar.bz2` are placed directly into their respective server directories in `/home/user/extracted/` (e.g., `/home/user/extracted/server_alpha/app.conf`).

2. **Configuration Normalization (Text Transformation)**:
   Write a script (in Python, Ruby, Perl, or Bash) saved at `/home/user/normalize.py` (or respective extension) that traverses the `/home/user/extracted/` directory, processes all `.conf` files, and applies the following modifications in-place:
   - Change any line containing exactly `Port 8080` to `Port 443`.
   - Change any line containing exactly `LogLevel debug` to `LogLevel warn`.
   - Delete entirely any line that begins with exactly `# DEPRECATED` (including leading whitespace if the `#` is the first non-whitespace character).

3. **Logging**:
   Your script must generate a log file at `/home/user/changelog.txt` recording which files were modified. The format of `/home/user/changelog.txt` must be exactly as follows, with files sorted alphabetically:
   ```
   Modified files:
   server_alpha/app.conf
   server_beta/db.conf
   Total modified: <number>
   ```
   *Note: Only list the relative path from `/home/user/extracted/` for files that actually had at least one line changed.*

4. **Repackaging**:
   Finally, package the normalized `/home/user/extracted/` directory into a new archive at `/home/user/normalized_configs.tar.gz`. The archive should contain the `server_*` directories at its root (e.g., running `tar -tzf` should output `server_alpha/app.conf`, not `extracted/server_alpha/app.conf`).

Make sure your script operates efficiently, as there may be hundreds of files.