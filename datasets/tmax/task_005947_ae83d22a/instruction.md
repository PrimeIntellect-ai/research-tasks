You are assisting a release manager who needs to prepare deployments across a large microservice architecture. 

Your task is to create a Rust program that reads two state files, compares the semantic versions of the services, diffs them, and outputs a strict deployment plan.

You have been provided with two files:
1. `/home/user/current_release.json` - The current state of deployed microservices.
2. `/home/user/target_release.json` - The desired state of deployed microservices.

Both files share the following JSON schema:
```json
{
  "services": [
    {
      "name": "string",
      "version": "string (valid SemVer)"
    }
  ]
}
```

Write a Rust program in a new Cargo project located at `/home/user/release-diff`. 
Your program must:
1. Deserialize both JSON files.
2. Compare the services by name to find the diff.
3. Use strict Semantic Versioning rules to compare versions (including pre-release identifiers).
4. Serialize a deployment plan and save it to `/home/user/deployment_plan.json`.

The output file `/home/user/deployment_plan.json` must exactly match this JSON structure:
```json
{
  "actions": [
    {
      "action": "STRING",
      "name": "STRING",
      "from_version": "STRING or null",
      "to_version": "STRING or null"
    }
  ]
}
```

**Business Rules for the Diff:**
- The `actions` array must be **sorted alphabetically** by the service `name`.
- `action` can be one of the following:
  - `"INSTALL"`: The service is in the target release but not in the current release. (`from_version` must be `null`).
  - `"REMOVE"`: The service is in the current release but not in the target release. (`to_version` must be `null`).
  - `"UPGRADE"`: The target version is strictly greater than the current version according to SemVer.
  - `"ROLLBACK"`: The target version is strictly less than the current version according to SemVer.
  - `"KEEP"`: The versions are exactly the same.

You may use standard community crates (e.g., `serde`, `serde_json`, `semver`) by configuring your `Cargo.toml`. When finished writing the code, build and run your Rust project so that `/home/user/deployment_plan.json` is generated.