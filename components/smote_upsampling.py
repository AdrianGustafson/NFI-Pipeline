import datetime
import fnmatch
from pathlib import Path
import pandas as pd
import numpy as np
from imblearn.over_sampling import SMOTENC, SMOTE


def report(message):
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d: %H:%M:%S')}::{__name__}] {message}")

def get_features(feature_list, columns):
    """Utility function to expand wildcard features in the list, e.g., used for species
    
    """
    res = []
    for feature in feature_list:
        if '*' in feature:
            matches = fnmatch.filter(columns, feature)
            res.extend(matches)
        else:
            res.append(feature)
    return res


def run(config):
    report("Commence SMOTEing the dataset")

    sites = config.get('SITES', [])
    if len(sites) == 0:
        report("No sites provided in settings. Please provide what sites to process.")

    if isinstance(sites, str):
        sites = [sites]

    resample_vars = config['VARIABLES']

    for site in sites:
        ipath = Path(config['INPUT_PATH'].format(site=site))
        ifname = Path(config['INPUT_FNAME'].format(site=site))
        opath = Path(config['OUTPUT_PATH'].format(site=site))
        ofname = Path(config['OUTPUT_FNAME'].format(site=site))
        

        df = pd.read_csv(ipath.joinpath(ifname))

        target = df.pop('alive')

        usecols = get_features(resample_vars, df.columns)

        if 'species.cor' in usecols:
            catidx = df[usecols].columns.get_loc('species.cor')
            smote = SMOTENC(random_state=42, categorical_features=[catidx], )
        else:
            smote = SMOTE(random_state=42)

        resampled_data, resampled_labels = smote.fit_resample(df[usecols], target)

        df_smote = pd.merge(resampled_data, resampled_labels, left_index=True, right_index=True)

        if not opath.exists():
            opath.mkdir(parents=True)

        df_smote.to_csv(opath.joinpath(ofname), index=False)


    report("Finished!")
