You are a security engineer tasked with rotating credentials and sanitizing authorized key files after a potential compromise. 

We have identified a list of compromised SSH public keys. You need to write a Go program (`/home/user/rotator.go`) that performs an automated security sweep and key rotation. 

Your Go program must perform the following actions:
1. **Intrusion Detection & Vulnerability Sweeping:**
   Read the file `/home/user/compromised.list`. This file contains one compromised SSH public key per line.
   Scan all `authorized_keys` files located in the user directories under `/home/user/app_users/` (e.g., `/home/user/app_users/alice/authorized_keys`, `/home/user/app_users/bob/authorized_keys`, etc.).
   Remove any line from these `authorized_keys` files that exactly matches any of the keys in `compromised.list`. Keep a running total of how many compromised key entries were removed across all files.

2. **SSH Key Generation & Hardening:**
   Generate a new Ed25519 SSH keypair for the `admin` user. You may use Go's `os/exec` to call `ssh-keygen -t ed25519 -N "" -f /home/user/app_users/admin/id_ed25519` or implement it natively in Go.
   Ensure strict file permission access control:
   - The private key (`/home/user/app_users/admin/id_ed25519`) must have exactly `0600` permissions.
   - The public key (`/home/user/app_users/admin/id_ed25519.pub`) must have exactly `0644` permissions.
   Append the newly generated public key (the contents of `id_ed25519.pub`) to the `/home/user/app_users/admin/authorized_keys` file on a new line.

3. **Reporting:**
   Create a report file at `/home/user/rotation_report.txt` with exactly the following format:
   ```
   Removed compromised keys: <X>
   Admin key generated: true
   ```
   Replace `<X>` with the total integer count of compromised key lines removed.

Once you have written the Go program, run it so that the sanitization and rotation are completed.