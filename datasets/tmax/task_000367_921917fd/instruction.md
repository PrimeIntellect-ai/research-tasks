I need your help fixing a local project. I have a Python project under `/home/user/log_sanitizer` that processes incoming traffic logs for a legacy API gateway. However, there's a problem: we recently started receiving malformed, adversarial log entries designed to crash our internal parser.

We are currently using a vendored library to parse the logs, located at `/app/vendored/py-fast-log-parser`. The issue is twofold:
1. The vendored library has a deliberate bug/perturbation in its Makefile and environment setup that prevents it from building its C-extension correctly. You'll need to figure out what's wrong with the package in `/app/vendored/py-fast-log-parser`, fix it, and build/install it locally so our Python code can use it.
2. Once the vendored parser is working, you need to write a Python script at `/home/user/log_sanitizer/sanitizer.py` that implements a specific filtering state machine.

Your `sanitizer.py` script must expose a CLI function or accept a directory of log files to process. Specifically, it should take two arguments: an input directory and an output directory.
Usage: `python3 /home/user/log_sanitizer/sanitizer.py <input_dir> <output_dir>`

The sanitizer must read all `.log` files in the input directory. Each line in a `.log` file is a JSON string. The sanitizer must parse the JSON, examine the `url` and `parameters` fields, and determine if the entry is safe.
If it is safe, it must be written to the exact same filename in the output directory. If it is "evil", it must be completely discarded.

Safe vs Evil criteria:
- Evil logs contain path traversal attempts in the URL (e.g., `../`, `%2e%2e%2f`).
- Evil logs contain SQL injection patterns in any parameter value (look out for `' OR '1'='1`, `UNION SELECT`, `--`).
- Evil logs contain control characters (`\x00` through `\x1F`) in the URL routing or parameter parsing state.
- Safe logs are everything else.

To test your implementation, we have provided two directories:
- `/app/corpora/evil/` containing files with known bad logs.
- `/app/corpora/clean/` containing files with known good logs.

Your task is complete when:
1. The vendored package at `/app/vendored/py-fast-log-parser` is correctly fixed and installed.
2. The script `/home/user/log_sanitizer/sanitizer.py` successfully filters logs. If run against `/app/corpora/clean/`, it preserves 100% of the files identically in the output directory. If run against `/app/corpora/evil/`, it generates completely empty files in the output directory (meaning 100% of the evil entries are rejected).

Please provide the final `sanitizer.py` and ensure all setup steps are complete.