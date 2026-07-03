You are the release manager for a quantitative trading firm. You are preparing the deployment of a new ultra-low-latency math expression evaluator, "MathScript", which is embedded in the trading pipeline. 

Currently, the MathScript engine is in a broken state. The previous developer left the codebase with memory leaks, undefined behavior (UB), and no build system. Furthermore, it is highly vulnerable to malformed or malicious math expressions that cause crashes (segfaults or floating-point exceptions).

Your tasks are:

1. **Extract Release Parameters:**
   There is an image file at `/app/release_spec.png` containing the release notes for this version. Use OCR tools (e.g., `tesseract`) to read the image. You must find the explicit maximum allowed Abstract Syntax Tree (AST) depth parameter (e.g., `MAX_AST_DEPTH=XX`).

2. **Fix and Build the Engine:**
   The source code for the interpreter is in `/app/src/`. 
   - Fix all memory leaks and undefined behaviors (such as missing bounds checks or unchecked divisions). 
   - Create a `CMakeLists.txt` in `/app/src/` to compile the C++ code into an executable named `mathscript`. 
   - Build the project in the `/app/build/` directory. You must link standard libraries appropriately.

3. **Implement an Adversarial Filter:**
   Modify the `mathscript` CLI to support a `verify` mode. When invoked as `/app/build/mathscript verify <path_to_expr_file>`, the engine must NOT evaluate the expression. Instead, it must parse it and act as a sanitizer/classifier:
   - Print "SAFE" to standard output and exit with code `0` if the expression is perfectly safe.
   - Print "UNSAFE" to standard output and exit with code `1` if the expression contains:
     - Division by zero (e.g., `x / 0` or mathematically guaranteed zero divisors in constant expressions).
     - AST nesting that exceeds the `MAX_AST_DEPTH` extracted from the image.
     - Syntax errors, incomplete expressions, or unrecognized tokens.
   
4. **Validation:**
   There are two corpora of MathScript files provided:
   - `/app/corpus/clean/`: Contains 50 safe, well-formed expression files.
   - `/app/corpus/evil/`: Contains 50 malicious or malformed expression files designed to trigger UB, stack overflows (via deep nesting), or arithmetic exceptions.
   Your compiled `/app/build/mathscript` will be automatically tested against both corpora. It must successfully accept 100% of the clean files and reject 100% of the evil files.