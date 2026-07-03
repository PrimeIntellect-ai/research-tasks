You are a deployment engineer tasked with rolling out a new release for a web application. The application files need to be deployed from a staging directory to the production directory, and strict file permissions and Access Control Lists (ACLs) must be applied based on a deployment manifest. 

Your task is to write a Bash script at `/home/user/deploy_update.sh` that automates this process, and then run it to perform the deployment.

Here are the requirements:

1. **Directories**: 
   - Source directory: `/home/user/release_v2` (already contains the updated files)
   - Target directory: `/home/user/production` (where files must be deployed)
   - Manifest file: `/home/user/manifest.txt`

2. **Manifest Format**:
   The manifest file uses a pipe-separated format:
   `relative_filepath | base_octal_permissions | acl_user | acl_permissions`
   Example: `api/server.py | 640 | www-data | r-x`

3. **Script Operations (`/home/user/deploy_update.sh`)**:
   - The script must accept the manifest file as its first argument.
   - For every line in the manifest (ignoring empty lines):
     - Copy the file from the source directory to the target directory (create target subdirectories if they don't exist).
     - Apply the `base_octal_permissions` using `chmod` to the target file.
     - Apply the ACL using `setfacl` granting `acl_user` the `acl_permissions` on the target file.
   - After processing all files, the script must use `awk` and `getfacl` to generate an audit log at `/home/user/audit.log`.

4. **Audit Log Format (`/home/user/audit.log`)**:
   The log must contain exactly one line per deployed file, sorted alphabetically by file path, in the following format:
   `FILE: <relative_filepath> - PERMS: <octal_perms> - ACL: <acl_user>:<acl_permissions>`
   *(Note: extract the actual applied permissions directly from the deployed files to ensure accuracy, do not just copy the manifest).*

Run your script to complete the deployment and generate the `/home/user/audit.log` file.