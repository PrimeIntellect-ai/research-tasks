You are a script developer tasked with creating a build automation utility for a polyglot monorepo. 

In `/home/user/project`, there is a multi-language project containing C, Python, Bash, and Ruby files. The build configuration is defined in a structured JSON file at `/home/user/project/build_config.json`. 

Your goal is to write a script (in the language of your choice) that parses this JSON file, resolves the dependency graph, and generates two artifacts:
1. A valid GNU `Makefile` in `/home/user/project/Makefile`.
2. A GitHub Actions CI/CD pipeline configuration in `/home/user/project/.github/workflows/ci.yml`.

### Specifications for `build_config.json`
The JSON file has a single key `targets`, which is an object mapping target names to their configurations.
Example:
```json
{
  "targets": {
    "my_c_prog": { "lang": "c", "src": "main.c", "deps": ["prep_script"] },
    "prep_script": { "lang": "bash", "src": "prep.sh", "deps": [] }
  }
}
```

### 1. Makefile Requirements
Your script must generate a `Makefile` in `/home/user/project/Makefile` with the following rules:
- **Dependencies:** Each target in the Makefile must explicitly list its `src` file and all of its `deps` (other target names) as prerequisites.
- **Build Commands:**
  - If `lang` is `"c"`, the command must compile the source file into an executable named after the target using `gcc`: `gcc <src> -o <target>`
  - If `lang` is `"python"`, `"ruby"`, or `"bash"`, the command must copy the source file to an executable named after the target and make it executable: `cp <src> <target>` followed by `chmod +x <target>`
- **All Target:** The Makefile must include a default `all` target at the top that depends on all targets defined in the JSON file.

### 2. CI/CD Pipeline Requirements
Your script must generate a GitHub Actions workflow file at `/home/user/project/.github/workflows/ci.yml` with the following contents:
- It must trigger on `push` to the `main` branch.
- It must contain a single job named `build` running on `ubuntu-latest`.
- The job must have two steps:
  1. A step named "Checkout code" using `actions/checkout@v3`.
  2. A step named "Build all targets" that runs `make all`.

### Execution
After writing your script, run it so that the `Makefile` and `ci.yml` are generated in `/home/user/project/`.
Ensure the `.github/workflows` directory is created if it does not exist.
You can use `make all` inside `/home/user/project` to verify your generated Makefile works correctly.