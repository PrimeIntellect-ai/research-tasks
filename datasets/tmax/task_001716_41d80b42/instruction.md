As a researcher, I have a collection of compressed dataset archives in `/home/user/datasets`. Some of these archives are untrusted and might contain "zip slip" payloads (paths that attempt to traverse parent directories using `../` or absolute paths like `/etc/passwd`).

Write and execute a Python script at `/home/user/process_datasets.py` to do the following:

1. Scan all `.zip` and `.tar.gz` files in `/home/user/datasets`.
2. Identify any archive that contains a path traversing outside the archive root (e.g., starts with `/` or contains `../` as a path component). Write the filenames (just the basename, e.g., `bad_data.zip`) of these malicious archives, one per line, to `/home/user/malicious.log`.
3. For the **safe** archives, process their contents directly from the compressed stream (do NOT extract them to disk).
4. For any `.gcode` file found inside a safe archive, parse it and calculate the total extrusion length. This is the sum of all `E` values in lines that start with `G1` and contain an `E` parameter (e.g., `G1 X10 E5.5` contributes 5.5).
5. For any ELF file inside a safe archive (identified by the `\x7fELF` magic number at the start of the file, regardless of its extension), read its ELF header to determine the machine architecture. The `e_machine` field is a 2-byte integer at offset `0x12`. Assume all ELF files in the dataset are little-endian. Extract this integer value.
6. Output a JSON file at `/home/user/report.json` with the exact following structure:
```json
{
  "safe_archive1.zip": {
    "gcode_totals": {
      "path/to/file1.gcode": 150.5
    },
    "elf_architectures": {
      "path/to/program1.bin": 62
    }
  }
}
```

Constraints:
- You must write the Python script and run it to produce the outputs.
- Do not extract safe archives to disk; process streams in memory.
- Round the GCode totals to 1 decimal place in the JSON.