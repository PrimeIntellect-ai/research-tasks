We are migrating away from a proprietary, legacy system configuration generator, but we lost the source code. The generator is a compiled Linux binary located at `/app/legacy_config_gen`. It is a stripped binary.

Your task is to analyze this binary and write a new, equivalent program in Python 3 (or any other language installed on the system, like Bash or Perl) that perfectly replicates its behavior.

The legacy binary reads a configuration file from a path specified as the first command-line argument. The configuration file contains a list of directives, one per line.
The directives are of the form:
`ALLOW <IP_ADDRESS> <PORT_START>-<PORT_END>`
`BLOCK <IP_ADDRESS> <PORT>`

The legacy binary processes this file and outputs a sequence of `iptables` commands to stdout. It also ignores lines starting with `#` and empty lines. 

You need to reverse-engineer the exact formatting and logic of the `iptables` commands it outputs. For example, you need to see exactly what flags it uses (like `-A INPUT`, `-p tcp`, `--dport`, etc.).

Write your replacement program and save it as an executable file at `/home/user/new_config_gen`. Your program must accept exactly one command-line argument (the path to the input file) and print the exact same output to stdout as the legacy binary would for any valid input file.

To test your implementation, you can create sample input files and compare the output of `/app/legacy_config_gen sample.txt` with `/home/user/new_config_gen sample.txt`.