You have been assigned to migrate a legacy Python 2 telemetry processing script to Python 3. The script processes a custom sensor data format using a basic state machine, calculates some numerical metrics, and outputs the results.

Currently, the script is broken under Python 3 due to several syntax, type, and standard library changes. It also has an unimplemented function for calculating statistics.

Here is the legacy Python 2 code. Please create this file at `/home/user/process_telemetry.py` and upgrade it to valid Python 3:

```python
import json

def parse_stream(filepath):
    # State machine: 0=WAIT_HEADER, 1=IN_DATA
    state = 0
    valid_frames = []
    current_frame = []
    
    with open(filepath, 'rb') as f:
        for line in f:
            line = line.strip()
            if state == 0:
                if line.startswith('HEAD'):
                    state = 1
                    current_frame = []
            elif state == 1:
                if line == 'END':
                    valid_frames.append(current_frame)
                    state = 0
                elif line.startswith('HEAD'):
                    # Corrupted frame, reset
                    current_frame = []
                else:
                    # Parse hex values separated by space
                    try:
                        vals = map(lambda x: int(x, 16), line.split(' '))
                        current_frame.extend(vals)
                    except Exception, e:
                        print "Error parsing line:", e
                        state = 0
    return valid_frames

def calculate_metrics(frame):
    # TODO: Implement calculation of the mean and population variance for the given frame (list of ints).
    # Return a dictionary: {"mean": <float>, "variance": <float>}
    # If the frame is empty, return {"mean": 0.0, "variance": 0.0}
    pass

def main():
    frames = parse_stream('/home/user/telemetry.dat')
    results = []
    for i in xrange(len(frames)):
        metrics = calculate_metrics(frames[i])
        results.append({"frame_id": i, "metrics": metrics})
    
    with open('/home/user/results.json', 'w') as out:
        json.dump(results, out)

if __name__ == '__main__':
    main()
```

Your tasks are:
1. Create the file `/home/user/telemetry.dat` with the following content:
```
HEAD
0A 14 1E
05 0F
END
HEAD
FF 00
ERROR_LINE
END
HEAD
02 04 06 08
END
```
2. Save the upgraded Python 3 script to `/home/user/process_telemetry.py`.
3. Fix all Python 2 incompatibilities (e.g., `xrange`, `except Exception, e:`, bytes vs string handling when reading files, and `map` return types if used in lists).
4. Implement the `calculate_metrics` function to compute the arithmetic mean and the **population variance** of the integers in the frame. Do not use external libraries like `numpy` or `pandas`—use only standard built-in Python modules.
5. Run the script so that it generates `/home/user/results.json`.

The final output file `/home/user/results.json` should contain the computed metrics for all successfully parsed frames.