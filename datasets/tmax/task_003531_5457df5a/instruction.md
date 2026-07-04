You are acting as a technical writer tasked with organizing and formatting a legacy documentation repository for a new static site generator. 

You have been provided with an archive of legacy documentation and a set of instructions.

Here are your tasks:

1. **Tool Setup (Vendored Package)**:
   A third-party Bash documentation generator, `shdoc`, is provided as a vendored source tarball at `/app/shdoc-0.2.tar.gz`. You need this tool to generate API docs for some of the shell scripts in the repository. 
   Extract it and install it. **Note**: You do not have `sudo` privileges. Furthermore, this specific version has a known misconfiguration where it hardcodes the `AWK` path to `/opt/bin/gawk` inside the `shdoc` executable, which will fail on this system. You must fix this perturbation so that `shdoc` uses the standard system `gawk` or `awk` before using it. Install the working executable to `/home/user/.local/bin/` and ensure it is in your `PATH`.

2. **Archive Verification & Extraction**:
   The legacy documentation is stored in `/home/user/legacy_docs.tar.gz`. 
   Verify its integrity against the checksum in `/home/user/legacy_docs.md5`. 
   Once verified, extract the contents to `/home/user/extracted_docs/`.

3. **Configuration Interpretation & File Moving**:
   Inside the extracted directory, there is a file named `mapping.conf`. It contains routing rules in the format `old_filename.md:new_directory/new_filename.md`.
   Create a new directory at `/home/user/organized_docs/`.
   Read `mapping.conf` and move/rename each file from the extracted directory into `/home/user/organized_docs/` according to the rules. Create any necessary parent directories.

4. **Text Transformation (Link Conversion)**:
   The legacy markdown files use an old wiki-style link format: `[[My Target Page]]`.
   Using Bash/`sed`/`awk`, you must recursively process all `.md` files in `/home/user/organized_docs/` and convert these to standard Markdown links: `[My Target Page](My_Target_Page.md)`.
   Specifically, the display text inside the brackets remains exactly the same, but the URL part must have spaces replaced with underscores and end with `.md`. 
   *Example:* `[[Setup Guide]]` becomes `[Setup Guide](Setup_Guide.md)`.

5. **Generate Script Documentation**:
   There is a file `/home/user/organized_docs/scripts/deploy.sh`. 
   Use your fixed `shdoc` tool to generate markdown documentation from this script.
   Save the output to `/home/user/organized_docs/scripts/deploy_api.md`.

6. **Final Packaging**:
   Once all files are moved, links are transformed, and the API doc is generated, create a final compressed archive of the `/home/user/organized_docs/` directory at `/home/user/final_docs.tar.gz`.

Your success will be evaluated by an automated script checking the accuracy of your wiki-link conversion across all files, as well as the presence of the `shdoc` generated file. You should aim for 100% link conversion accuracy.