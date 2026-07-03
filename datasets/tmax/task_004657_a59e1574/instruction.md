You are a release manager tasked with preparing a deployment package for a microservices architecture. The developers have handed off a small release candidate located in `/home/user/release_prep`. However, the build is broken, the protobuf definitions are incomplete, and the deployment configuration needs to be extracted.

Your goal is to complete the release preparation by fulfilling the following tasks strictly using Bash and standard Linux command-line tools:

1. **Structured Data Parsing:**
   There is a JSON file at `/home/user/release_prep/deployment.json`. You must parse this file to extract the `service_name`, `target_environment`, and `version`. 
   Create a file named `/home/user/release_prep/release.env` containing these values in the following exact format:
   ```
   SERVICE_NAME=<service_name>
   ENVIRONMENT=<target_environment>
   RELEASE_VERSION=<version>
   ```

2. **Protobuf Service Design Update:**
   The service definition at `/home/user/release_prep/service.proto` is missing a critical endpoint required by the new release. 
   Update `service.proto` to include a new message called `HealthCheckResponse` with a single boolean field `healthy` (tag 1).
   Then, update the `DeploymentService` service block within the same file to include a new rpc call named `HealthCheck` that takes `google.protobuf.Empty` as input and returns `HealthCheckResponse`.

3. **Fix the Makefile Linking Error:**
   The codebase includes a small C utility for deployment checks. If you run `make` in `/home/user/release_prep/`, the `check_util.c` file compiles into an object file, but fails during the linking phase with an "undefined reference" error (it uses a math function but doesn't link the math library).
   - First, create a backup of the original Makefile at `/home/user/release_prep/Makefile.orig`.
   - Fix the `Makefile` so that the executable `check_util` builds successfully.
   - Run `make` to ensure the `check_util` binary is generated.

4. **Diff and Patch Processing:**
   Generate a standard unified diff patch representing your fix to the Makefile.
   Compare `Makefile.orig` and your fixed `Makefile`. Save the patch output to `/home/user/release_prep/makefile_fix.patch`.

Ensure all requested files (`release.env`, `service.proto`, `Makefile`, `check_util`, and `makefile_fix.patch`) are exactly in the `/home/user/release_prep` directory with the correct names and contents.