**URGENT: 3AM PAGE - PRODUCTION INCIDENT**

You are the on-call systems engineer. It's 3:00 AM, and our core network inspection service is intermittently locking up and exhausting CPU/memory. Operations has mitigated the issue temporarily by restarting the service every 5 minutes, but we need a permanent fix immediately. 

Here is what we know:
1. The service uses a vendored version of the `dpkt` library for packet parsing, located at `/app/dpkt-1.9.8`. 
2. The lockups seem to occur when the service processes specific, rarely seen network packets. A recent system update modified our vendored `dpkt` package to "optimize" parsing of certain TCP options, but we suspect it introduced an off-by-one boundary condition that causes an infinite loop or buffer mismanagement under specific cancellation or truncation conditions.
3. Operations has provided a network packet capture from the time of the crashes: `/home/user/incident_capture.pcap`.

**Your objectives:**

**Phase 1: Diagnosis & Repair**
Analyze the provided `/home/user/incident_capture.pcap` to identify the malformed packet(s) causing the intermittent failure. You will need to inspect the vendored `dpkt` source code at `/app/dpkt-1.9.8` to find the root cause of the hang. Fix the parsing logic (specifically, look for a boundary condition or off-by-one error in how it handles malformed or truncated packet lengths/offsets) so that the library safely raises an exception or skips the packet rather than hanging.

**Phase 2: Exploit Detection**
Security needs to know if this was a targeted attack. Once you understand the structure of the "poison" packet, you must write a standalone Python detection script at `/home/user/detector.py`. 

Your script must conform exactly to this interface:
* It must be executable via: `python3 /home/user/detector.py <path_to_pcap_file>`
* It must print EXACTLY the string `EVIL` to standard output if the pcap contains one or more packets designed to trigger the boundary condition.
* It must print EXACTLY the string `CLEAN` to standard output if the pcap does not contain any such packets.
* It must exit with code 0 in both successful analysis cases.

Your solution will be tested against a hidden suite of clean and malicious pcap files to ensure it correctly identifies 100% of the malicious files without any false positives. Fix the vendored package and create the detector script to resolve the incident.