You are an engineer tasked with building a highly optimized, polyglot analytics tool. The tool will parse millions of raw HTTP requests, extract specific routing parameters, sort them, and output the results. 

To achieve maximum performance for HTTP parsing, you must use the standard C `http-parser` library and link it into a newly created Rust application.

However, the vendored C library has a broken build system that you must fix first.

**Step 1: Fix the Vendored C Library**
The source code for `http-parser` (v2.9.4) is vendored at `/app/vendored/http-parser-2.9.4`. 
Currently, running `make library` fails due to compilation errors introduced by an outdated Makefile configuration on modern GCC.
1. Diagnose and fix the `Makefile` so that `make library` successfully produces `libhttp_parser.a`.
2. Generate a unified diff patch of your changes to the Makefile and save it to `/home/user/http-parser-makefile.patch`.

**Step 2: Polyglot Rust Setup**
Create a new Rust binary project at `/home/user/http_analytics`.
1. Configure a `build.rs` script to statically link the fixed `libhttp_parser.a` from the vendored directory.
2. Use Rust's FFI capabilities to interface with the C library (you will specifically need `http_parser_init` and `http_parser_execute`, along with the `http_parser_settings` struct to capture URLs).

**Step 3: Implementation**
Write the Rust application to accept two command-line arguments: an input log file path and an output file path.
`cargo run --release -- <input_file> <output_file>`

1. The input file (e.g., `/app/data/requests.log`) contains raw, unparsed HTTP/1.1 requests separated by a custom delimiter: `\r\n---REQUEST-BOUNDARY---\r\n`.
2. Use the linked C `http-parser` to parse each request. 
3. For each successfully parsed request, extract the URL.
4. Manually parse the URL's query string to find the `score` parameter (e.g., `/api/v1/data?user=123&score=85`). The score will always be a valid integer if present.
5. Filter out any requests that do not have a `score` parameter.
6. Sort the filtered URLs primarily by their `score` in **descending** order. If two URLs have the exact same score, sort them by the full URL string in **ascending** alphabetical order.
7. Write the sorted, full URLs (one per line) to the provided `<output_file>`.

**Step 4: Performance Goal**
Your application must be extremely fast. The automated verifier will compile your Rust code in `--release` mode and run it against a massive dataset at `/app/data/requests.log`. 
Your program must process the entire file and write the correct output to `/home/user/top_urls.txt` in **under 1.5 seconds**. Memory allocations should be minimized.