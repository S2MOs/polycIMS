# polycIMS: Automated CCS Calibration for Cyclic Traveling Wave Ion Mobility Spectrometry (cIMS)

polycIMS is a command-line tool for processing cIMS data and performing automated collisional cross section (CCS) calibration, using commercial poly(ethylene glycol) as calibrant. Inputs are Waters *dt.raw files from Waters Select Series instruments and outputs are calibration curves, with effective CCS values in He or N<sub>2</sub>.

This package accompanies the publication **PolycIMS: Polymers for Automated Cyclic Ion Mobility Spectrometry Calibration**, Q.Duez, L. Groignet, T. Robert, F. Chirot, P. Gerbaux, J. De Winter, *Submitted*.

## Prerequisite
polycIMS requires installing [Git](https://git-scm.com/install/windows), [Anaconda](https://www.anaconda.com/docs/getting-started/miniconda/main) and ProteoWizards' [msconvert](https://proteowizard.sourceforge.io/doc_users.html).

For convenience, it is possible to edit Windows' Registry and open Anaconda prompts in specific working directories. Here is how to do it :
1. Run Registry Editor (regedit.exe)
2. Go to HKEY_CLASSES_ROOT > Directory > Background > shell
3. Add a key named AnacondaPrompt and set its value to Anaconda Prompt Here
4. Add a key under this key called command, and set its value to cmd.exe /K C:\Users\user\Anaconda3\Scripts\activate.bat change the location to wherever your Anaconda installation is located.

## Installation

1. Clone the repository and navigate into it :
```
git clone https://github.com/S2MOs/polycIMS.git
cd polycIMS
```

2. Update anaconda, create a virtual environment and activate it. Libmamba is also installed to rapidly handle the environment :
```
conda update anaconda
conda update -n base conda
conda install -n base conda-libmamba-solver
conda config --set solver libmamba
conda env create -f environment.yml
conda activate polycIMS
```
The environment creation might take a while... This is perfectly normal.

3. Install polycIMS :
```
pip install -e .
```

4. Test whether you can use polycIMS with command line :
```
polycIMS
```
The expected output should be :
```
usage: polycIMS [-h] -f FILE -gas {He,N2}
polycIMS: error: the following arguments are required: -f/--file, -gas/--gas
```
5. Navigate into the polycIMS folder and edit `__main__.py` to include the path to `msconvert` :
```
mspath = "PATH/TO/MSCONVERT/msconvert.exe"
```

## Usage

1. Create a folder containing Waters *dt.raw files corresponding to your calibrants, recorded at different Separate times. It is important to only use *dt.raw files containing cIMS data, and not *.raw files.

2. In that folder, create an Excel sheet which should contain the following headers and information (**!! syntax matters for the column headers !!**) :

| File  | Separation_time |
| :-------------: | :---: |
| FILE1_dt.raw  | 2 |
| FILE2_dt.raw  | 0 |
| FILE3_dt.raw  | 15 |
| FILE4_dt.raw  | 30 |
| FILE5_dt.raw  | 50 |

3. Open an Anaconda prompt in that directory, activate polycIMS and run the tool (replace the arguments in the `{}`) :
```
conda activate polycIMS
polycIMS -f {name_of_your_Excel_sheet}.xlsx -gas {He/N2}
```

4. Wait a bit.

5. The output should be a `.svg` file in the same folder, containing calibration curves.

## Citing polycIMS
If you would like to reference polycIMS, please cite the following:
- polycIMS, version 1.0 (https://github.com/S2MOs/polycIMS)
- Q. Duez, L. Groignet, T. Robert, F. Chirot, P. Gerbaux, J. De Winter, **PolycIMS: Polymers for Automated Cyclic Ion Mobility Spectrometry Calibration**, *Submitted*.
