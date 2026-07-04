You are an IT support technician responding to an escalated ticket from the Data Science team. 

**Ticket Details:**
"Hi IT, we have a legacy Bash pipeline that computes an approximation of Pi using the Gregory-Leibniz series. It used to work, but we recently moved it to a new server and now it's completely broken. 

When we try to run `/home/user/calc_pi.sh`, it fails to build its C helper program, it can't read its configuration file properly, and even when we tried to manually bypass those issues, the math just blew up and failed to converge to anything near 3.14. 

Please fix `/home/user/calc_pi.sh` so that it successfully runs from start to finish. The script should read the iterations from the configuration, build the helper, compute the series, and finally write the approximated value of Pi to `/home/user/pi_result.txt`."

**Your Objectives:**
1. Investigate and fix the file encoding/serialization issue preventing the script from reading the target iterations.
2. Fix the compiler/linker error so the C helper program builds successfully.
3. Fix the mathematical logic inside the Bash script so the series properly converges (it currently fails to alternate signs for the series).
4. Run the fixed `/home/user/calc_pi.sh` script.

**Success Criteria:**
- The script `/home/user/calc_pi.sh` must execute without errors.
- The correct approximated value of Pi must be written to `/home/user/pi_result.txt`.