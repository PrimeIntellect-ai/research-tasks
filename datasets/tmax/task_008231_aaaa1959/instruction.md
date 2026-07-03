I am a technical writer organizing our software documentation. I have several old documentation archives that need to be extracted, processed, and repackaged into a new release bundle. 

I need you to write and execute a Bash script (or run the commands) to perform the following exact steps:

1. **Extract Archives**: I have a directory `/home/user/docs_raw/` containing three archives: `v1.0.tar.gz`, `v1.1.tar.gz`, and `v2.0-draft.tar.gz`. Extract them into `/home/user/docs_processed/`. Each archive contains a single directory matching its version name (e.g., `v1.0`), which contains a `README.md` (text) and an `api.bin` (binary).

2. **Prepare the Release Directory**: Create a new directory `/home/user/release/`.

3. **Copy Binary Data**: Find the `api.bin` file inside the extracted `v2.0-draft` directory and copy it to `/home/user/release/api.bin`.

4. **Atomic Text Update**: Read the `README.md` file from the extracted `v1.1` directory. Append the exact text `CONFIDENTIAL - DRAFT STATUS` as a new line at the end of the text. To ensure atomic writes, write this updated content to a temporary file `/home/user/release/.README.md.tmp`, and then move (`mv`) it to `/home/user/release/README.md`.

5. **Create a Symbolic Link**: Inside the `/home/user/release/` directory, create a symbolic link named `latest_api` that points to `api.bin` within the same directory. The link must be a relative symlink.

6. **Create the Final Archive**: Compress the entire `/home/user/release/` directory into a new gzip-compressed tar archive located at `/home/user/final_archive.tar.gz`. The archive should store the `release` folder at its root (so extracting it creates the `release` directory).

Make sure all commands are run successfully. The final verification will check the structure and contents of `/home/user/final_archive.tar.gz`.