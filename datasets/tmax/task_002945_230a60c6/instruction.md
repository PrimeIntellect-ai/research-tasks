You have inherited an unfamiliar, undocumented tool located in `/home/user/project`. 

The tool is supposed to read all text files from `/home/user/data`, process them, and print their contents prefixed with the file name. However, the previous developer left it in a broken state. 

When you run the wrapper script `/home/user/project/run_all.sh`, it hangs indefinitely or crashes with a segmentation fault. 

Your tasks are:
1. Diagnose and fix the shell script (`/home/user/project/run_all.sh`) which currently fails to properly handle filenames with spaces.
2. Diagnose and fix the C++ program (`/home/user/project/processor.cpp`). It currently contains an infinite recursion bug when it fails to open a file. Fix it so that it stops retrying after 3 failed attempts (i.e., if `retries == 3`, it should print "Error: Could not read <filename>" to standard error and return).
3. Recompile the C++ program: `g++ processor.cpp -o processor`
4. Run `./run_all.sh` and redirect its standard output to `/home/user/success.log`. 

Ensure that `/home/user/success.log` contains the successfully processed contents of all files in `/home/user/data`, and that the program terminates cleanly without infinite loops or segfaults.