apt-get update && apt-get install -y python3 python3-pip python3-dev build-essential
    pip3 install --default-timeout=100 pytest numpy

    mkdir -p /home/user/audio_pipeline/c_ext
    mkdir -p /app

    # Create C extension with intentional bug
    cat << 'EOF' > /home/user/audio_pipeline/c_ext/audio_filter.c
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <Python.h>
#include <numpy/arrayobject.h>

static PyObject* apply_filter(PyObject* self, PyObject* args) {
    PyArrayObject *input_array;
    PyArrayObject *filter_array;
    if (!PyArg_ParseTuple(args, "O!O!", &PyArray_Type, &input_array, &PyArray_Type, &filter_array)) {
        return NULL;
    }
    int num_samples = PyArray_DIM(input_array, 0);
    int filter_len = PyArray_DIM(filter_array, 0);

    float *input = (float*)PyArray_DATA(input_array);
    float *filter = (float*)PyArray_DATA(filter_array);

    npy_intp dims[1] = {num_samples};
    PyArrayObject *output_array = (PyArrayObject*)PyArray_SimpleNew(1, dims, NPY_FLOAT32);
    float *output = (float*)PyArray_DATA(output_array);

    for (int i = 0; i < num_samples; i++) {
        float sum = 0.0;
        for (int j = 0; j < filter_len; j++) {
            // BUG: i - j can be negative, reading before input array
            sum += input[i - j] * filter[j];
        }
        output[i] = sum;
    }

    return Py_BuildValue("O", output_array);
}

static PyMethodDef AudioFilterMethods[] = {
    {"apply_filter", apply_filter, METH_VARARGS, "Apply FIR filter."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef audiofiltermodule = {
    PyModuleDef_HEAD_INIT,
    "audio_filter",
    NULL,
    -1,
    AudioFilterMethods
};

PyMODINIT_FUNC PyInit_audio_filter(void) {
    import_array();
    return PyModule_Create(&audiofiltermodule);
}
EOF

    # Create setup.py
    cat << 'EOF' > /home/user/audio_pipeline/setup.py
from setuptools import setup, Extension
import numpy as np

module1 = Extension('audio_filter',
                    sources = ['c_ext/audio_filter.c'],
                    include_dirs=[np.get_include()])

setup(name = 'AudioFilter',
      version = '1.0',
      description = 'Audio Filter Extension',
      ext_modules = [module1])
EOF

    # Create Python 2 process script
    cat << 'EOF' > /home/user/audio_pipeline/process.py
import wave
import struct
import numpy as np
import audio_filter
import sqlite3

def process_audio(input_file, output_file):
    print "Processing file:", input_file
    wf = wave.open(input_file, 'rb')
    frames = wf.readframes(wf.getnframes())
    wf.close()

    input_signal = np.frombuffer(frames, dtype=np.int16).astype(np.float32)
    filter_coeffs = np.array([0.1, 0.2, 0.4, 0.2, 0.1], dtype=np.float32)

    output_signal = audio_filter.apply_filter(input_signal, filter_coeffs)

    output_signal = np.clip(output_signal, -32768, 32767).astype(np.int16)

    out_wf = wave.open(output_file, 'wb')
    out_wf.setnchannels(1)
    out_wf.setsampwidth(2)
    out_wf.setframerate(44100)
    out_wf.writeframes(output_signal.tobytes())
    out_wf.close()
    print "Done processing."

if __name__ == '__main__':
    process_audio('/app/test_signal.wav', '/home/user/output_signal.wav')
EOF

    # Generate initial data using a temporary python script
    cat << 'EOF' > /tmp/setup_data.py
import wave
import numpy as np
import sqlite3

# Generate test_signal.wav
signal = np.sin(2 * np.pi * 440 * np.linspace(0, 1, 44100)) * 10000
signal = signal.astype(np.int16)

wf = wave.open('/app/test_signal.wav', 'wb')
wf.setnchannels(1)
wf.setsampwidth(2)
wf.setframerate(44100)
wf.writeframes(signal.tobytes())
wf.close()

# Generate records.db
conn = sqlite3.connect('/home/user/audio_pipeline/records.db')
c = conn.cursor()
c.execute('CREATE TABLE audio_records (id INTEGER PRIMARY KEY, filename TEXT, duration REAL, data_blob BLOB)')
data = np.array([0.1, 0.2, 0.3], dtype=np.float32).tobytes()
c.execute('INSERT INTO audio_records (filename, duration, data_blob) VALUES (?, ?, ?)', ('old_record.wav', 1.5, data))
conn.commit()
conn.close()
EOF

    python3 /tmp/setup_data.py
    rm /tmp/setup_data.py

    useradd -m -s /bin/bash user || true
    chown -R user:user /home/user
    chmod -R 777 /home/user
    chmod -R 777 /app