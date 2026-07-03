You are a developer tasked with organizing a messy directory of project dependencies. 

You have a directory located at `/home/user/packages_raw/` containing several metadata files. A previous backup system heavily obfuscated the filenames. Specifically, every filename in this directory is a standard Base64-encoded string. If you decode a filename, it follows this exact format:
`[package_name]_v[major].[minor].[patch].meta`
For example, decoding `bGliYWxwaGFfdjEuMTAuMC5tZXRh` yields `libalpha_v1.10.0.meta`.

You also have a requirements file at `/home/user/requirements.txt`. Each line specifies the minimum required version for a package in the format:
`[package_name] >= [major].[minor].[patch]`

Your task is to write a C program that organizes these files based on Semantic Versioning (SemVer) rules. 

Requirements for your C program:
1. It must be written in C and compiled to `/home/user/organizer`.
2. It should read the `/home/user/requirements.txt` file to parse the minimum required versions.
3. It must scan the `/home/user/packages_raw/` directory.
4. For each file, it must decode the Base64 filename to determine the package name and its version.
5. It must compare the parsed version against the requirement using strict semantic versioning rules (e.g., `1.10.0` is strictly greater than `1.2.0`).
6. If the package's version is greater than or equal to the required version, the program must copy the file into `/home/user/valid_packages/` using its **decoded** filename.
7. If the package's version is strictly less than the required version, the program must copy the file into `/home/user/outdated_packages/` using its **decoded** filename.
8. If a package is not listed in `requirements.txt`, ignore it.

Ensure you create the `/home/user/valid_packages/` and `/home/user/outdated_packages/` directories before running your program. Run your compiled C program and redirect its standard output to `/home/user/run.log`.

Do not use any external dependencies or libraries outside of the standard C library (libc). You must implement the Base64 decoding and Semantic Version parsing logic yourself within the C program.