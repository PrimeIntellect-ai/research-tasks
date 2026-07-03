You are an artifact manager responsible for curating binary repositories. We have a set of incoming software artifacts and a build log. You need to write a Rust program that processes these files, organizes them by architecture and version, and prepares a finalized repository archive.

Here is the step-by-step requirement for your task:

1. **Archive Extraction**: Extract the archive `/home/user/incoming/artifacts.tar.gz` into the directory `/home/user/incoming/extracted/`.
2. **Log Parsing**: Parse the multi-line log file at `/home/user/incoming/build.log`. The log contains build records in the following format:
   ```
   --- BUILD RECORD ---
   Artifact: <binary_name>
   Target: <environment>
   Version: <version_string>
   Status: <SUCCESS|FAILED>
   --------------------
   ```
   You only care about records where `Status: SUCCESS`.
3. **ELF Parsing**: For each successfully built binary found in `/home/user/incoming/extracted/`, determine its architecture. You may use external tools like `readelf` or parse the ELF header directly in your Rust program. We expect the architecture string to be normalized to either `x86_64` or `aarch64`.
4. **Atomic Writes & Organization**: For each valid binary, securely copy it to `/home/user/repo/<arch>/<binary_name>-<version>.elf`. To ensure no partial writes occur in our live repository, you MUST write the file to a temporary file in the target directory first (e.g., `<binary_name>-<version>.tmp`), and then atomically rename it to the final `.elf` filename.
5. **Link Management**:
   - Create a central directory `/home/user/repo/all_binaries/`. For every binary placed in the architecture folders, create a **hard link** to it inside `all_binaries/` with the same filename (`<binary_name>-<version>.elf`).
   - For each unique binary name within an architecture, create a **symbolic link** at `/home/user/repo/<arch>/<binary_name>-latest.elf` that points to the highest version of that binary (using standard semantic versioning comparison).
6. **Final Archive**: Once the `/home/user/repo/` directory is fully constructed, create a compressed archive of it at `/home/user/repo_curated.tar.gz` containing the `repo` directory at its root.

Write your Rust program at `/home/user/curator/src/main.rs`. You can initialize a new cargo project there. Run the program to perform the curation.

**Initial Setup:**
- `/home/user/incoming/artifacts.tar.gz` contains several ELF binaries without extensions.
- `/home/user/incoming/build.log` contains the build details.

Ensure the final tarball `/home/user/repo_curated.tar.gz` preserves the symlinks and hard links perfectly.