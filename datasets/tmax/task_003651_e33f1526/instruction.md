You are assisting a compliance officer who is auditing an enterprise network for unauthorized data exfiltration paths. 

A proprietary firewall rules export has been provided at `/home/user/audit/fw_export.dat`. The system administrators did not provide the schema for this file, but we know it contains rules detailing allowed connections between various internal and external hosts, along with other metadata like protocols, ports, and rule IDs.

Your tasks are:

1. **Reverse Engineer the Data Model:** Inspect `/home/user/audit/fw_export.dat` and deduce its structure. Identify which fields correspond to the Source Host and Destination Host.
2. **Shortest Path Computation:** We suspect there is a critical compliance violation allowing transitive data flow from the `SecurePaymentGateway` to the `PublicInternet`. Representing the allowed connections as a directed graph, find the shortest path (minimum number of hops) from `SecurePaymentGateway` to `PublicInternet`. 
3. **Format Output:** You must output your findings to `/home/user/audit/compliance_report.txt`. The output must strictly follow this exact format:

```
SCHEMA:
Field1: <Name of inferred field 1>
Field2: <Name of inferred field 2>
...
FieldN: <Name of inferred field N>

VIOLATION PATH:
<Node1> -> <Node2> -> ... -> <NodeN>
```
*Note: Use logical names for the schema fields based on the data (e.g., Source_Host, Destination_Host, Protocol, Port, Rule_ID).*

**Constraints:**
- You must use Bash and standard Linux CLI tools (like `awk`, `grep`, `sed`, `bash`) to process the data and find the path. Python, Perl, or other high-level scripting languages are strictly forbidden.
- The path must be the shortest possible path. If there are multiple paths of the same shortest length, output any one of them.