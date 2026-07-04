You are an AI assistant helping a system administrator maintain our web hosting servers. 

We have a legacy compiled utility located at `/app/legacy_web_scanner` that we use to scan user home directories to generate a mapping of active web directories and TLS certificate symlinks. Unfortunately, the source code was lost, and the binary is stripped. We need to rewrite this utility in Rust.

Your task is to reverse-engineer the behavior of `/app/legacy_web_scanner` and write a functionally identical Rust program. 

The utility takes exactly one argument: a base directory path. 
It scans this directory and outputs a specific formatted string to stdout based on the directory structure, symlinks, and ownership settings.

Please write a Rust program, compile it, and place the executable at `/home/user/new_web_scanner`.

The new program must perfectly match the output of the legacy binary for any valid directory structure it is run against. The system will test your binary by passing various newly generated directory paths to both the legacy binary and your new Rust binary and asserting that their standard outputs match exactly.

You may use standard tools like `strings`, `strace`, `objdump`, or write test scripts to understand the legacy binary's behavior. The base directory contains subdirectories simulating user accounts, some of which contain `public_html` directories, and `tls/cert.pem` symlinks.