import pathlib
import warnings
import numpy as np
import pandas as pd
from lmfit.models import GaussianModel
from sklearn import linear_model

MZ_THRESHOLD = 0.03
GAUSSIAN_R2 = 0.5
TPP_R2 = 0.98

warnings.filterwarnings("ignore", category=RuntimeWarning) #Make RuntimeWarning silent in case passnumber = 0


def filter_mz(df, mz, mzthreshold):
    return df[(abs(df.mz.values - mz) < mzthreshold)]


def get_ATDs(z, data, polymer_df):
    ref_mz = polymer_df[f"{z}+"].values
    out_df = pd.DataFrame(columns=[], index=data.drift_time.unique())
    i = 0
    while i < len(ref_mz):
        mz = ref_mz[i]
        DP = polymer_df.index[polymer_df[f"{z}+"] == mz]
        filtered = filter_mz(data, mz, MZ_THRESHOLD)
        filtered = filtered.drop(columns=["mz"])
        if (
            filtered.intensity.max() > 0.001 * data.intensity.max()
        ):  # Here, we only consider ions that are > 0.01% of the intensity of the max peak
            filtered = filtered.groupby("drift_time").sum()
            out_df[f"DP{DP.item():02}"] = filtered
        else:
            pass
        i += 1

    # Replace NaNs by zeros
    out_df = out_df.fillna(0)
    return out_df


def get_tpp(data):
    out_df = pd.DataFrame(columns=["Perturbed_time"])
    for col in data:
        t0 = data[col][0]
        t1 = data[col][2]
        ts = data.index[1:].values
        multipass = data[col][1:].values
        t_one_pass = t1 - t0
        passnumber = np.round(
            (multipass - t0) / (t1 - t0), 0
        )  # !!! The passnumber has to be round !!!
        tnd = multipass - t0
        y_variable = (tnd - ts) / passnumber
        x_variable = ts / passnumber

        mask = ~np.isnan(x_variable) & ~np.isnan(y_variable)
        x_variable = x_variable.reshape(len(x_variable), 1)
        y_variable = y_variable.reshape(len(y_variable), 1)
        regr = linear_model.LinearRegression(fit_intercept=True)

        try:
            regr.fit(x_variable[mask], y_variable[mask])
            # print(regr.coef_[0], regr.intercept_, regr.score(x_variable[mask], y_variable[mask]))
            if regr.score(x_variable[mask], y_variable[mask]) > TPP_R2:
                out_df.loc[int(col[2:]), "Perturbed_time"] = round(*regr.intercept_, 3)

        except ValueError:
            pass
    return out_df


def experiment_parser(datapath, polymer_df):
    fit_dfs = [None]
    # os.chdir(Path.cwd())
    experiment_details = pd.read_excel(datapath, header=0, index_col="File")
    for z in range(1, 6):
        fit_dt = pd.DataFrame(columns=[])

        for index, row in experiment_details.iterrows():
            name = pathlib.Path(index).stem
            data = pd.read_hdf(f"{name}.h5")
            ATD = get_ATDs(z, data, polymer_df)
            x = np.array(ATD.index)

            for col in ATD:
                y = np.array(ATD[col].values)
                model = GaussianModel()
                params = model.guess(y, x=x)
                result = model.fit(y, params, x=x)

                # for evaluation of the fitted parameters
                r2 = result.rsquared

                if r2 > GAUSSIAN_R2:  # FOR THE MOMENT, WE DO NOT CONSIDER SPLIT ATDs
                    fit_dt.loc[row["Separation_time"], col] = round(
                        result.params["center"].value, 3
                    )
                else:
                    pass

        fit_dt = fit_dt.sort_index(axis=1)
        fit_dfs.append(fit_dt)

    return fit_dfs
