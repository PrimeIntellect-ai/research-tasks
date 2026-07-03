We are implementing a GitOps workflow for our Kubernetes operator. To ensure security and compliance before manifests are deployed, we need to enforce a strict security policy via a validation tool that will eventually be used as a Git `pre-receive` hook. 

The exact security policy has been recorded in an audio memo by our security lead. 
1. Transcribe or listen to the audio file located at `/app/k8s_policy.wav` to understand the restriction being enforced.
2. Write a Rust command-line application in `/home/user/validator`. 
3. Your Rust application must take a single file path as an argument (e.g., `./validator /path/to/manifest.yaml`).
4. The tool must read and parse the Kubernetes YAML manifest. If the manifest violates the policy specified in the audio file, the tool must exit with a non-zero status code (reject). If the manifest complies with the policy, it must exit with status code `0` (accept).
5. Compile your Rust project in release mode so the final binary is located at `/home/user/validator/target/release/validator`.
6. Make sure your Rust application correctly handles multi-document YAML files (files containing `---`), as a single violation in any document should reject the entire file.

For your testing, we have provided two directories containing sample Kubernetes manifests:
- `/app/corpora/clean/`: Contains manifests that are compliant with the policy.
- `/app/corpora/evil/`: Contains manifests that violate the policy.

An automated grader will run your compiled binary against hidden, extended versions of these corpora.