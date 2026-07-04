You are taking over a multi-file Rust project for a Web Security Dashboard that currently fails to compile. The previous developer left abruptly, but they left a voicemail file with some critical handover details.

Your objectives:
1. **Extract Audio Clues:** Transcribe the audio file located at `/app/voicemail.wav`. It contains the secret API token required for the service's authentication, as well as a hint about what is missing from the build configuration.
2. **Fix the Build System:** The Rust project located in `/app/vuln_dashboard/` fails to compile because of a missing static library linkage. Use the hint from the audio and fix `build.rs` so that it correctly links the static library `libsecutils.a` located in `/app/vuln_dashboard/lib/`. 
3. **Implement Data Processing:** The project is missing the core logic in `src/processor.rs`. You need to read and parse the structured JSON file at `/app/data/raw_vulns.json`. The logic must:
   - Merge duplicate vulnerability entries (based on their `cve_id`), combining their `affected_endpoints` into a single deduplicated list.
   - Sort the final list of vulnerabilities by severity descending (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`), and then alphabetically by `cve_id` for ties.
4. **Deploy the REST API:** Complete the REST API in `src/main.rs` (or create a wrapper service in any language if you prefer, but it must serve the parsed/sorted data). 
   - The service MUST listen on `127.0.0.1:8080`.
   - It must expose a `GET /api/v1/reports` endpoint.
   - It must require an `Authorization: Bearer <TOKEN>` header, where `<TOKEN>` is the exact secret token mentioned in the voicemail. Requests without this exact token must receive an HTTP 401 Unauthorized status.
   - Valid requests should return HTTP 200 OK with the sorted and merged JSON array.

Leave the service running in the background listening on port 8080 once you are finished.