I have a messy Python project in `/home/user/workspace` that I need help organizing, fixing, and testing. It is supposed to be a simple REST API that verifies file checksums against a set of constraints, but I moved some files around and now the imports are broken. Furthermore, the core hashing logic and the end-to-end tests are missing.

Here is what you need to do:

1. **Fix the Application**: 
   The main API file is located at `/home/user/workspace/api/app.py`. It uses Flask. I recently moved the hashing utility to `/home/user/workspace/api/utils/hashing.py`, which caused import errors in `app.py`. Fix the import structure so the Flask app can start correctly.

2. **Implement the Checksum API**:
   The `/verify_files` POST endpoint in `app.py` relies on `verify_checksums` from `hashing.py`. You need to implement `verify_checksums`.
   - The endpoint will receive a JSON payload like this:
     `{"constraints": [{"filename": "file1.txt", "expected_sha256": "abc..."}, ...]}`
   - The function should read the target files from the `/home/user/workspace/data/` directory.
   - It must compute the actual SHA256 checksum of each file.
   - It should return a list of filenames that **DO NOT** match the expected checksum or do not exist.
   - The returned list of failed filenames must be **sorted alphabetically**.
   - The API endpoint should return a JSON response in the format: `{"failed_files": ["file1.txt", "file3.txt"]}`.

3. **Orchestrate an End-to-End Test**:
   Create a Python test script at `/home/user/workspace/test_e2e.py`.
   - This script must start the Flask app in the background on port 5000.
   - It must wait for the server to be ready.
   - It must send a POST request to `http://127.0.0.1:5000/verify_files` with the following exact payload:
     ```json
     {
       "constraints": [
         {"filename": "config.json", "expected_sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"},
         {"filename": "app.log", "expected_sha256": "c888c3c4017387b322f9af5c442740bc43a75a02421370bda43f9a76572e0a29"},
         {"filename": "missing.txt", "expected_sha256": "deadbeef"}
       ]
     }
     ```
   - The script must write the raw JSON response from the API to `/home/user/workspace/e2e_result.json`.
   - The script should then shut down the Flask server and exit cleanly.

You will need to install Flask and requests if they are not already installed (`pip install flask requests`).