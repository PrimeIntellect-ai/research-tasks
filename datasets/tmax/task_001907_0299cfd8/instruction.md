I need you to build a custom, highly-performant Kubernetes manifest processor in Rust to replace a sluggish legacy Python script. This processor acts as a client-side "operator" that enforces network and topology rules before deployment. 

We have a diagram with the new infrastructure rules located at `/app/topology_rules.png`.

Here is your objective:
1. **Extract Rules:** Use OCR (e.g., `tesseract`, which is pre-installed) to read the networking and topology constraints from `/app/topology_rules.png`.
2. **Rust Processor:** Create a Rust project at `/home/user/k8s_processor`. Write a robust application that reads a directory of input Kubernetes manifests (`/home/user/input_manifests/`), applies the extracted rules (modifying replicas, adding labels, and injecting network policies), and writes the modified YAML files to `/home/user/output_manifests/`.
3. **CI/CD & Process Supervision:** Create a robust bash pipeline script at `/home/user/pipeline.sh`. This script must:
    - Compile the Rust application (handling compilation errors gracefully).
    - Watch for changes in `/home/user/input_manifests/` (or simply run in a supervised loop every 2 seconds).
    - Ensure the Rust process is supervised and automatically restarted if it panics or fails due to malformed input.
4. **Accuracy Validation:** Your Rust implementation must correctly enforce all rules parsed from the image. We have an evaluator at `/home/user/evaluate_manifests.py` which will score the generated manifests in `/home/user/output_manifests/`.

Your goal is to achieve an accuracy score of **>= 0.95** (95%) when evaluated. 

Deliverables:
- The compiled Rust binary must be runnable via `/home/user/pipeline.sh`.
- The final processed manifests must be present in `/home/user/output_manifests/`.
- Ensure your Rust program properly uses `serde_yaml` or similar to safely manipulate the manifests without destroying existing fields.

Do your best to infer the exact label names, namespaces, and replica counts from the image, and embed that logic into your Rust program.