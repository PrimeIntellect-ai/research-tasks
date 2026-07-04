You are a QA Engineer tasked with setting up a Web Application Firewall (WAF) test environment. We have a hybrid C/Go project that acts as a request sanitizer, but the build is currently broken and the version-checking logic is missing.

Your objective is to fix the project, implement the missing logic based on an image artifact, and verify it against our test corpora.

Here are the steps you must complete:

1. **Extract Rules from Image**: 
   There is an image at `/app/version_rules.png`. Use OCR (e.g., `tesseract`) to read the semantic versioning rules from it. It contains specific instructions on which client versions should be blocked.

2. **Fix the C Scanner Library**:
   In `/app/c_scanner/`, there is a legacy C library used for payload inspection. 
   - The `Makefile` is broken (missing libraries or incorrect flags) and fails to compile.
   - Fix the `Makefile` and compile it to produce a shared object `libscanner.so`.
   - Ensure the library can be linked by Go (you may need to set `LD_LIBRARY_PATH` or copy it to an appropriate location accessible by the Go build).

3. **Resolve Go Circular Import**:
   The Go project in `/app/go_waf/` uses `cgo` to bind to `libscanner.so`. However, running `go build` fails due to a circular import between `go_waf/internal/config` and `go_waf/internal/scanner`. 
   - Refactor the code to break this import cycle.
   - Do not remove existing configuration properties; just move them or use interfaces to resolve the cycle.

4. **Implement Semantic Versioning Logic**:
   In `/app/go_waf/internal/versions/version.go`, implement the `IsAllowed(version string) bool` function. 
   - Parse the incoming semantic version.
   - Apply the rules you extracted from `/app/version_rules.png`. Return `false` if the version should be blocked, and `true` if it is allowed.

5. **Build and Classify Corpora**:
   Build the Go WAF CLI tool into an executable named `/app/go_waf/waf-tester`.
   The tool takes a directory of JSON HTTP requests and outputs a classification file.
   Command usage: `/app/go_waf/waf-tester -dir <target_directory> -out <output_file.json>`
   
   We have provided two test corpora:
   - `/app/corpora/clean/` (Valid requests with safe payloads and acceptable versions)
   - `/app/corpora/evil/` (Requests with malicious payloads caught by the C scanner OR banned versions caught by your Go logic)

   Run your tool on both directories:
   `/app/go_waf/waf-tester -dir /app/corpora/clean/ -out /app/clean_results.json`
   `/app/go_waf/waf-tester -dir /app/corpora/evil/ -out /app/evil_results.json`

The generated JSON files must be a simple map of filename to classification:
```json
{
  "request1.json": "CLEAN",
  "request2.json": "EVIL"
}
```
All files in the `clean` corpus must be classified as `CLEAN`, and all files in the `evil` corpus must be classified as `EVIL`.