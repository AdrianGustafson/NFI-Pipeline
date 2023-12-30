import datetime
from pathlib import Path
import pandas as pd

TRAIT_FEATURES = [
    'tmt.tree.id', 'tmt.census.id', 'd.max', 'ba.max', 'biomass.max', 
    'd.growth.max', 'ba.growth.max', 'biomass.growth.max', 'LMA', 'leafN', 
    'wd'
]

def report(message):
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d: %H:%M:%S')}::{__name__}] {message}")

def run(config):
    sites = config.get('SITES', [])
    if len(sites) == 0:
        report("No sites provided in settings. Please provide what sites to process.")

    if isinstance(sites, str):
        sites = [sites]

    for site in sites:
        report(f"Starting connecting trees and traits for {site}")
        ipath = Path(config['INPUT_PATH'].format(site=site))
        ipath_trait = Path(config['INPUT_PATH_TRAIT'].format(site=site))
        opath = Path(config['OUTPUT_PATH'].format(site=site))

        trait_path = ipath_trait.joinpath(Path(f'03_treedata-traits_TMt_{site}.csv'))
        if not trait_path.exists():
            trait_path = ipath_trait.joinpath(Path(f'03_treedata-traits_TMt_{site}.csv.gz'))
        if not trait_path.exists():
            report("Trait data file does not exist in accepted formats. " 
                   "Your file needs to end with either .csv or .csv.gz")
            continue

        df = pd.read_csv(f'{ipath}/tree_biomass_rgr_{site}_bounded_noharvest.csv')
        trait_data = pd.read_csv(trait_path)

        df_traits = pd.merge(df, trait_data[TRAIT_FEATURES], on=['tmt.tree.id', 'tmt.census.id'])

        df_traits.to_csv(f'{opath}/tree_biomass-traits_rgr_{site}_bounded_noharvest.csv', index=False)

    report("Finished connecting traits to trees!")