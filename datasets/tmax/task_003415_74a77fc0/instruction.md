You are an AI assistant helping a developer organize a massive, chaotic directory of project assets. The project dump contains thousands of files, many of which are duplicated, have incorrect file extensions, or are corrupted. We need to deduplicate, categorize by true binary format, rename them using a metadata service, and update our project's manifest file with the new paths. 

Because of the scale of the repository, you must process these files concurrently, using distributed locking to ensure race conditions don't corrupt the output. 

Here is the environment and what you need to do:

### 1. Multi-Service Infrastructure
There are two background services you must start and use:
1. **Redis Server**: Installed locally. Start it on the default port (6379).
2. **Metadata API**: A Flask application located at `/app/services/metadata_api.py`. Start it (it will bind to `127.0.0.1:5000`).

### 2. The Task Workflow
The raw files are located in `/home/user/project_dump/assets/` (which contains deep, nested subdirectories).
You must write a Python script (or combination of Bash and Python) to do the following concurrently (using at least 4 parallel workers):

1. **Recursive Traversal**: Find all files in `/home/user/project_dump/assets/`.
2. **Binary Header Extraction**: Ignore the file extension. Read the first few bytes (magic numbers) of each file to determine its true format. You only care about:
   - **PNG**: Starts with `\x89PNG\x0d\x0a\x1a\x0a`
   - **JPG**: Starts with `\xff\xd8\xff`
   - **PDF**: Starts with `%PDF-`
   - Ignore anything else.
3. **Hashing & Deduplication**: Calculate the SHA-256 hash of the file contents.
4. **Metadata Lookup**: Query the Metadata API: `GET http://127.0.0.1:5000/get_name?hash=<sha256>&ext=<true_extension_without_dot>`. It will return a JSON response: `{"filename": "canonical_name.ext"}`.
5. **Concurrent Move with Locking**: Multiple workers might process duplicates simultaneously. You must use a Redis lock (key: `lock:<sha256>`) to ensure only one worker copies the unique file to `/home/user/organized/<true_extension>/<canonical_name.ext>`. 
6. **Large-scale Text Editing**: Update the project manifest located at `/home/user/project_dump/manifest.txt`. The manifest has lines in the format `Asset: <old_relative_path>`. You must create a new file `/home/user/manifest_updated.txt` where the `<old_relative_path>` is replaced with the new absolute path `/home/user/organized/<ext>/<canonical_name.ext>`. If a file was skipped (unknown type), leave the line as-is.

### Verification
Once your script finishes executing, the correctness of your work will be evaluated by an automated scoring script (`/app/verify.py`). It calculates an `Organization_Accuracy_Score` based on correct categorization, successful deduplication without race conditions, and correctly rewritten text macros. 
You must achieve an `Organization_Accuracy_Score >= 0.95`.