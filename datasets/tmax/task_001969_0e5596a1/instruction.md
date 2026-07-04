You are acting as an AI assistant for a technical writer trying to recover and organize a corrupted documentation repository. Recently, the internal documentation system was infected by a malware strain that scattered malicious files disguised as documentation, and created symlink loops to confuse our scripts. 

Before the lead architect went on leave, they left a voice memo detailing the new proprietary compression format they used for the latest documentation, and how to identify the legitimate files.

Your task is to write a robust Bash script that identifies, decrypts, and organizes the valid documentation while safely rejecting any malicious or corrupted files.

Here is what you need to do:

1. **Listen to the Voice Memo:**
   Extract the instructions from the audio fixture located at `/app/architect_memo.wav`. You can use `whisper` or other tools available in your environment to transcribe it. The memo contains critical information about:
   - The custom compression/encoding sequence used for legitimate files.
   - The exact magic string (signature) that legitimate files begin with after decompression.

2. **Create the Processor Script:**
   Write a Bash script at `/home/user/process_doc.sh`. The script will be invoked as follows:
   `bash /home/user/process_doc.sh <input_file_path> <output_file_path>`

   For each file, the script must:
   - Safely determine if the input file is a regular file (rejecting symlink loops, directories, or broken links).
   - Decompress/decode the file according to the method described in the audio memo.
   - Verify that the decompressed content starts with the exact magic string specified in the memo.
   - If the file is **valid (clean)**: Write the decompressed content to `<output_file_path>`, append the output file's base name to `/home/user/master_index.txt` using strict file locking (`flock`) to ensure safe concurrent access, and exit with status `0`.
   - If the file is **invalid, malicious, or corrupted (evil)**: Do not write to `<output_file_path>`, do not modify the index, and exit with status `1`.

3. **Adversarial Verification:**
   We have provided two testing directories:
   - `/app/corpus/clean/`: Contains strictly valid, properly encoded documentation files.
   - `/app/corpus/evil/`: Contains malicious files, symlink loops, incorrect magic strings, and malformed data.
   
   An automated verifier will run your `/home/user/process_doc.sh` in parallel against all files in both corpora. To pass, your script must exit `0` for 100% of the clean files, and exit `1` for 100% of the evil files. It must also correctly decompress the clean files and populate the master index safely without race conditions.

Ensure your script is executable (`chmod +x /home/user/process_doc.sh`). You may use any standard Linux utilities available (like `tac`, `base64`, `head`, `flock`, `stat`, etc.).