You are acting as a support engineer. We have received a bug report from a customer stating that our custom binary protocol parser crashes unexpectedly when processing certain corrupted packets. 

You have been provided with a Git repository located at `/home/user/parser_repo`. The repository contains the Python package for our parser, specifically `bin_parser.py`. 
You also have the malformed packet saved at `/home/user/crash_packet.bin`.

The parser used to handle malformed packets gracefully by simply returning the raw payload, but a recent feature addition caused a regression where it now throws an unhandled `struct.error` (similar to a buffer over-read).

Your tasks are:
1. **Reproduce & Automate:** Write a regression test script at `/home/user/test_regression.py`. This script should read `/home/user/crash_packet.bin`, pass it to `bin_parser.parse_packet()`, and exit with code 1 if it encounters the `struct.error` crash, or exit with code 0 if it completes successfully or raises a handled exception.
2. **Git Bisection:** Use `git bisect` (along with your regression test) in the `/home/user/parser_repo` directory to identify the exact commit that introduced the regression. 
3. **Report:** Save the full 40-character SHA-1 hash of the bad commit to `/home/user/bad_commit_hash.txt`.
4. **Fix the Bug:** Checkout the `main` branch (the latest commit). Modify `bin_parser.py` to fix the bug. The fix must ensure that if the payload for a packet of type `0x01` is too short to be unpacked as a 4-byte integer, the parser should explicitly raise a `MalformedPacketError` (which is already defined in the file) with the exact message `"Payload too short"`.

Do not modify the Git history; only commit your fix to the tip of `main` or leave it as an uncommitted modification on `main`.