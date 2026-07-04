You are a QA engineer setting up a new automated test environment. We are transitioning away from a legacy payload encoder to a modern microservice architecture. 

We have a legacy encoder binary at `/app/legacy_oracle`. It is a stripped binary that is currently used to format test payloads. It takes two command-line arguments: a semantic version and a raw string payload. Example: `/app/legacy_oracle 1.5.2 "test_data"`

Your task is to build a Rust-based HTTP microservice that acts as a drop-in replacement for the test environments, but extends the functionality for newer semantic versions.

Here are the exact requirements:
1.  **Analyze the Oracle:** Black-box test (or reverse engineer) `/app/legacy_oracle` to determine its exact encoding, sorting, and checksumming algorithm. It outputs a specific string format. It always assumes the version provided is `< 2.0.0`.
2.  **Create the Rust Microservice:** 
    *   Initialize a new Rust project at `/home/user/encoder_service`.
    *   Create an HTTP server listening on exactly `127.0.0.1:8080`.
    *   Expose a `POST /process` endpoint that accepts JSON: `{"v": "1.5.2", "payload": "test_data"}`
3.  **Implement the Routing Logic:**
    *   Parse the semantic version `v`.
    *   If `v < 2.0.0`: Replicate the exact logic of the `/app/legacy_oracle`.
    *   If `v >= 2.0.0`: The logic changes. Calculate the CRC32 of `payload`. Encode `payload` using standard Base32 (RFC 4648 without padding). Do NOT sort the encoded characters. The output format should be exactly `V_[v]_CRC_[crc32_hex_lowercase]_[base32_data]`.
4.  **Polyglot Integration:**
    *   There is a C integration test client at `/app/integration_tester.c`.
    *   Write a script at `/home/user/build_and_run.sh` that builds your Rust service in release mode, starts it in the background, compiles `/app/integration_tester.c` using `gcc` (linking `libcurl`), and executes the compiled C binary.

The automated verification suite will make direct HTTP POST requests to `127.0.0.1:8080/process` using both legacy (`< 2.0.0`) and modern (`>= 2.0.0`) version numbers to test your encoding, sorting, checksumming, and semver comparison implementations. Ensure the Rust service remains running.