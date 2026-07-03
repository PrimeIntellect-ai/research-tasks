You are an infrastructure engineer tasked with automating the provisioning of an email processing pipeline on a new server. We have a custom C utility that monitors storage limits and formats email headers, which currently resides at `/app/email_quota_monitor-1.2.0`. 

However, this vendored utility has a broken Makefile and is missing a critical patch to correctly parse the environment variable `QUOTA_WARN_LEVEL`. 

Your objectives are:
1. Fix the vendored package at `/app/email_quota_monitor-1.2.0` so that it builds correctly using `make` and correctly reads the `QUOTA_WARN_LEVEL` environment variable.
2. Build the package. The resulting binary should be located at `/app/email_quota_monitor-1.2.0/build/eqm_util`.
3. We need a secondary interactive script written in C that acts as a wrapper. Write a new C program at `/home/user/quota_wrapper.c` and compile it to `/home/user/quota_wrapper`. 
This wrapper must take inputs via standard input (one line at a time representing an email size in bytes) and output whether it exceeds a hardcoded limit of 1048576 bytes (1 MB). If it exceeds the limit, output "EXCEEDED"; otherwise, output "OK". The program should loop until EOF.

Ensure your wrapper exactly matches the behavior of our legacy oracle program for processing inputs.