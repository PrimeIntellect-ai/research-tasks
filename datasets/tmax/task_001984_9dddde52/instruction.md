You are a mobile build engineer maintaining the CI/CD pipelines for our mobile web application. Recently, we've had incidents where debug views, stack traces, and developer secrets were accidentally exposed in the UI during release builds. To prevent this, we are adding an automated security check to our End-to-End (E2E) testing pipeline.

Your task is to orchestrate a build check that uses OCR to read text from E2E screenshots, and passes that text through a security filter you will write.

Here are your requirements:

1. **Write the Security Filter (`/home/user/security_filter.py`)**
   Create a Python CLI script that takes a file path as an argument, reads its contents, and analyzes the text.
   It must exit with code `0` (Safe) if the text is clean, and exit with code `1` (Evil) if the text contains any of the following leaked information:
   - AWS Access Keys (the string `AKIA` followed by exactly 16 uppercase alphanumeric characters).
   - Stack traces (the exact case-sensitive words `Traceback` or `Exception`).
   - Any HTML/XML tags (e.g., `<script>`, `<img>`, `<div class="x">`).
   - Internal IP addresses in the `10.x.x.x` or `192.168.x.x` ranges.
   
   To help you test, we have provided sample files in `/app/corpus/clean/` and `/app/corpus/evil/`. Your script must accept all clean files and reject all evil files.

2. **Property-Based Testing (`/home/user/test_filter.py`)**
   Write a Python test script using the `hypothesis` library. It should generate random alphanumeric strings (which by definition won't contain the evil patterns above) and assert that your `security_filter.py` logic evaluates them as safe. 

3. **OCR and Build Orchestration (`/home/user/Makefile`)**
   We have a test screenshot from our E2E suite located at `/app/screenshot.png`.
   Create a `Makefile` with a target called `check`. When we run `make check`, it must:
   - Use `tesseract` to extract the text from `/app/screenshot.png` and save it to `screenshot_text.txt`.
   - Run `python3 security_filter.py screenshot_text.txt`.
   - If the filter detects a leak (exit code 1), the `make check` command should fail (which fails the CI build). 

*Constraints & Notes:*
- `tesseract-ocr` and `libtesseract-dev` are pre-installed. You can install Python dependencies like `pytesseract` and `hypothesis` via pip.
- Do not modify the original `/app/screenshot.png` or the `/app/corpus/` directories.