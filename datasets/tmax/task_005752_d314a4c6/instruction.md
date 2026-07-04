You are an artifact manager responsible for curating our internal binary repositories. We are migrating our old artifact repository to a new, secure global standard, but hundreds of Python build scripts still point to the old legacy URLs.

Your task is to recursively search through the repository directory located at `/home/user/artifact_repo/` and update all Python (`.py`) files that reference the old repository. 

Here are the exact requirements:
1. Find every `.py` file inside `/home/user/artifact_repo/` (and its subdirectories) that contains the exact string `http://old-repo.local/v1/`.
2. For each matching file, replace `http://old-repo.local/v1/` with `https://secure-repo.global/v2/`.
3. In these same modified files, immediately after any line containing the assignment `artifact_url = "..."` (which you just updated), you must insert a new line containing exactly: `curated_by = "artifact_manager"`.
4. Files that do not have the `.py` extension must be completely ignored, even if they contain the old URL.
5. Python files that already use `https://secure-repo.global/v2/` must be completely ignored.
6. Record the absolute paths of all the Python files you modified into a log file at `/home/user/updated_artifacts.log`. The paths in this log file must be sorted alphabetically, with one absolute path per line.

Modify the files in-place. You may use shell tools (`sed`, `awk`, `find`, etc.) or write a Python script to accomplish this.