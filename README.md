# polycIMS: Automated CCS Calibration for Cyclic Traveling Wave Ion Mobility Spectrometry (cIMS)

polycIMS is a command-line tool for processing cIMS data and performing automated collisional cross section (CCS) calibration, using commercial poly(ethylene glycol) as calibrant. Inputs are Waters *dt.raw files from Waters Select Series instruments and outputs are calibration curves, with effective CCS values in He or N<sub>2</sub>.

This package accompanies the publication **PolycIMS: Polymers for Automated Cyclic Ion Mobility Spectrometry Calibration**, Q.Duez, L. Groignet, T. Robert, F. Chirot, P. Gerbaux, J. De Winter, *Submitted*.

## Prerequisite
polycIMS requires installing [Git](https://git-scm.com/install/windows) (62 Mo), [Miniconda](https://www.anaconda.com/download/success?reg=skipped) (128 Mo) and [ProteoWizard](https://proteowizard.sourceforge.io/download.html)(88 Mo).

Anaconda could also be installed instead of Miniconda, but the file size will be much larger.

**OPTIONAL BUT USEFUL :**
For convenience, it is possible to edit Windows' Registry and open Anaconda prompts in specific working directories. Here is how to do it :
1. Run Registry Editor (Windows button + R, then type regedit)
2. Go to HKEY_CLASSES_ROOT > Directory > Background > shell
3. Right click on 'shell'; New > Key; Rename the key AnacondaPrompt; Double click and set its value to Anaconda Prompt Here
4. Under the key AnacondaPrompt, add another key called command, and set its value to
```cmd.exe /K C:\Users\user\Anaconda3\Scripts\activate.bat```
or change the location to wherever your Miniconda or Anaconda installation is located.
5. Close the Registry Editor

## Installation

**General note : Never add spaces ' ' in your folder or file names. This breaks the code. Always replace spaces with underscores _.**

Create a directory where the code will be stored. Navigate to the directory you created and open an prompt there by right clicking + 'Anaconda Prompt Here'. Input the following commands in the prompt :

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
```
The next command might take a while (20-30 min)... This is perfectly normal. It will also download ~722 Mo of data.
```
conda env create -f environment.yml
conda activate polycIMS
```

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
5. Navigate into the polycIMS folder and edit `__main__.py` with your favourite text editor to include the path to `msconvert` :
```
mspath = "PATH/TO/MSCONVERT/msconvert.exe"
```
Note : `msconvert.exe` should be located in `AppData/Local/Apps/ProteoWizard XXX/msconvert.exe`.
Note 2 : Be careful at the orientation of the slash `/`. Backslashes `\` will not work.

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

Separation_time = 0 corresponds to tbe 'Bypass' experiment.

3. Open an Anaconda prompt in that directory, activate polycIMS and run the tool (replace the arguments in the `{}`, including the brackets) :
```
conda activate polycIMS
polycIMS -f {name_of_your_Excel_sheet}.xlsx -gas {He/N2}
```

4. Wait a bit.

5. The output should be a `.svg` file in the same folder, containing calibration curves.

6. Working examples are available at https://github.com/S2MOs/polycIMS_examples, feel free to try them !

## Citing polycIMS
If you would like to reference polycIMS, please cite the following:
- polycIMS, version 1.0 (https://github.com/S2MOs/polycIMS)
- Q. Duez, L. Groignet, T. Robert, F. Chirot, P. Gerbaux, J. De Winter, **PolycIMS: Polymers for Automated Cyclic Ion Mobility Spectrometry Calibration**, *Submitted*.
