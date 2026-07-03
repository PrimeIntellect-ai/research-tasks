You are acting as an artifact manager for a software repository. A legacy build system has just dumped a batch of binary archives into your staging directory, but the filenames are obfuscated. Along with the binaries, the system provided a multi-line manifest log file that maps the obfuscated temporary names to their real artifact names. 

Because the legacy system runs on an old Windows environment, the manifest file was written in UTF-16LE encoding, which is causing issues with our standard Unix tools.

Your task is to curate these binary repositories by doing the following:

1. Navigate to `/home/user/artifacts`.
2. You will find a manifest file named `incoming_manifest.log`. Convert its character encoding from UTF-16LE to UTF-8 and save it as `manifest_utf8.log`.
3. The manifest file contains multi-line records formatted exactly like this:
   ```
   [Artifact]
   Temp-Name: <obfuscated_filename>
   Real-Name: <proper_filename>
   Timestamp: <date>
   ```
4. Parse this multi-line log to extract the mappings between `Temp-Name` and `Real-Name`.
5. Bulk rename all the corresponding obfuscated archive files in the `/home/user/artifacts` directory to their `Real-Name`. (e.g., if `Temp-Name: bin_001.tar.gz` and `Real-Name: database-v1.tar.gz`, rename the file accordingly).
6. Once all files are renamed, package ONLY the newly renamed `.tar.gz` files into an uncompressed tar archive named `/home/user/curated_artifacts.tar`. Do not include the directories in the tar paths (i.e., the files should be at the root of the tar archive).
7. Finally, list the contents of `/home/user/curated_artifacts.tar` and save the output to `/home/user/final_list.txt`, sorted alphabetically.

Ensure your parsing and renaming logic is robust enough to handle the multi-line nature of the log records.