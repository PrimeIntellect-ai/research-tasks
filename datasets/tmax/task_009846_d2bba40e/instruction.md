You are an on-call engineer and have just received a 3 AM PagerDuty alert. The internal Forensics Audit Service has gone down after an automated configuration merge. The pipeline is broken, the service won't compile, and incident responders are complaining that the recent audit query results look completely corrupted.

You need to investigate and fix the code in `/home/user/forensic_service`.

Here is the situation:
1. **Compilation Failure**: The project currently fails to compile due to an interface implementation mismatch introduced in the recent merge. You must interpret the compiler errors and fix the signature mismatch between the `AuditStore` interface and the SQLite implementation.
2. **Query Result Debugging**: Even after it compiles, the `GetCriticalEvents()` function is returning corrupted data. The incident responders noticed that the `Action` and `Username` fields seem to contain incorrect or swapped data. Diagnose the SQL query and the row scanning logic, and fix the bug so the data maps correctly to the Go structs.
3. **Regression Test Construction**: To prevent this from happening again, you must write a regression test. Create a file at `/home/user/forensic_service/db/db_test.go`.
   - The test function must be named `TestGetCriticalEvents`.
   - It should instantiate an in-memory SQLite database (`:memory:`).
   - It should create the `events` table (using the schema found in the code).
   - It should insert the following three records:
     - ID: 1, Username: "alice", Action: "LOGIN", Severity: 1
     - ID: 2, Username: "bob", Action: "UNAUTHORIZED_ACCESS", Severity: 5
     - ID: 3, Username: "eve", Action: "DATA_EXFILTRATION", Severity: 5
   - It should call `GetCriticalEvents()` (which fetches Severity >= 5).
   - It must use assertion-based validation to verify that exactly 2 records are returned, and that the first record's `Username` is "bob" and `Action` is "UNAUTHORIZED_ACCESS". If the assertions fail, the test must fail (`t.Errorf` or `t.Fatalf`).
4. **Fix Report**: Finally, run your test. Once the test passes, write a report to `/home/user/forensic_service/fix_report.log` with the exact following format:
```
STATUS: FIXED
COMPILER_ISSUE_ROOT_CAUSE: <1-2 sentences explaining the interface mismatch>
QUERY_ISSUE_ROOT_CAUSE: <1-2 sentences explaining the scanning bug>
TEST_PASSED: TRUE
```

**Constraints:**
- Do not change the struct definition of `Event` in the `models` package.
- Ensure all your code compiles and passes the standard `go test ./...` command.
- The project is located at `/home/user/forensic_service`.