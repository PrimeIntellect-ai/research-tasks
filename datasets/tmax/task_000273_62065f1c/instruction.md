You are a build engineer responsible for managing web security artifacts. You need to create a test fixture and a security scoring report based on a given artifact manifest.

The manifest file is located at `/home/user/artifact_manifest.csv`. It contains a list of build artifacts in the format: `ArtifactName,SizeInBytes,OctalPermission`.

Write a Bash script at `/home/user/process_artifacts.sh` that performs the following tasks:

1. **Test Fixture Setup**:
   - Create a directory called `/home/user/mock_artifacts/`.
   - For each entry in the manifest, create a dummy file in this directory with the exact `ArtifactName`.
   - Ensure the dummy file has the exact size specified in `SizeInBytes` (you can use the `truncate` command).
   - Set the file's permissions to the specified `OctalPermission` (e.g., `0644`).

2. **Numerical Security Scoring**:
   - For each artifact, calculate a "risk score" using the following formula: 
     `Score = ((SizeInBytes XOR DecimalMode) * 13) MODULO 97`
     *(Note: `DecimalMode` is the base-10 integer value of the octal permission. For example, octal `0644` is decimal `420`. XOR is the bitwise exclusive OR operation).*

3. **Serialization**:
   - Output the results as a JSON array to `/home/user/security_report.json`.
   - The JSON must be strictly formatted. For each artifact, include an object with keys `"artifact"` (string) and `"score"` (integer).
   - Example format:
     ```json
     [
       {
         "artifact": "app.tar.gz",
         "score": 72
       },
       {
         "artifact": "deploy.sh",
         "score": 25
       }
     ]
     ```
     (You may output it compactly as `[{"artifact":"app.tar.gz","score":72},{"artifact":"deploy.sh","score":25}]` as well).

Ensure your script is executable (`chmod +x /home/user/process_artifacts.sh`) and run it so the directory and JSON file are created. Use standard Bash built-ins and standard CLI utilities (like `cat`, `mkdir`, `truncate`, `chmod`).