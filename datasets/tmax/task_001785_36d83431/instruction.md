You are a Linux systems engineer investigating performance issues with a local SMTP relay service. 

We use a vendored version of the `aiosmtpd` Python package, located at `/app/aiosmtpd`, to process incoming notification emails. A wrapper script at `/app/run_server.py` starts the server on `127.0.0.1:8025`.

Recently, developers have complained that the SMTP server is unacceptably slow, causing upstream applications to block or timeout when sending alerts. An engineer suspects some stray debug code or a poorly configured sleep/timeout was accidentally committed into the vendored package's source code handling the SMTP transaction.

Your tasks are to:
1. Start the server (`python3 /app/run_server.py &`) and diagnose the slow connectivity. 
2. Locate and fix the performance bug within the vendored `/app/aiosmtpd` package. 
3. Write a robust Python diagnostic script at `/home/user/stress_test.py` that sequentially connects to `127.0.0.1:8025` and sends 50 test emails. 
   - Envelope sender: `test@example.com`
   - Envelope recipient: `dest@example.com`
   - Message Subject: `Test`
   - Message Body: `This is a test`
4. `/home/user/stress_test.py` must measure the time it takes to send all 50 emails and print the result to stdout exactly in this format: `Total time: X.XXX seconds`

You have succeeded if the bug is patched and your stress test script successfully delivers all 50 emails in under 2.0 seconds total time.