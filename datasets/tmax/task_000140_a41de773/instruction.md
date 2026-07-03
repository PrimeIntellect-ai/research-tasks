You are acting as a backup administrator for a legacy Linux system. We have a proprietary backup archiving tool located at `/app/legacy_packer`. Unfortunately, we lost the source code for this tool years ago, and we are migrating to new environments where this compiled binary no longer reliably runs. 

Your task is to reverse-engineer the behavior of `/app/legacy_packer` and write a 100% bit-exact equivalent replacement script in pure Bash, located at `/home/user/packer.sh`. 

The legacy tool takes exactly one argument—a path to a directory—and writes a custom archived stream to standard output. 

Based on our previous analysis, the proprietary archiving format does the following:
1. It prints a header containing the total number of files.
2. It processes all regular files within the target directory (recursively), sorted alphabetically by their relative paths.
3. For each file, it prints a file header with its relative path and original size.
4. It reads the file's text contents, applies a text redaction and substitution pass (which you must deduce by running the binary on test inputs), compresses the resulting stream without file metadata, and encodes it into base64. 

You have `sudo` access if needed to install debugging tools like `hexdump`, `strings`, or `strace` to analyze the binary, though standard coreutils are already present. 

**Requirements:**
- Write your replacement script at `/home/user/packer.sh`. 
- The script must accept a target directory as its first argument (`$1`).
- The script must print the exact same standard output as `/app/legacy_packer "$1"` for any given directory containing text files. 
- You must use standard shell built-ins and coreutils (`find`, `sort`, `sed`, `tr`, `gzip`, `base64`, `stat`, etc.). Do not compile a new C binary.
- Ensure your output stream matches the legacy packer bit-for-bit. A verification suite will fuzz your script by generating hundreds of random directory trees containing text files, some containing sensitive keywords, and compare the standard output of your script against the legacy binary.

*Hint: Pay close attention to what happens to the word "CONFIDENTIAL" and standard alphabetic characters when passed through the packer. Also, ensure your compression avoids embedding timestamps.*