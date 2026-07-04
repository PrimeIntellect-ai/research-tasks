You are a web developer tasked with building a new input sanitization feature for our Web Application Firewall (WAF). We recently experienced a security incident, and the details of the attack vector were left in a voicemail by our lead security engineer.

Your task has three phases:

1. **Incident Analysis (Audio)**: 
   Listen to or transcribe the audio file located at `/app/voicemail.wav`. It contains the specific zero-day attack keyword that attackers are using. You will need to extract this keyword to include in your blocklist. You can use standard command-line tools to transcribe or analyze it.

2. **Polyglot Build & Integration**:
   We have a highly optimized text normalization library written in C located at `/app/libnormalize/normalize.c`. It exposes a function `void normalize_text(char* input)` that modifies the string in-place to strip zero-width spaces and normalize homoglyphs.
   Create a new Rust executable project at `/home/user/waf_filter`.
   You must use a `build.rs` script to compile the C code and statically link it to your Rust project. 

3. **Filter Implementation & Constraint Satisfaction**:
   Write a Rust CLI tool that takes a single command-line argument (a path to a text file).
   The tool must:
   - Read the contents of the file.
   - Use FFI to pass the contents to the C `normalize_text` function.
   - Check if the normalized text contains either:
     a) Standard SQL injection patterns (specifically the exact string `OR 1=1`)
     b) The secret attack keyword you extracted from the voicemail.
   - If the file is malicious (contains either of the above), your program MUST exit with status code `1` (reject).
   - If the file is benign, your program MUST exit with status code `0` (accept).

You have been provided with training data in `/app/corpus/clean/` and `/app/corpus/evil/`. Every file in the clean directory should exit `0`, and every file in the evil directory should exit `1`.

Your final compiled binary must be located at `/home/user/waf_filter/target/release/waf_filter`.