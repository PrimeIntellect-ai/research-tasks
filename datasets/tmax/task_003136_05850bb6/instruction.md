You are a release manager preparing a new deployment pipeline. We are migrating a legacy deployment configuration parser to a pure Bash implementation to run on lightweight containers. 

You have been provided with an architecture diagram at `/app/schema.png` that contains the new deployment routing rules embedded as text. Use OCR (tesseract is available) to extract the routing sequence rule from this image. 

Your task is to write a Bash script at `/home/user/router.sh` that behaves exactly as the legacy system did, but adheres to the new routing sequence extracted from the image. 

The script must:
1. Accept exactly one argument: a comma-separated string of 5 alphanumeric configuration values (e.g., `alpha,beta,gamma,delta,epsilon`).
2. Read the extracted routing sequence rule from the image. The rule will dictate the exact order in which these 5 fields must be sorted, merged, and formatted.
3. Print the resulting formatted string to standard output. 
4. Exit with code 0 on success, or code 1 if the input does not contain exactly 5 comma-separated fields.

Additionally, you have access to the legacy system's obfuscated reference binary at `/app/legacy_router`. Note that `/app/legacy_router` uses the OLD sequence. Your Bash script must implement the same string processing logic but apply the NEW sequence found in the image.

Ensure your script is executable (`chmod +x /home/user/router.sh`). The CI pipeline will verify your script by fuzzing it with thousands of random inputs and comparing the output bit-for-bit against a hidden updated reference oracle.