You are an engineer tasked with setting up the validation layer for a new polyglot build system. Our organization relies heavily on custom build manifest files (using a custom syntax) that define dependencies between microservices. We have received several patches to these files that introduce circular dependencies or execute unauthorized shell commands.

You have been provided with an architecture diagram image located at `/app/system_architecture.png`. This image details the strict, allowable dependency graph between our microservice tiers (e.g., "Frontend -> API Gateway", "API Gateway -> Auth Service", "API Gateway -> DB Service").

Your task is to write a Python-based sanitizer and validator script named `/home/user/build_validator.py`.

Requirements:
1. Extract the allowed dependency constraints from `/app/system_architecture.png` (you can use the preinstalled `tesseract` OCR tool).
2. The custom build manifests use a custom format:
   ```
   Target: [Service Name]
   Depends-On: [Comma separated list of Services]
   Cmd: [Build command]
   ```
3. Your Python script must read a build manifest file (the path will be passed as the first CLI argument) and apply the following rules:
   - Ensure that the dependencies listed in `Depends-On` strictly satisfy the allowed architecture extracted from the image. Any violation should result in rejection.
   - Detect and reject any manifest where the `Cmd` contains dangerous shell constructs like reverse shells or unescaped interpolations (`$(...)` or `` `...` ``), acting as a state machine parser to catch obfuscated bash substitutions.
4. Your script must exit with code `0` if the manifest is entirely valid (clean), and exit with code `1` if it violates constraints or contains dangerous commands (evil).
5. Output `VALID` or `INVALID` on standard out.

Once your script `/home/user/build_validator.py` is ready, test it against the corpora located in `/app/corpora/`.