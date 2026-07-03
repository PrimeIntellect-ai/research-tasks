You are tasked with migrating a set of legacy configuration files for a configuration management system. The old system wrote configuration snapshots in a custom INI-like format using the ISO-8859-1 character encoding. The new system requires these configurations to be strictly formatted as JSON and encoded in UTF-8.

You will find an archive containing the legacy configurations at:
`/home/user/legacy_configs.tar.gz`

Your objective is to:
1. Extract the `legacy_configs.tar.gz` archive. Inside, you will find a directory named `legacy_input` containing several `.conf` files.
2. Write a C program (saved at `/home/user/converter.c`) that:
   - Takes two command-line arguments: an input directory and an output directory.
   - Iterates through all `.conf` files in the input directory.
   - Parses the INI format. The format consists of sections like `[SectionName]` and key-value pairs like `Key=Value`.
   - Converts the text from ISO-8859-1 encoding to UTF-8.
   - Converts the parsed data into a valid JSON object where top-level keys are the section names, and their values are objects containing the key-value pairs for that section.
   - Saves the resulting JSON into the output directory with the same base name but a `.json` extension (e.g., `app1.conf` becomes `app1.json`).
3. Compile your C program and run it, specifying the extracted `legacy_input` directory as the input and a new directory `/home/user/json_output` as the output.
4. Package the processed JSON files into a new gzip-compressed tar archive located at:
   `/home/user/modern_configs.tar.gz`
   The archive should contain the JSON files directly at its root (or inside a `json_output` directory, either is acceptable as long as the files are correctly named and formatted).

**Requirements for the C program:**
- Must be written entirely in C.
- You may use standard POSIX libraries (like `dirent.h` for directory traversal) and `iconv.h` for character encoding conversion.
- The output must be valid JSON. Ensure strings are properly formatted.

**Example Input (`test.conf` in ISO-8859-1):**
```
[General]
Name=Café
[Network]
Host=españa.local
```

**Expected Output (`test.json` in UTF-8):**
```json
{
  "General": {
    "Name": "Café"
  },
  "Network": {
    "Host": "españa.local"
  }
}
```
*(Whitespace/indentation in the JSON output does not matter as long as it is valid JSON).*