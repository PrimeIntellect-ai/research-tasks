**URGENT: PAGERDUTY ALERT - 03:00 AM**

**Incident:** The risk calculation service is crashing with a fatal exception when querying Portfolio ID `9942`. 
**Context:** You are the on-call engineer. The developer who maintains this service just left the company and, according to the logs, accidentally deleted the source code during a supposed "cleanup" commit before handing over the system.

Your objectives:
1. Navigate to the local git repository at `/home/user/risk_engine`.
2. Recover the deleted C++ source file `calc.cpp` from the repository's history.
3. Analyze the algorithm inside `calc.cpp`. The program calculates a risk score by placing portfolio asset prices into a histogram. However, there is an algorithmic flaw in the bucket index formula that causes an out-of-bounds memory access (crashing the service) specifically when an asset hits the maximum expected price boundary.
4. Fix the formula implementation so that the maximum boundary values are properly clamped to the highest available bucket rather than exceeding the array bounds.
5. Compile your fixed code to a minimal executable at `/home/user/fixed_calc`.
6. Run your compiled executable against the failing portfolio ID: `/home/user/fixed_calc 9942`.
7. Save the exact console output of that command into `/home/user/solution.txt`.

You may use any standard shell tools and C++ compilers (like `g++`) available on the system.