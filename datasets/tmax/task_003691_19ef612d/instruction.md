You are a security researcher analyzing a new strain of obfuscated malware. We have recovered a partial analysis environment, but several pieces are broken.

Your goal is to build a reliable bash-based malware detector that identifies infected binaries while ignoring clean ones. 

Here are the components you have:
1. **The Ransom Note Image (`/app/ransom_note.png`)**: This image contains a screenshot of the malware author's terminal. It contains a specific 16-character hex signature (the "magic string") used to encrypt the payload. You need to extract this signature. `tesseract` is installed.
2. **The Extractor Source (`/app/extractor_src/`)**: A C project designed to parse ELF binaries and extract obfuscated query strings. However, it currently fails to compile due to linker and compiler errors. You must fix the source code and `Makefile` so it builds successfully into an executable at `/app/extractor_src/bin_extractor`.
3. **The Target Corpora**: We have a dataset of known clean binaries at `/app/corpora/clean/` and known malicious binaries at `/app/corpora/evil/`. 

Your tasks:
1. Extract the 16-character magic string from `/app/ransom_note.png`.
2. Debug and fix the compiler and linker errors in `/app/extractor_src/` to build the `bin_extractor` tool.
3. Write a classification script at `/home/user/classifier.sh`. This script must accept a single file path as an argument (`$1`). It should use your compiled `bin_extractor` and the extracted magic string to analyze the file. 
4. The script `/home/user/classifier.sh` must exit with code `1` if the file is malicious (matches the obfuscated pattern containing the magic string) and exit with code `0` if the file is clean. 

Ensure your script is robust and relies purely on standard bash utilities and the compiled `bin_extractor`.