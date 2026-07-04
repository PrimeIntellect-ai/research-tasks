You are tasked with building a secure configuration ingestion filter for our internal systems. Users upload configuration packages as standard `.tar` archives, but we have recently detected malicious payloads attempting path traversal attacks (Zip Slip) to overwrite system files outside the intended directories. Additionally, some packages belong to the wrong department.

Your goal is to create a robust Bash script at `/home/user/validate_config.sh` that validates an incoming configuration tarball. The script must take exactly one argument: the absolute path to the `.tar` file. It must exit with status `0` if the archive is perfectly safe and valid, and exit with status `1` if it is malicious or invalid.

**Requirements:**
1. **Department Verification (Image Fixture):** We have a scanned policy document located at `/app/policy.png`. You must use OCR (`tesseract` is installed) to extract the authorized department code from this image. The image contains a string in the format `DEPARTMENT_CODE: <CODE>`. 
2. **Safe Archive Inspection:** Your script must inspect the tarball's file list without unsafely extracting it to disk (or extract it safely to a temporary directory). 
3. **Zip Slip Prevention:** The script MUST reject the archive (exit `1`) if ANY file path inside the archive:
   - Is an absolute path (starts with `/`).
   - Contains parent directory traversal sequences (e.g., `../`, `..`, or similar standard traversal methods).
4. **Configuration Validation:** If the paths are safe, the script must parse the file named `settings.conf` located at the root level of the archive. This file will contain key-value pairs. The script must verify that the `DEPT` key exactly matches the `<CODE>` recovered from the image. If it does not match, or if `settings.conf` is missing, reject the archive (exit `1`).
5. **Acceptance:** If the archive contains no malicious paths and has the correct department code, accept it (exit `0`).

**Testing & Verification:**
To help you develop and test your script, we have provided two corpora of `.tar` files:
- `/app/corpora/clean/`: Contains perfectly valid archives. Your script MUST exit `0` for all files in this directory.
- `/app/corpora/evil/`: Contains archives that are malicious (Zip Slip attempts) or invalid (wrong department code, missing config). Your script MUST exit `1` for all files in this directory.

The automated test will evaluate `/home/user/validate_config.sh` against these corpora. You must achieve a 100% pass rate on both the clean and evil datasets. 

Do not modify the contents of the corpora or the image file. Ensure your script is executable (`chmod +x`).