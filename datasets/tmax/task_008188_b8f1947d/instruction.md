You are an artifact manager responsible for curating a local binary repository. 

You have an incoming drop directory at `/home/user/incoming` containing several files. Some of these are compiled ELF binaries, some are purely data files, and each binary has an associated metadata file (with a `.meta` extension) containing build logs and configurations.

Your task is to analyze, transform, and organize these artifacts into a structured repository at `/home/user/repo`.

Perform the following steps:
1. Identify all valid ELF binary files in `/home/user/incoming`. Ignore any files that are not valid ELFs (even if they have a `.elf` extension).
2. For each valid ELF binary, extract its machine architecture using standard tools (e.g., `readelf`). Map the extracted architecture string to a standardized lowercase folder name (e.g., "Advanced Micro Devices X86-64" should become `x86_64`, "AArch64" should become `aarch64`, "Intel 80386" should become `i386`).
3. For each valid ELF binary, read its corresponding `.meta` file (which shares the same base name, e.g., `app1.elf` -> `app1.meta`). The metadata file contains various build logs. Use text transformation tools to extract the version number, which is uniquely identified on a line starting exactly with `BUILD_VERSION=` (e.g., `BUILD_VERSION=2.4.1`).
4. Move and rename the valid ELF binaries to the new repository directory following this structure: `/home/user/repo/<architecture>/<original_basename>_v<version>.elf`. 
5. Create a tab-separated registry file at `/home/user/repo/registry.tsv`. The file must contain a header row: `OriginalName\tNewPath\tArchitecture\tVersion`. 
6. Add an entry for each valid ELF file you processed, sorted alphabetically by the `OriginalName`. The `NewPath` should be the absolute path to the file's new location.

Write a script in the language of your choice (Python, Bash, Ruby, etc.) to automate this process, execute it, and ensure the final state exactly matches these specifications.