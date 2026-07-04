You are a platform engineer maintaining a custom CI/CD pipeline. Before artifacts are deployed to the production environment, the pipeline evaluates complex deployment constraints against the current system state. 

Your task is to write a Python script `/home/user/evaluate_deployments.py` that parses the current system state, parses the deployment manifests, evaluates their constraint expressions, and generates a JSON report.

**System State Format:**
The current installed modules are listed in `/home/user/system_state.txt`. Each line represents a module in this format:
`Module: <module_name> Version: <semver>`
(e.g., `Module: auth-service Version: 2.1.0`)

**Manifests:**
The directory `/home/user/manifests/` contains several JSON files (`manifest_*.json`). Each manifest has the following structure:
```json
{
  "manifest_id": "deploy-123",
  "constraint": "(auth-service >= 2.0.0 & db-driver < 2.0.0)"
}
```

**Constraint Expression Grammar:**
- Variables are module names (e.g., `auth-service`).
- Operators: `==`, `>`, `<`, `>=`, `<=`.
- Boolean logic: `&` (AND), `|` (OR), `!` (NOT).
- Parentheses `()` can be used for grouping.
- Version strings are strict Semantic Versioning (`X.Y.Z`). You should use standard semver comparison rules (you can use `packaging.version.parse` from the standard Python ecosystem).
- If a module in the expression is *not* found in the `system_state.txt`, any comparison operator against it should evaluate to `False`.

**Goal:**
Write the Python script to evaluate all JSON manifests in `/home/user/manifests/`. The script must output a JSON file to `/home/user/deployment_report.json` containing a single dictionary mapping each `manifest_id` to a boolean indicating whether the constraint expression evaluates to `True` (deployable) or `False` (not deployable).

Example Output (`/home/user/deployment_report.json`):
```json
{
  "deploy-123": true,
  "deploy-456": false
}
```
Ensure your script writes the output formatted exactly as standard JSON. Execute your script to create the file before completing the task.