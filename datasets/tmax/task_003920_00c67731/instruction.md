I need you to help me organize and process a set of legacy project data files. These files are currently in an older encoding and take up too much space. I want you to write a Go program that processes them concurrently, applies a custom compression algorithm, and generates a manifest.

Here is the precise workflow and requirements for your Go program:

1. **Input Location**: Read all `.dat` files located in `/home/user/project_data/raw/`. 
2. **Encoding Conversion**: The input files are encoded in `ISO-8859-1`. You must read them and convert their contents to `UTF-8`.
3. **Custom Compression (Run-Length Encoding)**: Apply a custom RLE algorithm to the UTF-8 text. Specifically, replace any sequence of 3 or more identical consecutive characters with the character followed by `*` and the count. 
   - Example: `Hellooo Wörld!!!` becomes `Hel*3o Wörld!*3`.
   - Example: `AAbbcccc` becomes `AAbbc*4`.
4. **Atomic Writes**: Save the compressed output to `/home/user/project_data/processed/` with the extension `.rle` (e.g., `data1.dat` becomes `data1.rle`). To ensure no partial files are ever visible, you MUST write the output to a temporary file first (e.g., `.tmp`) and then atomically rename it to the final `.rle` file.
5. **Concurrent Logging and File Locking**: Process the files concurrently using Go routines. As each file finishes, append a log entry to `/home/user/project_data/process.log` in the format: `PROCESSED: [filename.rle]`. Because goroutines will write to this file concurrently, you must use proper OS-level file locking (e.g., `syscall.Flock`) to ensure the log entries are not corrupted or interleaved.
6. **Manifest Generation**: After all files are processed, generate a manifest file at `/home/user/project_data/manifest.txt`. Each line should contain the name of the processed file and its SHA256 checksum (in hex), separated by a double space (mimicking `sha256sum` output). Sort the manifest alphabetically by filename.
   - Format: `[sha256_hash]  [filename.rle]`

Please write, compile, and execute this Go program to process the directory.

You will need to install any necessary Go packages for text encoding (e.g., `golang.org/x/text/encoding/charmap`).