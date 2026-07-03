You are a developer tasked with organizing a legacy project dump that was provided to you as a compressed archive. 

Your starting point is a file located at `/home/user/legacy_project.tar.gz`.

Here are your instructions:
1. **Extract the Main Archive**: Extract `/home/user/legacy_project.tar.gz`. Inside, you will find a multi-part archive (`split_data.tar.gz.part1`, `split_data.tar.gz.part2`) and a configuration file named `layout.json`.
2. **Handle the Multi-part Archive**: Reassemble the multi-part archive into a single valid tarball and extract its contents into a directory named `/home/user/source_files/`. Inside, there will be several source files.
3. **Process with Go**: Write a Go program at `/home/user/process.go`. This program must:
   - Parse `layout.json` (which contains an array of file mapping objects with `name` and `category` fields).
   - Find the corresponding files inside `/home/user/source_files/`.
   - Read the contents of each file specified in the layout.
   - Print the mapped category and filename, followed by the exact file content, to Standard Output (`stdout`). The exact format for each file must be:
     `[{category}/{name}]`
     `{content}`
     (Make sure there is exactly one newline after the header, and one newline after the content before the next file).
4. **Redirection**: Run your Go program and use standard stream redirection (pipe or redirect) to save the output into a log file located at `/home/user/final_report.log`.

Do not hardcode the contents of the files in your Go program; it must read the configuration and the extracted files dynamically.