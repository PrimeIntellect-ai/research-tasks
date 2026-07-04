You are a security script developer. We have an old legacy WAF (Web Application Firewall) rule parser written in Ruby that we need translated to Python. The script parses custom `.wafr` (WAF Rule) files, compares them against a list of installed packages, and determines which packages are vulnerable based on semantic versioning rules.

Your task is to write a Python 3 script at `/home/user/waf_analyzer.py` that replicates the behavior of the legacy Ruby script, parses the rule files using a state machine, evaluates the semantic version requirements, and outputs a final JSON report.

Here is the setup:
1. The legacy Ruby script is located at `/home/user/legacy_parser.rb`. Read it to understand the parsing state machine and the version comparison logic.
2. A directory of WAF rules is located at `/home/user/rules/`.
3. A JSON file containing the currently installed packages and their versions is at `/home/user/packages.json`.

Your Python script `/home/user/waf_analyzer.py` must:
1. Accept two arguments: the path to the rules directory, and the path to the packages JSON file. 
   Example: `python3 /home/user/waf_analyzer.py /home/user/rules /home/user/packages.json`
2. Implement a state machine to parse the `.wafr` files, exactly as the Ruby script does (handling `RULE`, string extraction, and block parsing).
3. Implement semantic version comparison. The `VULN_VERSIONS` field in a rule contains comma-separated conditions (e.g., `>= 1.2.0, < 2.0.0`). A package is vulnerable only if its version satisfies ALL conditions in the string. Standard semver rules apply (e.g., `2.0.0` is greater than `1.15.9`).
4. Output the results to `/home/user/vulnerabilities.json` in the following exact format:
```json
{
  "RuleName": {
    "affected_package": "package_name",
    "installed_version": "x.y.z",
    "is_vulnerable": true
  }
}
```
Only include rules that were successfully parsed. `is_vulnerable` should be a boolean (`true` if the installed package matches the `AFFECTS` field and the installed version satisfies the `VULN_VERSIONS` conditions, `false` otherwise or if the package is not installed).

Please write the Python script, run it against the provided rules and packages, and generate the `/home/user/vulnerabilities.json` file.