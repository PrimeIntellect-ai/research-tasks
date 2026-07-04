You are a security researcher analyzing a suspicious system. We have detected a rogue background process running on this machine called `suspicious_daemon`. 

Your investigation involves three phases:

**Phase 1: Deleted File Recovery**
The `suspicious_daemon` process reads a secret key from `/home/user/bin/secret_key.txt` upon startup and immediately deletes the file to hide its tracks. However, the process is still running and holding the file handle open.
- Find the running process.
- Recover the contents of the deleted `secret_key.txt` from memory/file descriptors.
- Save the exact recovered contents to `/home/user/recovered_key.txt`.

**Phase 2: Vulnerability Analysis**
We have secured a copy of the daemon's source code at `/home/user/daemon_src`. It is a Rust project.
Recent versions of this daemon introduced a severe race condition in the `auth::authenticate` function. The function compares an input key against a master key, but due to improper use of `unsafe` global state, a concurrent attacker can bypass authentication by sending a wrong key at the exact same time a legitimate user sends the correct key.

Your job is to write a multi-threaded Rust test program that interacts with the `daemon_src` library to reliably trigger this race condition. The race condition occurs if `auth::authenticate` returns `true` when provided with an incorrect key, due to another thread simultaneously authenticating with the correct key. Use the key you recovered in Phase 1 as the correct key.

**Phase 3: Git Bisection**
The repository at `/home/user/daemon_src` has a linear commit history. The race condition was introduced in a specific commit, causing a regression from the previously secure implementation.
- Use `git bisect` combined with your Rust test script to automatically find the exact commit that introduced the race condition.
- Write the full 40-character SHA-1 hash of the first bad commit to `/home/user/bad_commit.txt`.

Requirements:
- Do not kill the `suspicious_daemon` process until you have recovered the key.
- Your output files (`recovered_key.txt` and `bad_commit.txt`) must contain only the requested data, with no extra whitespace or text.