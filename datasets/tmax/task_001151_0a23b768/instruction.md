We are setting up a polyglot build system from scratch that handles both Python (`requirements.txt`) and Node.js (`package.json`) dependencies. We have a major issue with conflicting peer dependencies and malicious build scripts being injected into our repositories. 

Your task is to implement a Python-based build configuration validator and resolver.

1. **Extract Constraints:** There is an audio file located at `/app/build_constraints.wav`. You must transcribe this audio file using available terminal tools (e.g., `whisper` or by writing a quick API script if you have access to a transcriber, or using standard speech-to-text libraries). The audio contains spoken instructions detailing specific constraint rules for our build system (e.g., "The Python version must be strictly greater than 3.8", "The package 'lodash' must not be installed if 'underscore' is present", "Reject any build script containing the base64 encoded string 'eval'"). Write these rules down in `/home/user/extracted_rules.txt`.

2. **Implement the Validator:** Write a Python CLI tool at `/home/user/build_validator.py`. This tool must:
   - Accept a directory path as an argument.
   - Parse `package.json` and `requirements.txt` in that directory.
   - Apply the constraints extracted from the audio file.
   - Analyze a custom `.build.sh` script in the directory for malicious patterns defined in the audio instructions (using diff/patch parsing to check for sneaky modifications or checksum mismatches).
   - Exit with code `0` if the directory represents a safe, valid build configuration that satisfies all constraints.
   - Exit with code `1` if the directory violates constraints or contains malicious build steps.

3. **Adversarial Testing:** We have provided two directories containing various project configurations:
   - `/app/corpora/clean/`: Contains 50 subdirectories with valid, safe polyglot projects.
   - `/app/corpora/evil/`: Contains 50 subdirectories. Some have impossible dependency constraints, while others contain obfuscated malicious build scripts.
   
   Run your `build_validator.py` against all subdirectories in both corpora. Your tool must successfully exit with `0` for all projects in the `clean` corpus, and exit with `1` for all projects in the `evil` corpus.
   
Write your final test script to `/home/user/verify_all.sh` which iterates over both directories and prints exactly "CLEAN PASSED" if all clean projects return 0, and "EVIL REJECTED" if all evil projects return 1.