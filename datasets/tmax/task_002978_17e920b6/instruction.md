You have been assigned to audit the permissions and authentication logs for our legacy internal data processing system. 

First, navigate to `/app/vendored/auth_parser-1.2.0`, which is a vendored third-party Python package used internally to parse authentication tokens and access control lists. The package is currently broken due to a recent bad patch applied by our internal team, which causes it to fail when processing valid nested group structures in tokens. Your task is to find the syntax or logic error introduced in `auth_parser/core.py`, fix it, and verify that the package's test suite passes (`python3 -m unittest discover`).

Next, examine the access log located at `/home/user/audit_logs/access.log`. One of the administrative users used a very weak password that has been logged as an MD5 hash. Extract the hash, crack it (the password is a 5-letter lowercase English word), and append the cracked password to `/home/user/audit_logs/cracked_pass.txt`.

Finally, we need to replace our old permission evaluation binary with a custom script. We have provided a reference oracle binary at `/opt/oracle/perm_eval_oracle`. You must write a script (in any language) that takes exactly two arguments: a path to a file containing a raw byte stream of user attributes, and a path to a file containing binary resource ACLs. Your script must output a binary stream representing the exact evaluated access flags (allow/deny bytes) just like the oracle. 
Save your script to `/home/user/evaluator_agent`, make it executable, and ensure it exactly matches the oracle's output for any arbitrary input byte combinations.

For verification, ensure:
1. The `auth_parser` module works and passes its tests.
2. The cracked password file exists.
3. Your script at `/home/user/evaluator_agent` is an exact bit-for-bit functional equivalent to `/opt/oracle/perm_eval_oracle`.