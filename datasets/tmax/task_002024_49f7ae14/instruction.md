You are helping a team migrate a massive legacy system from Python 2 to Python 3. During the audit, the team discovered a set of serialized business rules in a custom binary format (`/home/user/legacy_rules.bin`). These rules contain compiled operations that resemble a simplistic Python bytecode. 

Your task is to write a Go program (`/home/user/analyzer.go`) that parses this binary file, performs assembly-level analysis on the embedded bytecode, and identifies which rules contain Python 2-specific operations so they can be manually migrated.

### Binary File Specification
The file `/home/user/legacy_rules.bin` uses Little-Endian byte order for all multi-byte integers.

**Header:**
- Magic Number: 4 bytes (ASCII "PY2B")
- Version: `uint16`

**Records:**
- Rule Count: `uint32`
- Followed by exactly `Rule Count` records. Each record consists of:
  - ID: `uint32`
  - NameLength: `uint8`
  - Name: string of length `NameLength`
  - CodeLength: `uint32`
  - Code: Byte array of length `CodeLength` containing the custom bytecode.

### Bytecode Instruction Set
The `Code` section contains a sequence of instructions. You must step through the bytecode correctly to avoid reading instruction operands as opcodes.
- `0x01` (`LOAD_CONST`): Takes a **2-byte** operand immediately following the opcode.
- `0x02` (`PRINT_ITEM`): Python 2 specific. Takes **0** operands.
- `0x03` (`PRINT_NEWLINE`): Python 2 specific. Takes **0** operands.
- `0x04` (`CALL_FUNCTION`): Takes a **2-byte** operand immediately following the opcode.
- `0x05` (`BINARY_DIVIDE`): Python 2 specific (classic division). Takes **0** operands.

### Task Requirements
1. Design custom Go structs to parse and hold the structured binary data.
2. Read and parse `/home/user/legacy_rules.bin`.
3. Iterate sequentially through the `Code` bytes of each rule. You must properly advance your instruction pointer based on whether the current opcode takes an operand.
4. If a rule's code contains `0x02`, `0x03`, or `0x05`, it needs migration. 
5. Output the results to `/home/user/migration_report.json`.

### Output Format (`/home/user/migration_report.json`)
Produce a JSON file with the following exact structure. `violating_opcodes` should be a list of the unique Python 2 specific opcodes (2, 3, or 5) found in that rule, sorted in ascending numeric order.

```json
{
  "rules_to_migrate": [
    {
      "id": 101,
      "name": "rule_b",
      "violating_opcodes": [2, 3]
    }
  ]
}
```

Write the Go code, compile it, and run it to produce the JSON file. Ensure you format the JSON cleanly (e.g., using `json.MarshalIndent`).