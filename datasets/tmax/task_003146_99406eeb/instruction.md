We are migrating a legacy Python 2 system to Python 3. As part of this migration, a critical performance bottleneck was identified in our semantic version sorting and diffing module, which heavily relies on old Python 2 `cmp` behaviors that were removed in Python 3. Instead of porting it to Python 3, we have decided to rewrite this module entirely in C++ for maximum performance.

Your task is to write this new C++ implementation.

You have been provided with two important artifacts:
1. An image file at `/app/legacy_rules.png`. This flowchart contains a specific, proprietary legacy rule regarding how pre-release tags are weighted and sorted in our system (which deviates slightly from standard SemVer 2.0). You will need to extract these rules (e.g., using Tesseract OCR, which is installed).
2. A reference binary at `/app/semver_oracle`. This is a compiled PyInstaller executable of the original Python 2 script. It represents the exact, ground-truth behavior we expect from your new C++ program.

**Requirements:**
1. Create a C++ project in `/home/user/vparser_cpp/`.
2. Your C++ program must read lines from `stdin`. Each line will contain a space-separated list of our custom semantic versions.
3. For each line, parse the versions using a custom state machine.
4. Sort the versions in descending order based on the rules recovered from `/app/legacy_rules.png` and standard major/minor/patch hierarchy.
5. After printing the sorted versions (space-separated) on one line, compute and print the "diff" between each adjacent sorted version pair on the next line. The diff format must exactly match the output format of `/app/semver_oracle`. 
6. Your final executable must be compiled to `/home/user/vparser_cpp/vparser`.

Since this is replacing a core component, your C++ program's `stdout` and `stderr` must be **bit-for-bit identical** to the `/app/semver_oracle` for any given sequence of versions. We will test your compiled binary against the oracle with a massive battery of randomized fuzz inputs.

You may use standard C++17 or C++20 features. Do not use external parsing libraries; build the state machine and sorting logic yourself.