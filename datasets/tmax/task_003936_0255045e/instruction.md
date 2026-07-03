You are a network security engineer investigating a custom packet processing pipeline. We have a Go-based service called `net-sniff-processor` that captures specific traffic and passes metadata and payloads to an external shell script for logging. 

However, we have identified a severe CWE (Information Exposure) vulnerability: the service passes sensitive data (like extracted API keys and authorization tokens) to the logging script via command-line arguments. This means the secrets are temporarily visible to any user on the system who inspects `/proc/[pid]/cmdline`.

Your task is to fix the pipeline by doing the following:

1. **Fix the Vendored Package**: The source code for `net-sniff-processor` is vendored at `/app/net-sniff-processor-v1.2.0`. However, the previous developer introduced a bug in the `Makefile` that prevents it from building. Identify the perturbation in the `Makefile` (which prevents the Go compiler from finding the local modules) and fix it so that running `make build` successfully produces the `net-sniff` binary in the package directory.

2. **Create a Secure Redactor in Go**: Instead of modifying the complex `net-sniff` codebase to change how it spawns processes, we will intercept its calls. You need to write a Go program at `/home/user/redactor.go` and compile it to `/home/user/redactor`.
   - The `redactor` binary will be called by `net-sniff` in place of the logging script. It will receive the arguments exactly as the old script did.
   - Your `redactor` must inspect all incoming command-line arguments. 
   - It must sanitize the arguments by redacting any sensitive data. Specifically, any string matching the pattern of our API keys (a string starting with `AKIA` followed by exactly 16 alphanumeric characters, or any string following `PASSWORD=` up to the next space or end of string) must be replaced with `[REDACTED]`.
   - It must then execute the actual target logging script (the path to which is defined in the `TARGET_SCRIPT` environment variable), but instead of passing the sanitized data as command-line arguments (which would still expose them in `/proc`), it must pass the sanitized data as a JSON array via standard input (stdin) to the target script.

To ensure your redactor works perfectly and does not drop innocent traffic or fail to redact secrets, we have provided two directories containing sample argument lists (one argument per line) at `/app/tests/corpus/`:
- `/app/tests/corpus/clean/`: Contains normal packet metadata. Your redactor must output these exactly as they are (JSON array of strings) without modifying them.
- `/app/tests/corpus/evil/`: Contains payloads with embedded credentials. Your redactor must successfully redact the sensitive parts before formatting them as JSON.

Build your Go binary at `/home/user/redactor`. Ensure it compiles without errors and strictly adheres to the redaction rules. Do not leave any background processes running when you are finished.