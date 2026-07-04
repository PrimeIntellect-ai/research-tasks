I am a technical writer managing a huge library of documentation assets (archives containing markdown, JSON metadata, and embedded GCode for 3D printer manuals). Recently, a rogue archiving script corrupted our incoming pipeline by creating malicious archives that contain infinite symlink loops. 

I need you to build a secure Python-based archive validator that can inspect these documentation archives, detect malicious or invalid ones, and approve the clean ones.

Here are your requirements:
1. First, there is an image at `/app/docs/auth_stamp.png`. Use an OCR tool (like `tesseract`, which is installed) to read the text in this image. It contains a secret authorization token in the format `AUTH_TOKEN=XYZ`. You will need this token.
2. Create a Python script at `/home/user/validator.py`.
3. The script must accept two arguments:
   `python3 /home/user/validator.py --input <input_directory> --output <output_json_path>`
4. The script must process every `.tar` and `.tar.gz` file in the `<input_directory>`.
5. For each archive, classify it as either `"CLEAN"` or `"EVIL"` based on the following rules:
   - **EVIL Rule 1 (Symlink Loops):** If the archive contains any symbolic links that point back to parent directories in a way that creates an infinite loop, or point to absolute system paths (like `/etc/passwd`), it is EVIL.
   - **EVIL Rule 2 (Missing or Invalid Metadata):** The archive must contain a `meta.json` file at its root. If it is missing, or if the parsed JSON does not contain the key `"auth_token"` with the exact value extracted from the image in step 1, it is EVIL.
   - **EVIL Rule 3 (Malformed GCode):** If the archive contains any `.gcode` files, they must be parsed. If a `.gcode` file does not contain the exact line `; END OF GCODE` anywhere in its text, the archive is EVIL.
   - If an archive passes all the above checks, it is `"CLEAN"`.
6. The script must write a JSON file to `<output_json_path>` containing a single dictionary mapping the base filename of each archive to its classification. Example:
   ```json
   {
     "doc1.tar.gz": "CLEAN",
     "loop_bomb.tar": "EVIL"
   }
   ```

You can find a few sample archives to test your script in `/home/user/samples/`. When you are confident in your solution, simply ensure the script is saved at `/home/user/validator.py`. Automated verifiers will run your script against a hidden set of clean and evil archives.