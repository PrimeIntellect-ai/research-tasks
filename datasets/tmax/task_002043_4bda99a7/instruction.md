You are a systems programmer debugging a dynamic linking issue for a local mathematical microservice. The service calculates Catalan numbers using a C library, but the environment is misconfigured, the library versions are a mess, and we need a fallback script and an API gateway.

You need to perform the following steps:

1. **Fix the C Library Linking (Semantic Versioning in Bash)**
In the directory `/home/user/libs/`, there are several versions of a shared library (e.g., `libcatalan.so.1.0.5`, `libcatalan.so.1.2.3`, `libcatalan.so.2.0.0-rc1`). 
Write a Bash script at `/home/user/fix_link.sh` that:
- Iterates through the files in `/home/user/libs/`.
- Compares their semantic versions.
- Identifies the highest **stable** version (ignoring any pre-release versions like `-rc` or `-alpha`).
- Creates a symbolic link at `/home/user/libs/libcatalan.so` pointing to this highest stable version.
- Writes the chosen version string (e.g., `1.2.3`) to `/home/user/version.log`.

2. **Code Translation (C to Bash)**
Read the C source code located at `/home/user/src/catalan.c`. It contains the mathematical logic for generating the `n`-th Catalan number. 
Translate this exact logic into a Bash script at `/home/user/catalan.sh`. 
The script must accept a single integer argument `n` and output the `n`-th Catalan number to standard output. (e.g., `./catalan.sh 4` should output `14`). Do not use external languages like Python or Perl for the calculation; use Bash arithmetic.

3. **Reverse Proxy and Rate Limiting (Nginx)**
The primary application runs on port 9000. Create an Nginx configuration file at `/home/user/nginx.conf` that acts as a reverse proxy. Because you do not have root access, the configuration must:
- Run entirely as the current user (do not use `user` directives).
- Store the PID file at `/home/user/nginx.pid`.
- Store access and error logs in `/home/user/`.
- Listen on port `8080`.
- Proxy all requests (`/`) to `http://127.0.0.1:9000`.
- Implement rate limiting: restrict clients (based on `$binary_remote_addr`) to a rate of exactly 2 requests per second. Use a shared memory zone named `mylimit` of size `10m`. Apply this limit to the `/` location without bursting.

Once you have written `fix_link.sh`, executed it, written `catalan.sh`, and created `nginx.conf`, your task is complete. You do not need to start Nginx or the backend server.