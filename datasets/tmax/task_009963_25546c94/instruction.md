You are a developer tasked with organizing and restoring a legacy project archive. While cleaning up your `/home/user/legacy_project` directory, you found a custom-packed archive file named `archive.json` left by a former colleague.

The archive uses a proprietary serialization format combining JSON, Base64, Hex encoding, and a simple byte-shifting obfuscation method. The key to the byte shift was obfuscated using a snippet of custom pseudo-assembly language included in the JSON.

Your task is to write a Python script that parses `archive.json`, decodes the filenames and contents, translates the pseudo-assembly to determine the decryption key, and restores the files into `/home/user/restored_project/`.

Here are the specifications for the archive format and the obfuscation:

1. **Serialization Format**: `archive.json` has two main keys:
   - `decoder_asm`: A string containing pseudo-assembly instructions.
   - `files`: A list of objects, each containing `name_b64` (the Base64-encoded filename) and `content_hex` (the hex-encoded, obfuscated file contents).

2. **Pseudo-Assembly Language**: The `decoder_asm` snippet calculates an integer offset (the "key") in a single register `R1`. The instruction set is:
   - `MOV R1, X`: Set `R1` to the integer value `X`.
   - `ADD R1, X`: Add integer `X` to `R1`.
   - `SUB R1, X`: Subtract integer `X` from `R1`.
   - `SHR R1, X`: Perform a bitwise right-shift on `R1` by `X` bits.
   - `XOR R1, X`: Perform a bitwise XOR on `R1` with integer `X`.

3. **Decoding the Files**:
   - The original filename is simply the Base64 decoding of `name_b64` (assume utf-8).
   - The file content must be recovered by first decoding the `content_hex` string into raw bytes.
   - Then, to de-obfuscate the bytes, **subtract** the integer key calculated by the pseudo-assembly from each byte's integer value. If the subtraction results in a negative number, wrap it around (i.e., modulo 256).
   - The resulting decrypted bytes should be written to the restored file.

**Goal:**
1. Read `/home/user/legacy_project/archive.json`.
2. Extract the key by analyzing and translating the `decoder_asm`.
3. Decode and decrypt each file.
4. Create the directory `/home/user/restored_project/` and save the restored files there using their decoded filenames.
5. Create a file named `/home/user/restored_project/summary.txt` containing the decoded filenames, one per line, sorted alphabetically.

Write a Python script to automate this entire process, and execute it to restore the project files.