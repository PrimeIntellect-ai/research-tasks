You are tasked with fixing and organizing a custom URL routing engine written in C. The project is located at `/home/user/url_router/`. 

Currently, the project is a mess:
1. The `Makefile` is broken and fails to link the object files correctly.
2. There is a circular dependency between `router.h` and `parser.h` that prevents compilation.
3. The parameter parsing logic in `parser.c` has a pointer arithmetic bug that causes a segfault when parsing URL constraints (e.g., when trying to enforce parameter length limits).

Your objective:
1. Fix the C code and the Makefile so that it successfully builds the executable at `/home/user/url_router/router_bin`.
2. Find the correct constraint modulus. The parser relies on a specific `CONSTRAINT_MODULUS` macro defined in `parser.h`. The current value is wrong. To find the correct value, you must analyze the video file located at `/app/signal.mp4`. This video contains exactly 100 frames. Some frames are pure red (RGB 255,0,0), while others are black. Count the total number of red frames. The correct `CONSTRAINT_MODULUS` is calculated as: `(RED_FRAME_COUNT * 17) % 255`. Update `parser.h` with this value.
3. Ensure your fixed executable behaves *exactly* like the reference binary provided at `/app/oracle_router`. The executable takes a single argument (the URL path) and prints the routed ID and parsed variables to stdout.

The system will run automated tests feeding thousands of randomized URLs to your `/home/user/url_router/router_bin` and comparing its stdout/exit codes to `/app/oracle_router`.