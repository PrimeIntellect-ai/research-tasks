You are helping a technical writer process a large legacy documentation repository. The writer frequently receives raw documentation files where embedded code snippets and binary references have been stripped and replaced with Base64 encoded blocks wrapped in specific custom tags.

Your task is to write a C++ command-line utility that decodes these blocks on the fly so the technical writer can pipe their documents through it to restore the original content.

Requirements:
1. **Fix the Base64 Library:** We are providing a vendored copy of `libb64` (version 1.2.1) in `/app/libb64-1.2.1`. However, the technical writer accidentally broke its build system while trying to modify it. You must find the syntax error or typo in its `src/Makefile`, fix it, and compile the library so you can link against it.
2. **Write the Decoder (`/home/user/doc_extractor.cpp`):**
   - The program must read the entirety of standard input (`stdin`) until EOF.
   - It must look for exact literal tags: `[B64]` and `[/B64]`.
   - Any text outside of these tags must be printed to `stdout` exactly as-is.
   - Any text strictly between a `[B64]` and the next `[/B64]` tag must be treated as Base64. You must use the vendored `libb64` library to decode this Base64 string, and print the decoded plaintext to `stdout`.
   - You can assume the tags are never nested.
3. **Compilation:** Compile your program to an executable named `/home/user/doc_extractor`. Ensure it statically or dynamically links to the fixed `libb64` properly.

Example:
If standard input contains:
`Here is the configuration: [B64]c2VydmVyX3BvcnQ9ODA4MA==[/B64] End of doc.`
Your program must output:
`Here is the configuration: server_port=8080 End of doc.`

Do not add any trailing newlines unless they exist in the input. Write efficient code, as this will be used on multi-gigabyte text streams.