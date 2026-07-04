As a release manager, you are preparing a deployment for a Rust web security tool located at `/home/user/web_sec_tool`. 

The tool has two major security and compatibility constraints that you must resolve:

1. **C Library Dependency (Build System & Linking)**:
   The tool links against a local custom cryptography library, `libwebcrypto`. The compiled shared objects are located in `/home/user/libwebcrypto/`. 
   Available versions in that directory are `1.2.0`, `1.3.4`, `1.3.5`, and `2.0.0`.
   - Security advisory: All versions `< 1.3.5` are vulnerable to a known buffer overflow.
   - Compatibility: Version `2.x.x` has breaking API changes and will not work with our Rust code.
   You must satisfy these constraints by configuring the system/build so that `cargo build` successfully links against the highest safe, compatible version of `libwebcrypto`. You may need to create necessary symlinks in the library directory so the Rust build system can find it.

2. **Rust Dependency (Constraint Satisfaction & SemVer)**:
   The project's `Cargo.toml` currently depends on an older version of the `regex` crate.
   - Security advisory: Versions `< 1.9.0` have a known vulnerability.
   - Compatibility constraint: Our internal codebase is incompatible with `regex` versions `>= 1.10.0`.
   Update the `Cargo.toml` to specify a SemVer constraint that guarantees a version `>= 1.9.0` and `< 1.10.0`. Ensure the project successfully compiles with `cargo build`.

After configuring the dependencies and successfully building the project, create a summary report at `/home/user/deployment.json` containing the exact `regex` version resolved in `Cargo.lock` and the `libwebcrypto` version you selected.

The JSON file must have exactly this format:
```json
{
  "regex_version": "<exact_resolved_version>",
  "libwebcrypto_version": "<selected_version>"
}
```

Ensure that running `cargo run` inside `/home/user/web_sec_tool` executes successfully after your changes.