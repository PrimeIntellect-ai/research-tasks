We are managing a legacy configuration tracking system. The system packages directory snapshots into a proprietary "CFGArchive" format. We have a compiled validation utility for this format located at `/app/cfg_verify`, but the utility is poorly written: it is vulnerable to path traversal attacks, symlink exploits, and nested archive "zip bombs." 

Your task is to write a secure, robust filter program in C to replace the unsafe validation logic. 

**Requirements:**
1. **Reverse Engineer the Format:** Examine the stripped binary `/app/cfg_verify` to understand the proprietary "CFGArchive" file structure. (Hint: It expects a specific magic header sequence at the very beginning of the file, immediately followed by a standard `tar.gz` stream).
2. **Develop the Filter (`/home/user/cfg_filter.c`):**
   Write a C program that accepts a single file path as a command-line argument: `./cfg_filter <path_to_archive>`.
   The program must:
   - Validate the proprietary magic header.
   - Use `libarchive` (you may install `libarchive-dev` and build with `-larchive`) to stream and parse the embedded `.tar.gz` payload.
   - **Safely traverse** the archive's contents in-memory or using secure, atomically created temporary directories.
   - Inspect any nested `.tar.gz` or `.zip` archives found inside the main archive.
3. **Security Constraints (The Filter Logic):**
   Your program must flag an archive as **EVIL** (exit code `1`) if it violates ANY of the following rules, and **CLEAN** (exit code `0`) if it passes all rules:
   - Contains any file or directory path with `../` or starting with `/`.
   - Contains any symbolic link pointing to an absolute path or containing `../`.
   - Contains archives nested more than 2 levels deep (i.e., a CFGArchive containing a tarball, which contains another tarball, which contains a third tarball is EVIL).
   - Fails the magic header check or contains corrupted archive headers.

Compile your solution to `/home/user/cfg_filter`. Test your binary against the sample archives in `/app/corpora/clean/` and `/app/corpora/evil/` to ensure your logic strictly separates safe configurations from malicious ones.