Hello, I'm an MLOps engineer setting up an automated artifact tracking pipeline. We have a Python script that processes experiment data and generates a visualization, but it is currently producing an empty/blank plot due to a misconfiguration in how the plot is saved.

Additionally, we need a standard shell script to archive these generated artifacts for large-scale storage.

Here is what you need to do:
1. Fix the Python script located at `/home/user/mlops/generate_artifact.py` so that it correctly saves the matplotlib plot to `/home/user/mlops/output/result.png` without it being blank. (Do not change the data being plotted or the output path).
2. Create a bash script at `/home/user/mlops/archive.sh`. This script should:
   - Make sure the directory `/home/user/archive/` exists.
   - Create a tarball named `/home/user/archive/artifacts.tar.gz` containing all `.png` files located inside `/home/user/mlops/output/`. The archived files should not contain absolute paths (i.e., when extracting the tarball, it should extract the files directly or within an `output` directory, but not the full `/home/user/...` hierarchy).
   
Make sure both the Python script and the bash script are executable. Run the Python script, then run your bash script to ensure `/home/user/archive/artifacts.tar.gz` is successfully created.