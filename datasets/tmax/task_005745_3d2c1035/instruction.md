You are a mobile build engineer maintaining a massive CI/CD pipeline. Currently, when C builds fail due to missing linker symbols, the logs are massive and hard for developers to read. We want to extract just the missing symbols and serialize them to JSON so our dashboard can ingest them.

I have placed a sample raw build error log at `/home/user/linker_error.log`. 

Your task is to:
1. Write a Python script at `/home/user/parse_linker.py` that reads `/home/user/linker_error.log`.
2. Inside the script, use a state machine logic to parse the `ld` output. The state machine must keep track of the "current object file" being processed and extract any undefined symbols associated with it.
3. Serialize the extracted data into a strictly formatted JSON file at `/home/user/missing_symbols.json`.
4. Create a bash script at `/home/user/benchmark.sh` that benchmarks the Python script using the shell built-in `time` command (running the python script 50 times in a loop) to ensure our parser is performant. Redirect the standard error of the `time` command (which contains the timing data) to `/home/user/benchmark.log`.

**Format of the Log File:**
The log contains standard `gcc`/`ld` error lines:
```
/usr/bin/ld: <object_file>: in function `<function_name>':
<source_file>:(.text+0x<hex>): undefined reference to `<symbol>'
```
Note that multiple `undefined reference` lines can follow a single `in function` line without restating the object file.

**Expected JSON Format for `/home/user/missing_symbols.json`:**
```json
{
  "ui_module.o": [
    {
      "file": "ui_module.c",
      "symbol": "draw_rect"
    },
    ...
  ],
  "network.o": [
    ...
  ]
}
```
Ensure the JSON is properly formatted and contains exactly the structured data derived from the log.