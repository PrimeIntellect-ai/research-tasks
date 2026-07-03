You are an expert script developer creating a new CI verification utility to prevent mathematically malformed and structurally broken packages from entering our codebase. We have been experiencing an issue where packages pass unit tests locally but fail in CI due to complex import ordering and corrupted payload metadata.

Your objective is to create a robust CI guard script at `/home/user/ci_guard.sh`. This script will be executed against various Python project directories to determine if they are safe to merge.

**Part 1: Configuration Extraction (Video Processing)**
Our centralized CI configuration is distributed as a telemetry video stream to prevent tampering. You have been provided with this video at `/app/ci_telemetry.mp4`.
- The video contains standard QR codes flashing at specific frames. 
- You must extract the frames, decode the QR codes (e.g., using `zbarimg` or similar tools you can install), and concatenate the decoded strings.
- The decoded string will yield a configuration payload in the format: `CRC_POLYNOMIAL=<hex_value>;TEST_MODE=<mode>`.
- Your `ci_guard.sh` must dynamically extract or use these decoded parameters.

**Part 2: Package & Dependency Verification (The CI Guard)**
Your script `/home/user/ci_guard.sh` must take exactly one argument: the path to a Python project directory.
It must analyze the directory and exit with code `0` if the project is clean, or exit with code `1` if the project is malformed ("evil").

A project is considered "evil" if it violates ANY of the following rules:
1. **Checksum Validation:** Every `.py` file in the project has a first line in the exact format `# CHECKSUM: <hex_crc32>`. The remaining contents of the file (from line 2 to the end) must hash to this exact CRC32 value. If any file has a mismatched checksum, the project is evil.
2. **Import Ordering & Unit Testing:** The project must not contain circular dependencies that cause an `ImportError` when the files are imported. Your script must create a temporary virtual environment, install the project's `requirements.txt` (if present), and programmatically attempt to import every `.py` module in the directory. If an import fails, the project is evil.

**Part 3: Adversarial Validation**
To ensure your utility works perfectly, we have provided an adversarial corpus containing dozens of mocked project directories.
- Clean corpus: `/app/corpus/clean/`
- Evil corpus: `/app/corpus/evil/`

Your script will be tested against every subdirectory in both corpora. It must exit `0` for 100% of the projects in the clean corpus, and exit `1` for 100% of the projects in the evil corpus.

Ensure your script is self-contained, handles missing dependencies by installing them locally if necessary, and strictly adheres to the exit code requirements.