You are acting as an automated assistant for a technical writer who needs to organize a massive, messy documentation dump from multiple engineering teams. 

You have been provided with an archive of raw documentation at `/home/user/raw_docs.tar.gz`. The archive contains a directory tree with various Markdown (`.md`) files and their corresponding JSON metadata files (`*.meta.json`). 

You also have a C++ single-header JSON parsing library available at `/home/user/json.hpp` (nlohmann/json).

Your objective is to extract, filter, rename, and repackage these documents according to the following rules:

1. Extract the `raw_docs.tar.gz` archive into a new directory `/home/user/docs_workspace`.
2. Write a C++ program at `/home/user/organizer.cpp` (and compile it) that traverses the extracted directory tree.
3. For every `*.meta.json` file it finds, it must parse the JSON. The JSON structure looks like this:
   ```json
   {
       "target_file": "intro.md",
       "component": "networking",
       "version": "v2.0",
       "status": "approved"
   }
   ```
4. If the `status` is `"approved"`, your C++ program must rename the associated `target_file` (which resides in the same directory as the metadata file) to include its component and version as a prefix. The new filename must follow the format: `<component>_<version>_<target_file>`. 
   *(For example, `intro.md` becomes `networking_v2.0_intro.md`)*
5. If the `status` is anything else (e.g., `"draft"` or `"deprecated"`), do not rename the Markdown file and ensure it is not included in the final release.
6. After your C++ program has successfully renamed the approved files, use shell commands to find all the newly renamed Markdown files (files matching the `*_*_*.md` pattern) and compress them into a single, flat ZIP archive located at `/home/user/release_docs.zip`. The zip file should not contain any directory structure (use the appropriate zip flag to flatten/junk paths), just the `.md` files themselves.

**Requirements:**
- You MUST use C++ to parse the JSON and rename the files. 
- You may use bash/shell commands for archive extraction, compilation, and final zip creation.
- The final zip archive `/home/user/release_docs.zip` must contain exactly the approved and renamed `.md` files.