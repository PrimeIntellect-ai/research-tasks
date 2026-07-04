You are an AI assistant helping a technical writer safely process and organize a messy dump of legacy documentation.

I have an archive located at `/home/user/docs.tar`. In the past, extracting similar archives caused system issues because they contained malicious symlinks that pointed outside the extraction directory and overwrote configuration files (similar to a zip-slip attack). 

Your task is to write and execute a Bash script (`/home/user/process_docs.sh`) that safely extracts, cleans, and organizes this archive. 

Here are the strict requirements for your script:
1. **Extraction:** Create a directory `/home/user/workspace` and extract `/home/user/docs.tar` into it.
2. **Link Management (Safety First):** Recursively traverse `/home/user/workspace`. Find and delete any symbolic links that resolve to a path outside of `/home/user/workspace`. You must leave safe, internal symbolic links intact.
3. **Binary Extraction:** Analyze the files to separate binaries from text. Any file that is binary (i.e., its MIME type does not start with `text/` and it is a regular file, not a symlink) must be moved to `/home/user/assets/`. When moving, append `.bin` to the filename if it doesn't already have an extension.
4. **Encoding Conversion:** Many of the remaining text files are encoded in `ISO-8859-1`. Check the charset of each text file. If it is `iso-8859-1`, convert its contents to `UTF-8` in place.
5. **Bulk Renaming:** For all regular text files remaining in `/home/user/workspace`, rename them to have a `.md` extension. If a file already has an extension (like `.txt`), replace it with `.md`. If it has no extension, append `.md`.
6. **Manifest Generation:** Finally, create a manifest file at `/home/user/manifest.txt` listing all regular files (not directories or symlinks) in `/home/user/workspace` and `/home/user/assets/` after processing. Each line must be formatted exactly as:
`[absolute_path] | [sha256sum]`
Sort the manifest alphabetically by the absolute path.

Execute your script so the final state matches these requirements.