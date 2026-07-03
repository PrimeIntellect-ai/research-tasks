You are acting as an automated release manager. We have a deployment manifest that specifies various microservices we want to deploy, but not all of them meet the resource and geographical constraints required for this release cycle. 

You need to write a Go program that processes this manifest, enforces the deployment constraints, and generates an approved deployment roster with encoded deployment tokens.

1. Read the input JSON file located at `/home/user/deploy_manifest.json`.
2. Parse it into custom Go data structures. The JSON has the following structure:
   - `global_allowed_regions`: A list of strings representing regions where deployments are currently permitted.
   - `services`: A list of objects, each containing:
     - `name` (string): The service name.
     - `version` (string): The service version.
     - `memory_limit_mb` (int): The maximum memory allocated to the container.
     - `required_memory_mb` (int): The minimum memory the service needs to boot.
     - `target_region` (string): The region where the service is requested to be deployed.

3. Apply constraint satisfaction logic to filter the `services`. A service is ONLY approved if:
   - Its `target_region` is present in the `global_allowed_regions` list.
   - Its `memory_limit_mb` is strictly greater than or equal to its `required_memory_mb`.

4. For each approved service, generate a `deployment_token`. The token is created by:
   - Concatenating the service name and version with a colon (e.g., `auth-service:v1.2.0`).
   - Encoding the resulting string using standard RFC4648 Base32 encoding, but **without padding** characters (`=`).

5. Write the approved services to `/home/user/roster.json` as a JSON array of objects. Each object must have exactly two fields:
   - `service` (string): The name of the service.
   - `token` (string): The Base32 encoded deployment token.
   Sort the output array alphabetically by the `service` name.

You must implement this in a Go file at `/home/user/process_release.go` and run it to produce the `roster.json` file.