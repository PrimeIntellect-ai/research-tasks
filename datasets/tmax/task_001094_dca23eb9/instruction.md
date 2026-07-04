You are tasked with debugging a floating-point regression in a distance calculation service. 

A repository located at `/home/user/geo_service` contains a Python script `calc.py` that calculates the Haversine distance between two sets of coordinates. We know that a floating-point precision error was introduced into the formula implementation recently, but we are not sure which commit caused it. There are 200 commits in the repository.

The specific test case that fails was accidentally deleted from the test suite. However, we have a network packet capture `/home/user/traffic.pcap` taken when the service was functioning correctly. The capture contains a single TCP HTTP POST request to the service with a JSON payload of the coordinates, followed by the HTTP response containing the exact, highly precise calculated distance.

Your objectives:
1. Analyze `/home/user/traffic.pcap` to extract the original test coordinates and the correct expected distance.
2. Use `git bisect` (or a custom script) across the repository to find the exact commit hash that introduced the precision regression for this specific test case.
3. Write the full 40-character Git commit hash of the **first bad commit** to a file named `/home/user/bad_commit.txt`.
4. Fix the formula implementation in `calc.py` on the `main` branch to restore full floating-point precision so that it exactly matches the expected distance from the packet capture. Leave the corrected file at `/home/user/geo_service/calc.py`.

Ensure your fix doesn't just hardcode the answer, but completely repairs the formula's precision logic.