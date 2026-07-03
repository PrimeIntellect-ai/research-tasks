You are acting as a technical writer organizing a chaotic repository of engineering documentation and assets. You need to write a Bash script to automate the organization, metadata extraction, and packaging of a release candidate.

The source files are located in `/home/user/doc_staging/`. This directory contains a deeply nested, messy mix of Markdown documentation (`*.md`) and 3D printing GCode assets (`*.gcode`).

Write and execute a Bash script at `/home/user/organize_docs.sh` that performs the following tasks:

1. **Create the Release Structure**: Create a base directory `/home/user/release/` containing two subdirectories: `/home/user/release/docs/` and `/home/user/release/models/`.

2. **Process Documentation (.md files)**:
   - Recursively search `/home/user/doc_staging/` for all `.md` files.
   - Read each file to check for a frontmatter block. Look for a line exactly matching `status: final`. If the file has `status: draft`, ignore it completely.
   - For "final" documents, extract the title from the line starting with `title: ` (e.g., `title: Assembly Guide`).
   - Copy the file to `/home/user/release/docs/`.
   - Rename the copied file to `<sanitized_title>_<original_filename>`. To sanitize the title, replace all spaces with underscores and convert all letters to lowercase (e.g., `assembly_guide_readme.md`).

3. **Process 3D Models (.gcode files)**:
   - Recursively search `/home/user/doc_staging/` for all `.gcode` files.
   - Parse each file to find a specific slicer comment indicating the material used. Look for a line starting with `; MATERIAL: ` (e.g., `; MATERIAL: PETG`).
   - Copy the file to `/home/user/release/models/`.
   - Rename the copied file to `<material>_<original_filename>`. Convert the material string to lowercase (e.g., `petg_bracket.gcode`). If a GCode file lacks the `; MATERIAL: ` line, default the material prefix to `unknown`.

4. **Generate a Manifest**:
   - After all files are copied and renamed, generate a SHA-256 checksum manifest of all files in `/home/user/release/docs/` and `/home/user/release/models/`.
   - The manifest file must be saved to `/home/user/release/manifest.sha256`.
   - The format of each line in the manifest must be `<sha256sum>  <relative_path_from_release_dir>`, for example: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  docs/assembly_guide_readme.md`.
   - The manifest entries must be sorted alphabetically by the relative file path.

Ensure your script is executable and run it so the final state in `/home/user/release/` is generated.