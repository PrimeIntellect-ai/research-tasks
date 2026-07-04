You are an artifact manager tasked with curating a legacy binary repository. A previous system dumped several files into `/home/user/artifacts`, but the file extensions are unreliable and the internal encodings are outdated. 

Your objective is to identify valid archives, extract their contents, normalize the files, and package them into a curated release.

Perform the following steps:
1. Scan the directory `/home/user/artifacts` for files that are actually ZIP archives, regardless of their current file extension. Ignore any files that are not valid ZIP archives.
2. Extract the contents of the identified ZIP archives into a new directory: `/home/user/extracted`.
3. In `/home/user/extracted`, process the extracted files as follows:
   - **Text Files**: All `.txt` files are currently encoded in `ISO-8859-1`. Convert their character encoding to `UTF-8` in-place (overwrite the original `.txt` files with the UTF-8 versions).
   - **Binary Files**: All `.blob` files contain an embedded 4-byte header. Read the first 4 bytes of each `.blob` file, convert those bytes to a lowercase hex string (8 characters), and rename the file to `<hex_string>.blob`.
4. Generate a manifest file at `/home/user/manifest.log`. This file must contain the `sha256sum` of every file inside `/home/user/extracted` after processing. The output should be standard `sha256sum` format, and the lines must be sorted alphabetically by the filename (just the basename, e.g., `sha256sum * | sort -k2`).
5. Finally, compress the processed `/home/user/extracted` directory into a gzip-compressed tarball at `/home/user/curated_artifacts.tar.gz`. The tarball should contain the `extracted` directory at its root.

Constraints:
- Use bash and standard coreutils. 
- You do not have root access. Ensure you place outputs exactly at the specified absolute paths.