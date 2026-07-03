You are an engineer responsible for maintaining a lightweight Git-based deployment pipeline. 

We have a local bare Git repository at `/home/user/deploy.git` that acts as our production remote. When developers push to this repository, a `post-receive` hook is supposed to check out the code to `/home/user/app` and start the application service by executing `/home/user/app/start-service.sh`.

However, the deployment is currently failing. If you navigate to our source repository at `/home/user/app-src` and attempt to run `git push deploy master`, the push is rejected because the hook fails to start the service. The service has strict requirements regarding its execution environment (specifically relating to timezones and locales to ensure consistent log formatting), and the current hook does not handle errors or environment configuration correctly.

Your task:
1. Diagnose why the `post-receive` hook in `/home/user/deploy.git/hooks/post-receive` is failing.
2. Fix the deployment process. You may modify the `post-receive` hook to properly configure the environment before invoking the service script.
3. Ensure the environment variables `TZ` is set to `UTC` and `LC_ALL` is set to `C.UTF-8` for the service script execution.
4. Ensure that the deployment gracefully handles errors (robust script writing).
5. Once fixed, execute the push successfully from `/home/user/app-src` via `git push deploy master`.

Verification:
An automated test will check that:
- The `git push deploy master` command completes successfully.
- The service successfully writes its startup status to `/home/user/app.log`, which should contain the exact word `READY`.