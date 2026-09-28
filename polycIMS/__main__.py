import argparse
import pathlib
import time
import warnings


from polycIMS import MS_to_h5, calibrate, get_polymermz, h5data_process

mspath = "C:/Users/qduez/AppData/Local/Apps/ProteoWizard 3.0.23312.e6e1708 64-bit/msconvert.exe"

warnings.filterwarnings("ignore", category=FutureWarning)


def existing_file(path):
    p = pathlib.Path(path)
    if not p.is_file():
        raise argparse.ArgumentTypeError(f"{path} is not a valid file")
    return p


def main():
    parser = argparse.ArgumentParser(
        description="polycIMS – Polymer cIMS calibration tool"
    )

    parser.add_argument(
        "-f", "--file", type=existing_file, required=True, help="Input Excel file"
    )

    parser.add_argument(
        "-gas", "--gas", required=True, choices=["He", "N2"], help="Drift gas"
    )

    parser.add_argument(
        "-tdout", "--tdout", required=False, choices=["True", "False"], help="Print td data ? Possible choices : True or False."
    )

    parser.add_argument(
        "-out", "--out", required=False, choices=["True", "False"], help="Print output data ? Possible choices : True or False."
    )

    args = parser.parse_args()

    start = time.perf_counter()
    print("Converting .raw files to .h5 format ... ")
    # Preparing raw files and polymer mz table
    MS_to_h5.convert(args.file, mspath)
    polymer_df = get_polymermz.mz_table_gen()

    print("Getting tpp values ...")
    # Data processing - Determining tpp
    fit_dfs = h5data_process.experiment_parser(args.file, polymer_df)
    if args.tdout == 'True':
        for z in range(1, 6):
            fit_dfs[z].to_excel(f'td_data_{z}+.xlsx')
    else:
        pass

    print("Making the calibration curves ...")

    cal_df = calibrate.make_calibration_curve(fit_dfs, polymer_df, args.gas)
    calibrate.make_plots(cal_df, args.gas)

    print("Calibration curves generated !")
    end = time.perf_counter()
    print(f"Total runtime: {end - start:.2f} seconds")
    print(f"Worked with {len(cal_df)} ions")
    print(f"Calibration between {cal_df['CCSref'].min()} and {cal_df['CCSref'].max()} Å²")
    if args.out == 'True':
        cal_df.to_excel('cal_data.xlsx')
    else:
        pass

if __name__ == "__main__":
    main()
