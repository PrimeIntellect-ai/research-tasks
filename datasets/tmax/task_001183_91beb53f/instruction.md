You are a mobile build engineer maintaining a secure CI/CD pipeline. Build artifacts are currently represented using a legacy schema (Version 1) which relies on weak MD5 hashing. For better web security and integrity verification when artifacts are uploaded, we are migrating to Version 2, which uses SHA256 and a secure manifest grouping.

Your task is to implement the schema migration, design a custom `Manifest` data structure to group the artifacts securely, and write property-based tests to ensure the migration is flawless.

All work must be done in the `/home/user/workspace` directory, which is already set up as a Go module.

1. Inspect the existing file `/home/user/workspace/artifact.go`, which contains the `ArtifactV1` struct.
2. In the same file, define the `ArtifactV2` struct with the following fields:
   - `Identifier` (string)
   - `Bytes` (int)
   - `Checksum` (string) - Must be the hex-encoded SHA256 hash of the payload.
   - `Payload` ([]byte)
   - `Version` (int) - Must always be 2.
3. Define a `Manifest` struct in the same file with:
   - `Artifacts` ([]ArtifactV2)
   - `ManifestHash` (string) - Must be the hex-encoded SHA256 hash of the direct concatenation of all the `Checksum` strings in the `Artifacts` array (in order).
4. Implement a function `Migrate(v1 ArtifactV1) ArtifactV2` that maps a V1 artifact to V2. `ID` maps to `Identifier`, `Data` to `Payload`. Ensure `Bytes` is set to the actual length of the `Payload`, and compute the correct SHA256 `Checksum`.
5. Implement a function `GenerateManifest(artifacts []ArtifactV2) Manifest` that creates a manifest and calculates its `ManifestHash`.
6. Create a test file `/home/user/workspace/artifact_test.go`. Write a property-based test function named `TestMigrationProperty` using Go's `testing/quick` package. The property tested should verify that for any randomly generated `ArtifactV1`, the resulting `ArtifactV2` from `Migrate()` has:
   - `Bytes` equal to the length of `Payload`.
   - `Version` equal to 2.
   - `Checksum` correctly equal to the hex-encoded SHA256 of the `Payload`.
   - `Identifier` equal to the original `ID`.
7. Write a standard unit test `TestGenerateManifest` to verify that `GenerateManifest` computes the correct `ManifestHash`.
8. Run your tests and save the output using the following command:
   `go test -v ./... > /home/user/workspace/test_results.log`

Make sure your implementation compiles and the tests pass. The automated verification will check the `test_results.log` file and inspect the functions and types in `artifact.go`.