You are an infrastructure engineer tasked with implementing a configuration quality gate for our new change management pipeline. 

We have a legacy configuration validation binary located at `/app/legacy_checker`. This stripped binary parses our custom `.cfg` files and exits with `0` if the configuration is valid according to our business logic, and `1` if it violates our constraints. 

However, `/app/legacy_checker` has two major problems:
1. It is extremely slow and cannot handle our new high-throughput stream processing pipeline.
2. It completely lacks security validation and blindly accepts shell metacharacters in the `ActionCmd` field, leaving our systems vulnerable to command injection.

Your task is to write a fast, secure pre-filter script at `/home/user/config_gate.py`. 

The script must:
1. Accept a single argument: the path to a `.cfg` file.
2. Parse the configuration file. The files are text-based, consisting of `Key: Value` pairs (one per line). Extraneous whitespace should be normalized/ignored.
3. Validate the `Timeout`, `MaxRetries`, and `NodeName` fields by perfectly replicating the hidden constraint logic inside `/app/legacy_checker`. You will need to interact with the binary to reverse-engineer its exact acceptable ranges and patterns.
4. Implement a strict security constraint on the `ActionCmd` field using regex pattern construction: `ActionCmd` must ONLY contain alphanumeric characters, spaces, hyphens, underscores, forward slashes, and periods. Any other character (e.g., `;`, `&`, `$`, `|`, `` ` ``, etc.) must be strictly rejected.
5. Exit with status code `0` if the file perfectly satisfies the legacy constraints AND the security constraints.
6. Exit with status code `1` if the file violates ANY constraint (legacy business logic or the new security rule) or is malformed.

For your testing, a sample set of configuration files is provided in `/app/samples/`. However, your script will be tested against a hidden, massive adversarial corpus to ensure it perfectly classifies safe and malicious configs.

Ensure your script operates independently of the legacy binary (do not just call `/app/legacy_checker` from your script, as it defeats the performance goal and still fails the security requirement).