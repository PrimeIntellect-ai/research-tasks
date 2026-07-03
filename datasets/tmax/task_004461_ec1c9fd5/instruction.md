You are an infrastructure developer tasked with organizing and securely processing project log files. A previous developer left behind an architecture diagram in an image file, and a partial pipeline. Your job is to build a robust C utility that processes incoming JSON log files, categorizes them, and safely writes them to an archive directory using atomic operations.

Step 1: Information Extraction
Extract the required archive file prefix from the diagram located at `/app/diagram.png`. You can use Tesseract OCR to read the text from this image. Look for a string in the format `PREFIX: <string>`.

Step 2: Implement the Log Organizer in C
Write a C program at `/home/user/organizer.c` and compile it to `/home/user/organizer`. 
The program must take exactly two arguments:
`./organizer <input_dir> <output_dir>`

For every `.json` file in `<input_dir>`, the program must:
1. Parse the JSON file. Each file contains exactly one JSON object with two string fields: `"filename"` and `"content"`. (e.g., `{"filename": "module1.log", "content": "Build successful."}`)
2. Validate the `"filename"` field to prevent path traversal attacks. You MUST reject any `"filename"` that contains forward slashes (`/`), backslashes (`\`), or directory traversal sequences (`..`).
3. If the JSON is invalid or the `"filename"` is malicious, the program must reject the file (skip it and print a warning to stderr, or exit with a non-zero status).
4. If valid, the program must write the `"content"` to a new file in `<output_dir>`. The final filename must be `<PREFIX><filename>` (using the prefix you extracted from the image).
5. The write operation must be ATOMIC to prevent race conditions with other log readers. You must write the content to a temporary file inside `<output_dir>` first (e.g., using `mkstemp`), and then use `rename()` to move it to the final destination path.

Step 3: Verification Corpus
Your tool will be tested against an adversarial corpus of logs.
- Clean corpus: `/app/corpus/clean` contains well-formed JSON logs. Your program must successfully process 100% of these, resulting in the correct atomically written files in the output directory.
- Evil corpus: `/app/corpus/evil` contains malicious JSON logs attempting path traversal (e.g., writing to `/etc/` or overwriting critical files outside the output directory). Your program must reject 100% of these and safely process nothing.

Build your C program, ensure it runs correctly against both corpora using a test output directory, and leave the compiled executable at `/home/user/organizer`.