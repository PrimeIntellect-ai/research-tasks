You are a security auditor analyzing a local authentication helper program. The current implementation passes sensitive HTTP cookies via command-line arguments, which is a critical security vulnerability because it leaks the token to any local user via `/proc/[pid]/cmdline`.

You have been provided with two files:
1. `/home/user/run_auth.sh` - A wrapper script used to launch the service.
2. `/home/user/auth_service.c` - The source code of the authentication service.

Your task is to fix this vulnerability:
1. **Identify the Leak:** Extract the leaked session token from the wrapper script (the value after `Cookie: session=`). Save *only* this token string (e.g., `abc123`) to `/home/user/leaked_token.txt`.
2. **Patch the Code:** Modify `/home/user/auth_service.c` to securely read the HTTP cookie from the environment variable `AUTH_COOKIE` instead of from `argv[1]`.
    - If the `AUTH_COOKIE` environment variable is not set, the program must print `Error: No cookie\n` to standard output and exit with status code `1`.
    - If the environment variable is set, it should perform the exact same validation as before (expecting the full string to match, e.g., `Cookie: session=<TOKEN>`). Do not use or read `argv[1]` anymore.
3. **Recompile:** Compile your modified C code using `gcc /home/user/auth_service.c -o /home/user/auth_service_fixed`.

Ensure the newly compiled binary `/home/user/auth_service_fixed` relies solely on the environment variable for authentication.