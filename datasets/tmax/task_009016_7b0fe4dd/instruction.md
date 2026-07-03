You are acting as a systems programmer who is debugging a C library linking issue. We have a dump of symbols from two mixed C libraries in a text file, and we need to identify link conflicts where the same symbol name is defined multiple times with either a different type or a different size.

Your task has three parts:
1. Data Parsing & Transformation: Write a Python module `/home/user/symbol_parser.py` that parses a custom `nm`-like text format.
2. Property-Based Testing: Write a test suite `/home/user/test_symbol_parser.py` using `pytest` and the `hypothesis` library to ensure your parser is robust.
3. Integration & Analysis: Write a script `/home/user/analyze_symbols.py` that processes a provided dump file and outputs the conflicts into a specific JSON format.

### Input Data Format
The input file will be located at `/home/user/nm_output.txt`. 
Each line represents a symbol and has the following format (components are separated by one or more spaces):
`[Address] [Size] [Type] [SymbolName]`
- `Address`: A 16-character lowercase hex string (e.g., `0000000000001a2b`). Can be empty/missing if the symbol is undefined.
- `Size`: A 16-character lowercase hex string. Can be empty/missing.
- `Type`: A single character (e.g., `T`, `D`, `U`, `W`).
- `SymbolName`: A string containing only alphanumeric characters and underscores.

Example lines:
`0000000000001000 0000000000000040 T init_widget`
`                 U external_dep`
`0000000000002000 0000000000000010 D global_config`

### Requirements
1. **Parser Module (`/home/user/symbol_parser.py`)**:
   Implement a function `parse_line(line: str) -> dict`. It should return a dictionary with keys: `address` (str or None), `size` (int or None), `type` (str), and `name` (str). If a field is missing in the line, its value should be `None` (except for size, which should be converted to an integer if present).

2. **Property-Based Tests (`/home/user/test_symbol_parser.py`)**:
   Write tests using `hypothesis` and `pytest`. You must use `hypothesis.strategies` to generate random valid strings for `SymbolName` and hex strings for `Address`/`Size`, verifying that `parse_line` correctly extracts the `name` and parses the `size` back to an integer regardless of the number of spaces between columns. 

3. **Analysis Script (`/home/user/analyze_symbols.py`)**:
   Read `/home/user/nm_output.txt`. Find all symbol names that appear **more than once** where there is a mismatch in either the `size` or the `type` between the occurrences.
   Write the results to `/home/user/conflicts.json`. The JSON should be a dictionary where the key is the symbol name, and the value is a list of dictionaries representing the conflicting definitions.
   Format of `/home/user/conflicts.json`:
   ```json
   {
     "init_widget": [
       {"address": "0000000000001000", "size": 64, "type": "T", "name": "init_widget"},
       {"address": "0000000000003000", "size": 128, "type": "W", "name": "init_widget"}
     ]
   }
   ```
   (Sort the lists for each symbol by address, ascending).

Run your scripts, execute the tests with `pytest`, and ensure `/home/user/conflicts.json` is generated correctly.