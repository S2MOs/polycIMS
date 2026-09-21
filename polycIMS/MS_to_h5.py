import os
import pathlib
import subprocess

import pandas as pd


def convert(datapath, mspath):
    input_df = pd.read_excel(datapath, header=0, index_col="File")
    for index, row in input_df.iterrows():
        file_to_convert = index
        name = pathlib.Path(file_to_convert).stem
        outfile = pathlib.Path(f'{name}.h5')

        if outfile.exists():
            continue
        else:
            # Converision from .raw to .mzML
            # os.chdir(pathlib.Path.cwd())
            try:
                os.remove("temp.txt")  # If temp.txt is already present, let's delete it
            except:
                pass

            with open("temp.txt", "a") as f:
                f.write(file_to_convert)  # MSConvert only takes text files as input
            CMD = f"{mspath} --32 --zlib -f {pathlib.Path.cwd()}/temp.txt"
            subprocess.call(CMD, stdout=open(os.devnull, "wb"))

            # Conversion from .mzML to .h5 - Needs to be done in a subprocess
            subprocess.run(
                [
                    sys.executable,
                    "-c",
                    f"""
import deimos
data = deimos.load(r'{name}.mzML', accession={{'drift_time': 'MS:1000016'}})
data = data['ms1']
data = data.drop(columns=['process','scan','function'])
deimos.save(r'{name}.h5', data, mode='w')
""",
                ],
                check=True,
            )

            os.remove("temp.txt")
            os.remove(f"{name}.mzML")
