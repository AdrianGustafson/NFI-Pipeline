import sys
import datetime
from pathlib import Path
import pandas as pd

def report(message):
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d: %H:%M:%S')}::{__name__}] {message}")

def get_noharvest_plots(stand_dynamics):
    noharvest_plots = []
    for name, plotdata in stand_dynamics.groupby('tmt.plot.id'):
        harvest = plotdata['harvest'].sum()
        if harvest == 0:
            noharvest_plots.append(name)
    return noharvest_plots

def extract_plot(treedata, stand_dynamics):
    # Find which sites have harvest
    noharvest_plots = get_noharvest_plots(stand_dynamics)

    # Filter out sites without harvest
    stand_dynamics_noharvest = stand_dynamics[stand_dynamics['tmt.plot.id'].isin(noharvest_plots)]
    treedata_biomass_noharvest = treedata[treedata['tmt.plot.id'].isin(noharvest_plots)]
    return treedata_biomass_noharvest, stand_dynamics_noharvest

def extract_tree(treedata, stand_dynamics):
    # Find which sites have harvest
    noharvest_plots = get_noharvest_plots(stand_dynamics)
    stand_dynamics_noharvest = stand_dynamics[stand_dynamics['tmt.plot.id'].isin(noharvest_plots)]

    treedata_biomass_noharvest = None

    return treedata_biomass_noharvest, stand_dynamics_noharvest


def run(config):
    sites = config.get('SITES', [])
    if len(sites) == 0:
        report("No sites provided in settings. Please provide what sites to process.")

    if isinstance(sites, str):
        sites = [sites]

    strategy = config.get('STRATEGY', 'plot')

    for site in sites:
        report(f"Starting extraction of noharvest plots for {site}")
        ipath = Path(config['INPUT_PATH'].format(site=site))
        opath = Path(config['OUTPUT_PATH'].format(site=site))

        # Open files
        treedata_path = ipath.joinpath(Path(f'01_treedata-biomass_TMt_{site}.csv'))
        if not treedata_path.exists():
            treedata_path = ipath.joinpath(Path(f'01_treedata-biomass_TMt_{site}.csv.gz'))
        if not treedata_path.exists():
            report("Treedata file does not exist in accepted formats. " 
                   "Your file needs to end with either .csv or .csv.gz")
            continue

        treedata_biomass = pd.read_csv(treedata_path).drop('Unnamed: 0', axis=1)
        standdata_path = ipath.joinpath(Path(f'02_stand-level-dynamics_TMt_{site}.csv'))
        if not standdata_path.exists():
            standdata_path = ipath.joinpath(Path(f'02_stand-level-dynamics_TMt_{site}.csv.gz'))
        if not standdata_path.exists():
            report("Stand dynamics file does not exist in accepted formats."
                   "Your file needs to end with either .csv or .csv.gz")
            continue
        stand_dynamics = pd.read_csv(standdata_path).drop('Unnamed: 0', axis=1)
    
        if strategy.lower() == 'plot':
            treedata_biomass_noharvest, stand_dynamics_noharvest = extract_plot(treedata_biomass, stand_dynamics)
        elif strategy.lower() == 'tree':
            treedata_biomass_noharvest, stand_dynamics_noharvest = extract_tree(treedata_biomass, stand_dynamics)
        else:
            raise ValueError("Invalid strategy option: allowed are (plot, tree)")

        # Write data to disk
        if not opath.exists():
            opath.mkdir(parents=True)

        ofname_treedata = Path(config['OFNAME_BIOMASS'].format(site=site, strategy=strategy))
        ofname_stand = Path(config['OFNAME_STAND'].format(site=site, strategy=strategy))
        treedata_biomass_noharvest.to_csv(opath.joinpath(ofname_treedata), index=False)
        stand_dynamics_noharvest.to_csv(opath.joinpath(ofname_stand), index=False)

    report("Harvest data extracted")

if __name__ == '__main__':    
    args = sys.argv
    nargs = len(args)
    import settings
    # Extract input arguments
    name = args[0]
    print(name)

    
    component_settings = getattr(settings, name, {})
    # Run the extractions
    #run(component_settings)
