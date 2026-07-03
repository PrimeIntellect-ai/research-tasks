You are a storage administrator responsible for managing and migrating user-uploaded archives. To optimize disk space, you need to extract thousands of old ZIP archives and convert their text contents into a single concatenated format. However, you suspect some of these archives are malicious and contain "Zip Slip" directory traversal attacks (e.g., files named `../../etc/passwd` or `/var/run/script.sh`). 

Your task involves three steps:

1. **Fix the Archive Library**: 
   We rely on a vendored copy of the `patool` library located at `/app/patool-1.12`. Unfortunately, a previous administrator accidentally corrupted its source code while trying to apply a patch, so it currently fails to install or run. Find the deliberate syntax error or perturbation in the vendored `patool` package, fix it, and install the package into your system Python environment.

2. **Create the Safe Converter**:
   Write a Python script at `/home/user/safe_converter.py` that takes two arguments:
   `python /home/user/safe_converter.py <input_archive.zip> <output_dir>`

   The script must use the newly installed `patool` (or standard `zipfile` module, if you prefer to use standard libraries for extraction and `patool` for initial inspection) to handle the archive. 

   **Security Requirements (Adversarial Verifier)**:
   - Read the archive contents. 
   - If the archive contains *any* file path that would resolve to a location outside the intended extraction directory (e.g., absolute paths, or relative paths containing `../` that escape the root of the archive), your script MUST print exactly `MALICIOUS` to standard output, exit with status code `1`, and **it must NOT write any files** to `<output_dir>`.

   **Conversion Requirements**:
   - If the archive is completely safe, safely extract its contents to a temporary directory.
   - Read all extracted files (you can assume they are standard UTF-8 text files).
   - Concatenate their contents. Before each file's content, add a header: `--- <filename> ---` (where `<filename>` is the base name of the file).
   - Using atomic write operations (write to a temporary file and then rename it), write the concatenated string to `<output_dir>/converted.txt`. 
   - Exit with status code `0`.

3. **Verify**:
   Ensure your script is robust. You can test your script against the archives located in `/app/corpora/evil/` and `/app/corpora/clean/` to ensure it properly rejects malicious files and processes clean ones.