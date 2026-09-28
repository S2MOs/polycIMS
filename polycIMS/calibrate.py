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
    base = linear_model.LinearRegression(fit_intercept=True)
    regr = linear_model.RANSACRegressor(estimator=base)
    regr.fit(x_variable, y_variable)
    print("A'"+f" = {np.round(np.exp(*regr.estimator_.intercept_),4)}")
    print(f"B = {np.round(*regr.estimator_.coef_[0],4)}")
    print(f"R²(Without outliers) = {np.round(regr.estimator_.score(x_variable[regr.inlier_mask_], y_variable[regr.inlier_mask_]),4)}")
    print(f"R²(With outliers) = {np.round(regr.estimator_.score(x_variable, y_variable),4)}")

    fig, ax = plt.subplots(figsize=(4, 4))

    sns.scatterplot(data=cal_df, x="ln_tpp", y="ln_CCSprime")
    ax.plot(x_variable, regr.estimator_.predict(x_variable), c="red")
    ax.set_xlabel("$ln(t_{pp})$", fontsize=10)
    ax.set_ylabel(r"$\ln\left(CCS_{\mathrm{ref}}\,\frac{\sqrt{\mu}}{z}\right)$", fontsize=10)

    ax.set_facecolor("#F8F8FB")

    ax.text(
        0.05,
        0.95,
        f"y = {np.round(*regr.estimator_.coef_[0],4)}.x + {np.round(*regr.estimator_.intercept_,4)} \nA' = {np.round(np.exp(*regr.estimator_.intercept_),4)} \nB = {np.round(*regr.estimator_.coef_[0],4)}",
        transform=ax.transAxes,
        fontsize=11,
        color="r",
        verticalalignment="top",
        horizontalalignment="left",
    )

    plt.savefig(f"CalibrationCurves_{gas}.svg", format="svg", bbox_inches="tight", dpi=600)
