You are assisting a configuration manager in auditing a legacy system's configuration artifacts. Over the years, configuration files have been stored in custom binary wrappers across complex directory structures. We need to extract the actual text configurations, normalize their encoding, and generate a manifest to track them.

Your task is to process a snapshot located in the directory `/home/user/legacy_configs/`.

Perform the following steps:

1. **Find Valid Configuration Files:** Search recursively through `/home/user/legacy_configs/` to find all files that begin with a specific 8-byte binary magic header. The header in hexadecimal is: `43 46 47 01 00 00 00 00`.

2. **Extract and Convert:** For each file that has this exact header:
   - Extract the payload data (everything immediately following the first 8 bytes).
   - The payload is plain text but encoded in `UTF-16LE`. Convert this text into `UTF-8`.
   - Create a directory called `/home/user/converted_configs/` if it does not exist.
   - Save the converted UTF-8 text into this directory using the original filename with `.utf8` appended to it. Flatten the directory structure (e.g., if the original file was `nested/dir/app.cfg`, save it as `/home/user/converted_configs/app.cfg.utf8`). You can assume all original base filenames are unique.

3. **Generate Manifest:** Generate a JSON manifest file at `/home/user/manifest.json`. The JSON should be a single object mapping the *original base filename* (without the directory path, but keeping its original extension) to the SHA-256 checksum of its corresponding newly created `.utf8` file.

Example of the expected `/home/user/manifest.json` format:
```json
{
  "app.cfg": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "router.bin": "8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92"
}
```

Only include files in the manifest that possessed the valid magic header. Do not include decoy or corrupted files.