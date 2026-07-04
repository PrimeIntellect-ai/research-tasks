I'm working on a web security system that uses a combination of a Rust-based WebSocket/gRPC server and a Python payload sanitiser. Right now, I'm facing two major issues:

1. My Rust project located at `/home/user/rust_server` is failing to compile. I left a voice memo for myself earlier with the exact fix for the dependencies, but I don't remember what it was. The audio file is located at `/app/voice_memo.wav`. Please transcribe it to find out which semantic version the gRPC dependency needs to be updated to, and fix the Rust project so that `cargo build` succeeds.

2. I need you to write a Python classifier at `/home/user/filter.py` that filters incoming WebSocket payloads based on the semantic version rules mentioned in the same audio file. The Python script should take a JSON string as a single command-line argument. The JSON represents a parsed WebSocket payload which contains a `"client_version"` field.
Your script must:
- Parse the `"client_version"` field as a semantic version.
- Accept the payload (exit code 0) if the version satisfies the security requirements described in the audio file.
- Reject the payload (exit code 1) if the version is vulnerable/unsupported, or if the payload is malformed.

Please implement the fix and the Python script. I have an adversarial corpus to test the script against, so ensure your semantic version comparison is robust.