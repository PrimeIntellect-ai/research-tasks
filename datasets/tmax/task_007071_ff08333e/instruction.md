You are an on-call engineer responding to a critical 3AM page. The production `packet_decoder` service has started crashing with a Segmentation Fault immediately after the latest deployment. 

The service processes binary packet dumps. It worked perfectly in the `v1.0` release, but something introduced in the recent commits has completely broken it.

Your objectives:
1. Navigate to the local repository at `/home/user/packet_decoder`.
2. Use `git bisect` (or manual binary searching) to identify the exact commit hash that introduced the segmentation fault. The known good commit is tagged `v1.0`, and the current broken state is `HEAD`.
3. Save the full 40-character SHA-1 hash of the bad commit to `/home/user/bad_commit.txt`.
4. Use `gdb` to analyze the core dump or the live execution of the program to find the root cause of the crash. 
5. The bug is an off-by-one boundary condition in the packet decoding logic. Fix the C code so it correctly processes the packets without overflowing buffers.
6. Compile your fixed version using `make`.
7. Run the fixed executable on the provided production data dump: `./packet_decoder /home/user/prod_dump.dat > /home/user/fixed_output.txt`.

System Context:
* Repository: `/home/user/packet_decoder`
* Production data: `/home/user/prod_dump.dat`

The automated verification will check:
- The correctness of the commit hash in `/home/user/bad_commit.txt`.
- The exact decoded text output in `/home/user/fixed_output.txt`.