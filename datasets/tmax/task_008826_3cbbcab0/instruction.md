You are a security engineer tasked with rotating credentials and fixing a legacy C tool that leaks secrets.

We have a legacy tool located at `/home/user/src/rotate.c`. Currently, this program takes a secret key as a command-line argument (`argv[1]`), which is a major security vulnerability because the secret is visible to other users via `/proc/[pid]/cmdline` and `ps`.

Your task is to fix this by modifying the C program to read the secret from a heavily restricted file instead, and then execute the rotation.

Perform the following steps:
1. Create a file named `/home/user/secret.key` containing exactly the string: `super_secret_rotation_key_99` (no newline required, but acceptable).
2. Set the permissions of `/home/user/secret.key` to strictly `0600` (read and write only for the owner).
3. Modify `/home/user/src/rotate.c` to:
   - Accept no command line arguments for the secret.
   - Use the `stat` system call to check the permissions of `/home/user/secret.key`. 
   - If the file permissions are NOT exactly `0600` (i.e., `S_IRUSR | S_IWUSR`), print "Insecure file" to standard error and exit with status code 1.
   - If the permissions are correct, open the file, read the secret (up to 50 characters).
   - Write the exact string "Credential rotated securely\n" to `/home/user/rotate.log`.
4. Create the directory `/home/user/bin` if it doesn't exist.
5. Compile the updated program using `gcc /home/user/src/rotate.c -o /home/user/bin/rotate`.
6. Execute `/home/user/bin/rotate` to perform the rotation successfully. 

Ensure that `/home/user/rotate.log` is created and contains the success message, as this will be checked by the automated verification system.