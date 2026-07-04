You are an infrastructure engineer tasked with securing our automated provisioning pipeline. 

We use a proprietary provisioning daemon to set up disk quotas, mount points, and network rules on our servers. The daemon relies on a configuration parser binary located at `/app/provtool`. Unfortunately, we've lost the source code for this binary.

Recently, we discovered that `/app/provtool` is vulnerable to several issues when processing malformed or maliciously crafted configuration files:
1. It crashes (segfaults) on certain inputs.
2. It silently applies unsafe settings (like arbitrary path writes or disabling SSH authentication) if specific undocumented flags or boundary values are present.

To prevent our CI/CD pipeline from feeding bad configs to the provisioning daemon, you need to write a pre-flight validator in Go.

Your task:
1. Analyze the stripped binary `/app/provtool` and the provided example configs in `/home/user/examples/clean/` and `/home/user/examples/evil/` to deduce the exact rules of what constitutes a valid vs. invalid (malicious/crashing) configuration.
2. Write a Go program at `/home/user/filter.go` and compile it to `/home/user/filter`.
3. The executable `/home/user/filter` must take a single command-line argument containing the absolute path to a configuration file.
   Usage: `/home/user/filter /path/to/config.txt`
4. The program must print "SAFE" to stdout and exit with status code 0 if the configuration is fully valid and safe.
5. The program must print "REJECT" to stdout and exit with status code 1 if the configuration is malicious, out-of-bounds, or triggers a crash in `/app/provtool`.
6. Ensure your code is robust, handles missing files gracefully (exit code 1), and parses the text effectively.

For your analysis, you may use standard tools like `strings`, `objdump`, `strace`, and black-box testing against `/app/provtool`.

An automated test suite will later run your `/home/user/filter` against a hidden adversarial corpus consisting of many clean and evil files. To pass, your filter must achieve 100% accuracy: rejecting all evil configs and preserving all clean ones.