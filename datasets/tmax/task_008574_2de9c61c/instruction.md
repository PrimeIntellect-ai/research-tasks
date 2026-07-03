You are an AI assistant helping a technical writer aggregate and archive a series of scattered documentation files into a single master archive. The documentation files are located in `/home/user/raw_docs/`.

Because the number of documents can be large, you need to write a Bash script that processes these files concurrently. However, writing to the single master archive concurrently will cause data corruption if not handled properly.

Your task is to create a Bash script at `/home/user/build_archive.sh` that does the following:

1. Loops through all `.txt` files in `/home/user/raw_docs/`.
2. Processes each file **concurrently** (as a background job).
3. Applies a "custom compression" pipeline to each file's stream:
   - Removes all completely empty lines.
   - Removes all ASCII vowels (both lowercase and uppercase: a, e, i, o, u, A, E, I, O, U).
   - Encodes the resulting text using `base64` (standard base64 output, wrapping is fine as long as it's standard).
4. Safely appends the processed stream to `/home/user/master_archive.b64` using file locking (`flock`) to prevent concurrent write interlacing. 
5. The format appended to the master archive for each file MUST be exactly:
   ```
   ---[<filename>]---
   <base64_encoded_content>
   ---[EOF]---
   ```
   *(Note: `<filename>` should be just the basename of the file, e.g., `doc1.txt`)*
6. The script must wait for all background jobs to finish before exiting.

Ensure your script is executable (`chmod +x /home/user/build_archive.sh`). 

Execute your script so that `/home/user/master_archive.b64` is generated. The automated test will verify the contents of the archive and analyze your script for concurrent background job usage (`&`) and file locking (`flock`).