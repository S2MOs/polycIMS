import pandas as pd
from molmass import Formula
from pyteomics.mass import calculate_mass, most_probable_isotopic_composition


def mz_table_gen():
    polymer_df = pd.DataFrame(columns=[])

    monomer = "C2H4O"
    chain_ends = "H2O"
    cation = "Na"

    for n in range(1, 150):
        for z in range(1, 6):
            formula = Formula(n * monomer + chain_ends + z * cation)
            biggest_isotope = most_probable_isotopic_composition(str(formula))
            composition, abundance = biggest_isotope
            polymer_df.loc[n, f"{z}+"] = round(calculate_mass(composition) / z, 4)

    return polymer_df
