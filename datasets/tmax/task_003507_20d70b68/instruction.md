You are assisting a technical writer with organizing and securely backing up their documentation. They have a repository of markdown files in `/home/user/docs`, but one of the past writers accidentally created a symlink (`/home/user/docs/shortcut`) that points back to `/home/user/docs`, creating an infinite loop if traversed blindly.

Your task is to securely archive this documentation.

1. **Extract Password**: There is an image file at `/app/password.png` containing the text of a secret backup password. Extract this text (you may use OCR tools like `tesseract` which is installed).
2. **Archive and Encrypt**: Create a bash command or script to archive the `/home/user/docs` directory into `/home/user/docs_backup.tar.gz.enc`.
   - You must use `tar` and `gzip` for the archive.
   - You must *not* follow or dereference symlinks (to avoid the infinite loop). Keep the symlink as a link in the archive.
   - You must encrypt the resulting tarball using `openssl enc -aes-256-cbc -pbkdf2 -pass pass:<EXTRACTED_PASSWORD>`.
3. **Integrity Verification**: Create a Bash script at `/home/user/verify.sh` that takes exactly one argument (the path to the `.enc` archive). The script should:
   - Decrypt the archive using the same password.
   - Use `tar` to list the contents of the unencrypted stream (verifying its integrity) without extracting it to disk.
   - Exit with code 0 if the archive is perfectly intact, or a non-zero code if it fails.

Our automated testing will run your `verify.sh` script and measure the exact byte-size of your final archive. If you accidentally follow the symlink loop, your archive will bloat past our strict numerical size threshold.