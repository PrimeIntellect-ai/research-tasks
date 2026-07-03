You are acting as an AI assistant for a Release Manager preparing a new deployment pipeline. We are migrating our deployment manifests from version `v1` to `v2` and need a validation service to gate deployments. 

First, there is a scanned image of a legacy architecture note located at `/app/legacy_schema.png`. You must read this image (using OCR tools like `tesseract`, which is preinstalled) to discover a critical schema migration constraint that was never formally documented. 

Next, initialize a new Rust project at `/home/user/deployment_validator`.
In this project, build a REST API (using a framework of your choice, like `axum` or `warp`) that listens on `127.0.0.1:3030`. 

The API must expose a single endpoint:
`POST /validate`

This endpoint will receive JSON payloads representing Deployment Manifests. The JSON structure is:
```json
{
  "previous_version": "v1",
  "target_version": "v2",
  "pre_deploy_hook": "echo 'starting'",
  "services": [
    { "name": "web", "image": "nginx:latest" }
  ]
}
```

Your Rust API must:
1. Parse this custom data structure.
2. Validate that the `services` array is not empty.
3. Apply the critical schema migration rule extracted from `/app/legacy_schema.png`.
4. Return an HTTP `200 OK` if the manifest is perfectly valid and safe.
5. Return an HTTP `400 Bad Request` if the manifest violates the migration rule, is empty, or is structurally invalid.

Write property-based or unit tests in your Rust project to ensure your validation logic is robust against malicious injections. Once your code is thoroughly tested, compile and run the REST API in the background. 

When the server is up and listening on port 3030, write the word "DONE" to `/home/user/status.txt` and exit. Our automated integration pipeline will then blast your API with a corpus of clean and malicious manifests to verify your implementation.