# polycIMS: Automated CCS Calibration for Cyclic Traveling Wave Ion Mobility Spectrometry (cIMS)

polycIMS is a command-line tool for processing cIMS data and performing automated collisional cross section (CCS) calibration, using commercial poly(ethylene glycol) as calibrant.

The software takes Waters *.dt.raw files acquired on Waters Select Series instruments and produces calibration curves with effective CCS values in helium (He) or nitrogen (N<sub>2</sub>.).

This package accompanies the publication **PolycIMS: Polymers for Automated Cyclic Ion Mobility Spectrometry Calibration**, Q.Duez, L. Groignet, T. Robert, F. Chirot, P. Gerbaux, J. De Winter, *Submitted*.

## Before you start
polycIMS has been tested on **Windows**.

You do **not** need to have any previous experience with Python or programming to use polycIMS. The installation mainly consists of installing three software packages and entering a few commands into an Anaconda/Miniconda Prompt.

polycIMS requires the following software:

1. [Git](https://git-scm.com/install/windows) — used to download the polycIMS code (~62 MB)
2. [Miniconda](https://www.anaconda.com/download/success?reg=skipped) — used to install Python and the required Python packages (~128 MB)
3. [ProteoWizard](https://proteowizard.sourceforge.io/download.html) — provides `msconvert.exe`, which is required to read Waters data and convert into Python-readable files (~88 MB)

**Miniconda is recommended.** Anaconda can also be used instead of Miniconda, but the full Anaconda installation is substantially larger.

> **Important:** You do not need to install Python separately. Miniconda will provide the Python environment required by polycIMS.
> **Important - 2 :** Do not use spaces in folder or file names. If you need to separate words, use underscores.

---

**OPTIONAL BUT USEFUL :**
For convenience, it is possible to edit Windows' Registry and open Anaconda prompts in specific working directories. Here is how to do it :
1. Run Registry Editor (Windows button, type Registry, launch as Administrator)
2. Go to HKEY_CLASSES_ROOT > Directory > Background > shell
3. Right click on 'shell'; New > Key; Rename the key `AnacondaPrompt`; Double click on (Default) and set value to `Anaconda Prompt Here`
4. In the key AnacondaPrompt; Right click; New > Key; Rename the key `command`, and set its value to ```cmd.exe /K PATH_TO_CONDA_INSTALLATION\activate.bat```. Change PATH_TO_CONDA by the location of your Miniconda or Anaconda installation is located. Mine is `C:\Users\user\Anaconda3_OR_Miniconda3\Scripts\activate.bat`. Don't forget ```cmd.exe /K``` after changing PATH_TO_CONDA.

5. Close the Registry Editor

## Installation

> You will only need to do this once.

1. **Download polycIMS**

Create a directory where the code will be stored. Navigate to the directory you created and open a Miniconda/Anaconda prompt there. To do so, Right click + 'Anaconda Prompt Here'(if you did the optional step above).

Then, enter the following commands one by one into the prompt :

```
git clone https://github.com/S2MOs/polycIMS.git
```
```
cd polycIMS
```

2. **Create the polycIMS environment**

The next steps create a dedicated Python environment called `polycIMS`. You will need to accept terms of service associated with conda.

```
conda update -n base conda
```

The Libmamba solver is also installed to rapidly handle the environment :
```
conda install -n base conda-libmamba-solver
```
```
conda config --set solver libmamba
```

**Important:** The next command might take a while (20-30 min, or more depending on your internet connection and computer)... This is perfectly normal. It will also download ~722 MB of data.
```
conda env create -f environment.yml
```
```
conda activate polycIMS
```

3. **Install polycIMS**

```
pip install -e .
```

4. **Test the installation**

Test whether you can use polycIMS with command line :
```
polycIMS
```
The expected output should be :
```
usage: polycIMS [-h] -f FILE -gas {He,N2} [-tdout {True,False}] [-out {True,False}]
polycIMS: error: the following arguments are required: -f/--file, -gas/--gas
```

This is not an installation error.

It means that polycIMS has been successfully installed and is waiting for you to provide an input Excel file and the desired collision gas. The important part is that the command polycIMS is recognized.

5. **Tell polycIMS where `msconvert.exe` is located**

`msconvert.exe` is normally located somewhere similar to `C:\Users\YourName\AppData\Local\Apps\ProteoWizard XXX\msconvert.exe`

At present, this location must be entered manually in the polycIMS source code. Navigate into the polycIMS folder and edit `__main__.py` with your favourite NotePad editor.

To include the path to `msconvert.exe`, find
```
mspath = "PATH/TO/MSCONVERT/msconvert.exe"
```
And replace the path with the actual location of `msconvert.exe`.

**Important:** Use forward slashes `/`. The Windows backslashes `\` will not work.


## Usage

> You must follow these steps each time you want to use polycIMS.

1. **Prepare your calibration data**

Create a folder containing Waters *dt.raw files corresponding to your calibrants, recorded at different Separate times. It is important to only use *dt.raw files containing cIMS data, and not *.raw files.

2. **Prepare an Excel input file**

In the same folder, create an Excel sheet which should contain the following headers and information (**!! syntax matters for the column headers !!**) :

| File  | Separation_time |
| :-------------: | :---: |
| FILE1_dt.raw  | 2 |
| FILE2_dt.raw  | 0 |
| FILE3_dt.raw  | 15 |
| FILE4_dt.raw  | 30 |
| FILE5_dt.raw  | 50 |

Separation_time corresponds to the cIMS separation time associated with each spectrum. Separation_time = 0 corresponds to the 'Bypass' experiment.

3. **Run the calibration**

Open an Anaconda prompt in that directory (Right click + Anaconda Prompt Here), activate polycIMS and run the tool (replace the arguments in the `{}`, including the brackets) :
```
conda activate polycIMS
```
```
polycIMS -f {name_of_your_Excel_sheet}.xlsx -gas {He/N2}
```

4. Wait for the process to finish.

5. The output should be a `.svg` file in the same folder, containing the calibration curve.

6. Working examples are available at https://github.com/S2MOs/polycIMS_examples, feel free to try them !

#### Optional :

It is possible to print intermediate results from polycIMS using the arguments `-tdout True` or `-out True` when calling polycIMS from the command line.

`-tdout` prints the extracted arrival times for invidiual polymer ions as a function of their charge state and degree of polymerization (DP). This allows users to verify proper linearization for the determination of $t_{pp}$. The output is a series of Excel sheets called `td_data_{x}+.xlsx`.

`-out` prints the calibration data, corresponding to the regression of $ln(CCS(sqrt(µ)/z)$ as a function of $ln(t_{pp})$. The output is `cal_data.xlsx`.

## Updating polycIMS
If a newer version of polycIMS becomes available, the existing installation can be updated by downloading the latest version of the GitHub repository. Don't forget to edit the `msconvert.exe` path in `__main__.py` for the newest version !

Before updating, please check the GitHub repository for the corresponding release/version instructions.

## Citing polycIMS
If you would like to reference polycIMS, please cite the following:
- polycIMS, version 1.0 (https://github.com/S2MOs/polycIMS)
- Q. Duez, L. Groignet, T. Robert, F. Chirot, P. Gerbaux, J. De Winter, **PolycIMS: Polymers for Automated Cyclic Ion Mobility Spectrometry Calibration**, *Submitted*.

## If you face issues
Please create an 'Issue' on GitHub and copy the complete error message from the Anaconda/Miniconda Prompt. If possible, please also provide the datafiles that you are trying to calibrate.

This will make it much easier to identify the problem.
