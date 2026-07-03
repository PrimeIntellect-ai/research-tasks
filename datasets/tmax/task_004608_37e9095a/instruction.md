You are acting as a localization engineer. We have a legacy data transformation tool that processes our translation files. The tool is currently a stripped binary located at `/app/loc_oracle`. It is undocumented, and the original source code was lost. 

Your task is to reverse-engineer the behavior of this binary by interacting with it, and then write a replacement in Go.

Here is what we know about the pipeline:
1. **Input**: The tool reads from `standard input`. The input is a "wide format" CSV without a header. Each row always has exactly 4 columns: `ID,EN_STRING,ES_STRING,FR_STRING`.
2. **Processing**: 
   - It reshapes this wide format into a "long format".
   - It performs tokenization/normalization on the strings.
   - It calculates a distance metric (likely Levenshtein distance) between the normalized English base string and the normalized target language strings.
3. **Output**: It writes the transformed data to `standard output` in a specific format (you will need to observe the exact output format, delimiter, and normalization rules by testing the binary).

Write your Go solution in `/home/user/main.go` and compile it to `/home/user/loc_tool`. 

Your compiled executable (`/home/user/loc_tool`) must be a drop-in replacement for `/app/loc_oracle`. It must read from `stdin`, write to `stdout`, and produce **bit-exact identical output** to the oracle binary for any valid input.