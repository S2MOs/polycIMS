from importlib import resources

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn import linear_model

from polycIMS import h5data_process

sns.set_theme(style="ticks", context="paper")


def make_calibration_curve(fit_dfs, polymer_df, gas):

    cal_df = pd.DataFrame()

    for z in range(1, 6):
        with resources.files("polycIMS").joinpath(f"ref/CCSref_{z}+_{gas}.xlsx").open(
            "rb"
        ) as f:
            CCS_ref = pd.read_excel(f, header=0, index_col="DP")
        tpp_data = h5data_process.get_tpp(fit_dfs[z])
        tpp_data["CCSref"] = CCS_ref["CCSref"]
        tpp_data = tpp_data.dropna()
        tpp_data["Perturbed_time"] = pd.to_numeric(
            tpp_data["Perturbed_time"], errors="coerce"
        )  # Convert values to numeric for calculations
        tpp_data["mu"] = (28 * z * polymer_df.loc[tpp_data.index, f"{z}+"]) / (
            28 + (z * polymer_df.loc[tpp_data.index, f"{z}+"])
        )
        tpp_data["ln_tpp"] = np.log(tpp_data["Perturbed_time"])
        tpp_data["CCSprime"] = CCS_ref["CCSref"] / (z * np.sqrt(1 / tpp_data["mu"]))
        tpp_data["ln_CCSprime"] = np.log(tpp_data["CCSprime"])
        tpp_data["z"] = z
        cal_df = pd.concat([cal_df, tpp_data], ignore_index=True)

    cal_df = cal_df.dropna()

    return cal_df


def make_plots(cal_df, gas):

    y_variable = cal_df["ln_CCSprime"].values
    x_variable = cal_df["ln_tpp"].values

    x_variable = x_variable.reshape(len(x_variable), 1)
    y_variable = y_variable.reshape(len(y_variable), 1)
    regr = linear_model.LinearRegression(fit_intercept=True)
    regr.fit(x_variable, y_variable)
    print(f"B = {np.round(*regr.coef_[0],4)}, R² = {np.round(regr.score(x_variable, y_variable),4)}")

    cal_df["tpp_power"] = (
        cal_df["Perturbed_time"] ** (regr.coef_[0])
        * cal_df["z"]
        * np.sqrt(1 / cal_df["mu"])
    )

    y_variable_2 = cal_df["CCSref"].values
    x_variable_2 = cal_df["tpp_power"].values

    x_variable_2 = x_variable_2.reshape(len(x_variable_2), 1)
    y_variable_2 = y_variable_2.reshape(len(y_variable_2), 1)
    regr_2 = linear_model.LinearRegression(fit_intercept=False)
    regr_2.fit(x_variable_2, y_variable_2)

    print("A'"+f" = {np.round(*regr_2.coef_[0],4)}, R² = {np.round(regr_2.score(x_variable_2, y_variable_2),4)}")

    fig, ax = plt.subplots(1, 2, figsize=(8, 3))

    sns.scatterplot(data=cal_df, x="ln_tpp", y="ln_CCSprime", ax=ax[0])
    ax[0].plot(x_variable, regr.predict(x_variable), c="red")
    sns.scatterplot(data=cal_df, x="tpp_power", y="CCSref", ax=ax[1])
    ax[1].plot(x_variable_2, regr_2.predict(x_variable_2), c="red")
    ax[0].set_xlabel("$ln(t_{pp})$", fontsize=10)
    ax[0].set_ylabel(r"$ln(CCS_{ref}\:\\frac{\\sqrt{\\mu}}{z})$", fontsize=10)
    ax[1].set_xlabel("$t_{pp}\\prime$", fontsize=10)
    ax[1].set_ylabel("$CCS_{ref}$", fontsize=10)

    ax[0].set_facecolor("#F8F8FB")
    ax[1].set_facecolor("#F8F8FB")

    ax[0].text(
        0.05,
        0.95,
        f"y = {np.round(*regr.coef_[0],4)}.x + {np.round(*regr.intercept_,4)} \n  $R^²$ = {np.round(regr.score(x_variable, y_variable), 4)}",
        transform=ax[0].transAxes,
        fontsize=10,
        color="r",
        verticalalignment="top",
        horizontalalignment="left",
    )
    ax[1].text(
        0.05,
        0.95,
        f"y = {np.round(*regr_2.coef_[0],4)}.x \n  $R^²$ = {np.round(regr_2.score(x_variable_2, y_variable_2), 4)}",
        transform=ax[1].transAxes,
        fontsize=10,
        color="r",
        verticalalignment="top",
        horizontalalignment="left",
    )

    plt.subplots_adjust(
        left=None, bottom=None, right=None, top=None, wspace=0.25, hspace=None
    )
    plt.savefig(f"CalibrationCurves_{gas}.svg", format="svg", bbox_inches="tight", dpi=600)
