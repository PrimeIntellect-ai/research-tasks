You are a script developer tasked with creating a distributed utility that analyzes the complexity of x86 assembly snippets. You will build a gRPC service in Python that parses minimal assembly, computes an "Instruction Execution Cost" (IEC) using a specific numerical algorithm and state machine, and a client that queries this service.

### Step 1: Create the gRPC Protobuf Definition
Create a file at `/home/user/analyzer.proto` with the following specifications:
- Syntax: proto3
- Package: `asm_analyzer`
- Service: `AssemblyAnalyzer`
- RPC Method: `AnalyzeSnippet` which takes a `SnippetRequest` and returns a `SnippetResponse`.
- `SnippetRequest` message: contains a single string field `code` (field number 1).
- `SnippetResponse` message: contains a single float field `score` (field number 1).

Compile this protobuf file for Python using `grpcio-tools`. The generated files should be placed in `/home/user/`.

### Step 2: Implement the gRPC Server
Create a server script at `/home/user/server.py` that implements the `AssemblyAnalyzer` service and listens on port `50051`. 
The `AnalyzeSnippet` method must calculate the IEC score based on the following rules:

**Parsing Rules (State Machine):**
1. Process the assembly code line by line.
2. Strip leading/trailing whitespace. Ignore empty lines and lines that start with `;`.
3. If a line contains a `;`, treat everything after and including the `;` as a comment and remove it before processing.
4. A label definition is a line that ends with a colon `:` (e.g., `loop_start:`). Keep track of all label names (without the colon) and the line number (or order) they were encountered.
5. An instruction is the first word on a line (case-insensitive) that is not a label definition.
6. The first operand (if any) is the second word on the line (ignoring commas).

**Numerical Cost Algorithm:**
1. Base Cost is initially 0.
2. For each parsed instruction, add to the Base Cost based on the mnemonic:
   - `mov`, `push`, `pop`: +1
   - `add`, `sub`, `inc`, `dec`, `cmp`: +2
   - `jmp`, `je`, `jne`, `jz`, `jnz`: +3
   - `mul`, `div`: +4
   - `call`, `ret`: +5
   - Any other instruction: +0
   - Label definitions: +0
3. **Backward Jump Penalty:** Count the number of backward jumps, let's call this `N`. A backward jump is defined as any jump instruction (`jmp`, `je`, `jne`, `jz`, `jnz`) whose first operand exactly matches a label name that was defined on an *earlier* valid line in the code.
4. Final Score = Base Cost * (1.5 ^ N).

### Step 3: Implement the Client
Create a client script at `/home/user/client.py`. The client must:
1. Connect to the server at `localhost:50051`.
2. Read all `.asm` files in the directory `/home/user/snippets/` (you should process them in alphabetical order by filename).
3. Send the contents of each file to the server using the `AnalyzeSnippet` RPC.
4. Write the results to `/home/user/results.log`.

**Output Format for `/home/user/results.log`:**
For each file, write a line in the exact format:
`<filename>: <score rounded to 2 decimal places>`

### Setup Instructions
You will need to create the snippets directory and the assembly files to test your client.
Create `/home/user/snippets/1_linear.asm`:
```assembly
mov eax, 1
add eax, 5
ret
```

Create `/home/user/snippets/2_forward.asm`:
```assembly
mov eax, 0
cmp eax, 10
je end
add eax, 1
end:
ret
```

Create `/home/user/snippets/3_loop.asm`:
```assembly
mov eax, 0
loop_start:
add eax, 1
cmp eax, 10
jne loop_start
ret
```

Ensure the server can run continuously in the background while the client executes. Finally, run your server and then your client to generate the `results.log` file.