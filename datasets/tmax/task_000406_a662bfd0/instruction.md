We are migrating our legacy configuration manager and need to deprecate an old compiled utility that tracks file changes. 

The utility is located at `/app/bin/tracker_parser`. It reads a multi-line configuration log from standard input and outputs a sequence of standardized tracking actions. Unfortunately, we lost the source code for this binary.

Your task is to reverse-engineer the exact behavior of `/app/bin/tracker_parser` and write a Bash script that serves as a drop-in replacement. 

1. Analyze `/app/bin/tracker_parser` by running it and feeding it various inputs via standard input. The binary is stripped, but you can interact with it to deduce its parsing rules. It generally expects records separated by blank lines containing `ID:`, `FILE:`, and `STATUS:` fields.
2. Create a script at `/home/user/parse_config.sh` that reads from standard input and processes the multi-line records exactly as the binary does.
3. The output of your script must be bit-exact equivalent to the output of the binary for any given input log.

Ensure your script is executable and robust against malformed input, mimicking the binary's behavior in all cases.