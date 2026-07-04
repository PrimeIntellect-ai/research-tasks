You are a build engineer responsible for packaging artifacts for a Web Application Firewall (WAF) project. You need to update the build pipeline, migrate the security rule database, and translate a legacy verification script. All of your work will take place in the `/home/user/waf_project` directory.

Complete the following objectives:

1. **Code Translation**: 
   There is a legacy Python script at `/home/user/waf_project/verify_sigs.py` that verifies the checksums of downloaded rule files. You must translate this script into a pure Bash script named `/home/user/waf_project/verify_sigs.sh`. 
   - The new script must take two arguments: the signature file path and the target directory. 
   - It must read the signature file (which uses the format `filename:sha256`) and verify the corresponding files in the target directory.
   - For each file, it must print exactly "OK: <filename>" if the SHA256 hash matches, or "FAIL: <filename>" if it does not.
   - The script must be executable.

2. **Schema Migration**: 
   The WAF rules are stored in an SQLite3 database located at `/home/user/waf_project/db/rules.sqlite`. 
   - The database currently contains a table `core_rules` with schema `(id INTEGER PRIMARY KEY, pattern TEXT)`.
   - Perform a schema migration to add a new column named `severity` of type `INTEGER` with a default value of `5`.

3. **Build System Configuration & Packaging**: 
   Modify the existing `/home/user/waf_project/Makefile` to add a new target named `release`. The `release` target must perform the following actions in order:
   - Run the newly created `./verify_sigs.sh signatures.txt downloads/` and save its output to `build_logs.txt`.
   - Create a tarball named `waf_release.tar.gz` that contains the migrated database (`db/rules.sqlite`) and all the files from the `downloads/` directory.

Ensure that running `make release` from `/home/user/waf_project` executes without errors and successfully creates both `build_logs.txt` and `waf_release.tar.gz`.