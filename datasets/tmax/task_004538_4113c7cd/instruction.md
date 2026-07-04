You are an integration developer testing a new API gateway setup. We are migrating our API request generation and filtering stack. Your task consists of three main parts:

1. **Extract Filter Logic from Audio:**
   We intercepted a voicemail from our security team detailing a specific API attack pattern that our legacy system missed. The audio file is located at `/app/briefing.wav`. You must transcribe or listen to this audio file to determine the exact criteria for "evil" API requests.

2. **Develop a Python Sanitizer:**
   Using the criteria extracted from the audio, write a Python script at `/home/user/sanitizer.py`.
   - The script must accept a single command-line argument: the path to a JSON file representing an API request.
   - The JSON format looks like this: `{"method": "POST", "path": "/api/data", "headers": {"User-Agent": "Mozilla"}, "body": {"username": "test"}}`.
   - If the request matches the evil criteria from the audio, the script MUST exit with status code `1` and print `EVIL`.
   - If the request is safe, the script MUST exit with status code `0` and print `CLEAN`.
   You can test your script against the provided datasets in `/app/corpora/evil/` and `/app/corpora/clean/`.

3. **Code Translation (Go to Python):**
   Our legacy testing tool, written in Go, is located at `/app/requester.go`. It uses goroutines and channels to read JSON files from a directory and simulate concurrent API requests.
   - Translate this Go script into a Python script at `/home/user/requester.py`.
   - You must use Python's `asyncio` to replicate the concurrency pattern (processing files concurrently rather than sequentially).
   - It should accept a directory path as a command-line argument and print the paths of processed files.

4. **Reverse Proxy Configuration (Optional context):**
   Assume your `sanitizer.py` will later be plugged into an Nginx reverse proxy using an `auth_request` module or embedded Python. For now, we only need the standalone `sanitizer.py` classifier to pass the automated suite.

Ensure your `sanitizer.py` is perfectly accurate against the clean and evil corpora.