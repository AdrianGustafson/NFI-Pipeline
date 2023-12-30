import datetime
from pathlib import Path
import pandas as pd


def report(message):
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d: %H:%M:%S')}::{__name__}] {message}")

def run(config):
    sites = config.get('SITES', [])
    if len(sites) == 0:
        report("No sites provided in settings. Please provide what sites to process.")

    if isinstance(sites, str):
        sites = [sites]

    opath = Path(config['OUTPUT_PATH'])
    if not opath.exists():
        opath.mkdir(parents=True)

    append_sets = config['TRAIN_TEST']

    report("Appending files")
    for traintest in append_sets:
        sitedata = []
        for site in sites:
            ipath = Path(config['INPUT_PATH'].format(site=site))
            ifname = config['INPUT_FNAME'].format(site=site, traintest=traintest)
            df = pd.read_csv(ipath.joinpath(Path(ifname)))
            sitedata.append(df.copy())

        df_sites = pd.concat(sitedata, ignore_index=True)  
        ofname = config['OUTPUT_FNAME'].format(traintest=traintest)
        df_sites.to_csv(opath.joinpath(Path(ofname)), index=False)

    report("Finished appending files!")