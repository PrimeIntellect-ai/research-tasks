You are a data engineer tasked with migrating an old ETL pipeline. We have a legacy data transformation tool that reads wide-format system metrics, reshapes them into long-format records, applies a text template, and generates simulated transfer payloads for a remote data lake.

The legacy tool is available as a compiled executable at `/app/legacy_transformer`. Unfortunately, the original source code has been lost, and the binary has been stripped of debug symbols.

Your task is to write a replacement program in Go that is **bit-exact equivalent** to the legacy binary.
You must figure out exactly how the legacy binary processes input and generates output by interacting with it (e.g., feeding it test data and observing the results) or reverse engineering it.

Requirements:
1. Write your Go source code in `/home/user/new_transformer.go`.
2. Compile your Go program to `/home/user/new_transformer`.
3. Your compiled program must read from standard input and write to standard output.
4. It must exactly match the output format, spacing, reshaping logic, severity rules, and simulated remote-transfer payload generation of the legacy tool for any valid input.
5. The input will always be a CSV file provided via standard input.

You can run `/app/legacy_transformer` with your own test CSV inputs to deduce its behavior. Pay close attention to how it handles headers, different value ranges, and missing/invalid data.