You are a technical writer organizing documentation for a legacy software project. The team currently relies on a proprietary, undocumented, and stripped binary tool located at `/app/doc_compiler` to parse the company's internal binary documentation format (`.tdoc`) into readable Markdown files. 

Because we are migrating to a new CI/CD pipeline where this old binary won't run, we need to replace it with a native Python script. 

Your task is to reverse-engineer the behavior of `/app/doc_compiler` and write a Python script at `/home/user/py_compiler.py` that parses `.tdoc` files in exactly the same way. 

The legacy binary is invoked like this:
`/app/doc_compiler <input_file.tdoc> <output_file.md>`

Requirements:
1. Your Python script must be executable exactly like this: `python3 /home/user/py_compiler.py <input_file.tdoc> <output_file.md>`.
2. It must produce **bit-exact identical output** to `/app/doc_compiler` for any valid or invalid `.tdoc` file.
3. It must replicate all error messages (to standard output or standard error) and exit codes produced by the binary when given corrupted or invalid files.
4. The binary reads a configuration file located at `/home/user/compiler_config.ini` to determine how to format certain sections. Your script must also parse and respect this configuration file identically.

To figure out the file format and behavior, you should create some dummy `.tdoc` files, modify the configuration file, and observe how `/app/doc_compiler` processes them. 

Write the final `/home/user/py_compiler.py` script once you have perfectly matched the binary's behavior.