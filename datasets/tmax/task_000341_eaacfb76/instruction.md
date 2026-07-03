You are an artifact manager tasked with curating a messy directory of incoming software releases. 

You have been provided with an incoming drop directory at `/home/user/incoming`. This directory contains several binary archives (`.tar.gz` and `.zip`) and their accompanying metadata files (`.meta`). The metadata files are written in a legacy, pseudo-XML format.

Your objective is to write and execute a Bash script (`/home/user/curate.sh`) that processes these incoming artifacts and curates them into a structured repository at `/home/user/repo`.

Here are your specific requirements:

1. **Filter by Metadata:** Iterate through the artifacts in `/home/user/incoming`. You must ONLY process artifacts where the `<status>` tag in their `.meta` file is exactly `production`. Ignore any artifacts marked as `testing`, `development`, or anything else.

2. **Extract Archive Data:** For each "production" artifact, look inside its corresponding archive (`.tar.gz` or `.zip`). Inside the root of the archive, there is a text file named `build.txt` containing a line like `ID=some-build-string`. You need to extract this build string.

3. **Restructure:** Copy the valid archive files into the new repository structure based on the metadata. The destination path must be:
   `/home/user/repo/<arch>/<lowercase_name>-<version>.<extension>`
   (Note: The `<name>`, `<arch>`, and `<version>` must be parsed from the `.meta` file. `<extension>` is the original file extension, either `tar.gz` or `zip`).

4. **Generate Manifest:** Create a single JSON manifest file at `/home/user/repo/manifest.json` that contains an array of all curated artifacts. Each object in the array must match this exact format:
   ```json
   [
     {
       "name": "alphatools",
       "version": "2.1",
       "arch": "arm64",
       "build_id": "alpha-992",
       "file": "alphatools-2.1.tar.gz"
     }
   ]
   ```
   (The `name` in the JSON must be strictly lowercase).

Constraints:
- Use **Bash** as your primary tool. You may use standard Unix utilities like `sed`, `awk`, `grep`, `tar`, `unzip`, and `jq`.
- Do not use Python, Perl, or Ruby for the text processing.
- You must create the `/home/user/repo` directory and its subdirectories.
- Ensure your script handles both `.tar.gz` and `.zip` extractions appropriately to read `build.txt`.

Write and run your script to complete the curation. The task is complete when `/home/user/repo/manifest.json` and the corresponding directory structure are perfectly formed.