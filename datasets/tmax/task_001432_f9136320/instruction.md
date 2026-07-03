You are an on-call engineer who just got paged at 3 AM. A critical internal service called `watermark-extractor` is failing in production. The service is supposed to read a base configuration from a physical watermark embedded in an image, parse incoming binary requests, and output validated telemetry. 

However, metrics show the service is occasionally getting stuck in infinite loops, crashing on specific edge cases in format parsing, and failing to correctly apply the watermark configuration. The previous engineer left a diagnostic image of the watermark at `/app/watermark_config.png` but didn't document what it says. 

Your tasks are to:
1. Extract the text from the image at `/app/watermark_config.png` (using OCR tools like `tesseract` which are preinstalled) to find the master offset value used by the parsing logic.
2. Investigate the `watermark-extractor` service source code located at `/home/user/service/` (which contains a mix of Python and C components). Trace its system calls to understand why it hangs on certain inputs.
3. Fix the boundary conditions (there is an off-by-one error in the C extension) and the format parsing edge cases (in the Python script) that cause the infinite loop and crashes.
4. Compile and configure the fixed service to output exactly the expected telemetry format. Write a wrapper script at `/home/user/run_extractor.sh` that takes a binary input file as its first argument and outputs the parsed telemetry to stdout. 

The fixed `/home/user/run_extractor.sh` must be robust and produce bit-exact equivalent output to our reference implementation for all possible inputs.