# MRIPhillipsKspaceReader

A simple tool to automate the GPI Phillips toolbox for reading in .raw kspace files.

## Installation
You need to install [GPI](https://github.com/gpilab/framework), [GPI Core](https://github.com/gpilab/core-nodes), and the [Phillips data reader](https://github.com/gpilab/philips-data-reader). I would recommend just using the anaconda installations [here](https://anaconda.org/conda-forge/gpi) and [here](https://anaconda.org/conda-forge/gpi_core). The Phillips data reader must be downloaded manually, see their Github repo for more information.

## How to use

Open the ```convert_to_kspace.py``` and change line 55 and 56 to where the files are located and where the files are to be saved. Then just run the python script as usual. Note, whatever you do, do not change or touch the .net files.

All k-space files will be saved as numpy arrays (.npy), but the files depend on the scan.

**Important**

If you want to use this on a server without a screen you need to run the following command:
```
export QT_QPA_PLATFORM=offscreen
```