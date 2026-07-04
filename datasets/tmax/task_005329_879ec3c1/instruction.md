You are a penetration tester auditing an automated SSH key provisioning system. The system ingests logs of user requests. Recently, attackers have been embedding XSS and SQL Injection payloads into the SSH key and username fields of these logs.

Your task consists of three phases:

1. **Fix the Regex Dependency**: 
   The system relies on a vendored version of the Google `re2` regex library, located at `/app/re2-src/`. The build configuration was accidentally broken during a recent migration. Fix the build system (it is currently failing to compile due to a deliberately introduced perturbation in the C++ standard flags) and compile the library to produce the static archive (`libre2.a`).

2. **Reverse Engineer Legacy Signatures**:
   We lost the source code for our old legacy filter, but the binary is available at `/app/legacy_filter`. Use standard disassembly or string extraction tools to analyze this binary. You will find two specific regular expressions hardcoded inside it: one for detecting SQL injection and one for detecting XSS. Extract these exact regex strings.

3. **Build the Classifier**:
   Write a C++ program at `/home/user/log_classifier.cpp` and compile it to `/home/user/log_classifier`. 
   - It must link against the compiled `re2` library from Phase 1.
   - It should take exactly one command-line argument: the path to a log file.
   - It must read the contents of the file.
   - If the contents match EITHER of the two regexes extracted from the legacy binary, it must print exactly `REJECT` to standard output and exit with code 1.
   - If the contents do NOT match either regex, it must print exactly `ACCEPT` to standard output and exit with code 0.
   
Ensure your `log_classifier` is perfectly accurate. It will be tested against a hidden corpus of clean and malicious files. 

When you have successfully compiled `/home/user/log_classifier`, write a log file to `/home/user/task_complete.log` containing the string "CLASSIFIER READY".