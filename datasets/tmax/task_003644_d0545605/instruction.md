You are an automation specialist managing a complex data pipeline. We have a proprietary, undocumented legacy binary at `/app/legacy_parser` that processes custom application logs. 

This binary takes raw log lines via standard input, performs timestamp alignment, extracts specific features (tags) from the message payload, and stratifies the log into a specific bucket based on its timestamp. It outputs the processed result to standard output.

Your task is to reverse-engineer the logic of this stripped binary and write a modern replacement. 
You can use any language you prefer (Python, Perl, Ruby, Bash, etc.), but your final solution must be wrapped in an executable shell script located at `/home/user/run.sh`. 

Requirements for `/home/user/run.sh`:
1. It must read line-by-line from standard input (just like the binary).
2. It must write the processed output to standard output.
3. For any given valid input string, your script's output must be **bit-for-bit identical** to the output of `/app/legacy_parser`.

To accomplish this, you will need to:
- Pass various test strings into `/app/legacy_parser` and observe its output.
- Figure out how it parses its custom timestamp format and aligns it to a UNIX epoch (assume UTC).
- Figure out how it extracts features (specifically, tags) from the message.
- Figure out its stratification logic (how it assigns a bucket number based on the data).
- Implement this exact logic in your own script.

The inputs will generally look like this:
`<Timestamp>|<Category>|<Message>`

Example input:
`2023.15.08/14:30:00|INFO|System started by @admin with @fast_boot enabled`

Do not hardcode answers for specific inputs; your script will be tested against a massive suite of thousands of randomly generated log lines to ensure perfect equivalence with the legacy binary.