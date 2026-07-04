We are porting a legacy tool to a minimal container environment. As part of this effort, we need a lightweight Rust HTTP service that validates software versions against a policy document. Unfortunately, the policy document is currently only available as an image.

You have been provided a skeleton Rust project in `/home/user/policy-service`. 

Your objectives are:
1. **Extract Policy:** Use the preinstalled `tesseract` CLI tool to extract the semantic version constraint from the image located at `/app/policy.png`. The image contains a single line of text representing a version constraint (e.g., `>=1.0.0 <2.0.0`).
2. **Fix Semantic Versioning Logic:** The project contains a module `src/semver.rs` with a custom semantic version parser and comparator. It currently has a bug where it incorrectly compares minor and patch versions when the major versions match. Fix this bug.
3. **Add Property-Based Tests:** Write a property-based test in `src/semver.rs` using the `proptest` crate (already included in `Cargo.toml`) to verify that your version comparison logic satisfies transitivity (i.e., if A > B and B > C, then A > C). Ensure `cargo test` passes.
4. **Implement HTTP Endpoint:** Complete the web server in `src/main.rs`. It must listen on `127.0.0.1:8080`. 
   - Expose a `POST /validate` endpoint.
   - The endpoint should accept a JSON payload: `{"version": "x.y.z"}`.
   - It should dynamically read the policy constraint extracted from `/app/policy.png` (using `tesseract`), parse it using the `semver` module, and check if the provided version satisfies the constraint.
   - Return a JSON response: `{"allowed": true}` or `{"allowed": false}`.

Once your service is implemented and tested, compile it and start it in the background. When the server is successfully listening on port 8080, create an empty file at `/tmp/service_ready` to signal that verification can begin.