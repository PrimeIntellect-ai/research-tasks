You are acting as a security engineer auditing a local network service. A secure file upload handler is running on localhost on a port between 8000 and 8010.

Your task has three parts:

1. **Service Auditing & Certificate Validation**: 
   Find the active service port in the 8000-8010 range. Connect to it and retrieve its SSL certificate. Verify the certificate against the Root CA provided at `/home/user/ca.pem`. Extract the Subject Common Name (CN) of the leaf certificate and write the exact CN string to `/home/user/cert_cn.txt`.

2. **CWE Identification**:
   The service uses a bash script located at `/home/user/upload_handler.sh` to process incoming uploads. Audit this script. Identify the primary security vulnerability related to how it handles file paths. Write the exact CWE identifier (in the format `CWE-XXX`) for this vulnerability to `/home/user/cwe.txt`.

3. **Code Auditing & Patching**:
   Patch the vulnerability in `/home/user/upload_handler.sh`. You must modify the script using Bash so that if the extracted `FILENAME` variable contains the substring `../` or exactly matches `..`, the script immediately prints `INVALID` to standard output and exits with a status code of `1`. Otherwise, the script should continue normally.

Ensure your modified `/home/user/upload_handler.sh` retains the original functionality for legitimate filenames. Do not change the existing variable names.