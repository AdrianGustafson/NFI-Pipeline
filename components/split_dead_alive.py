import datetime
from pathlib import Path
import pandas as pd
import numpy as np


def report(message):
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d: %H:%M:%S')}::{__name__}] {message}")
    

def bound_variable(df, varname, lower_bound=None, upper_bound=None):
    if lower_bound is not None:
        df = df[df[varname] >= lower_bound]
    if upper_bound is not None:
        df = df[df[varname] <= upper_bound]
        
    return df

    
    
def calc_growth_rates(df, bmass_col, should_be_dead):
    """
    Calculate absolute and relative growth rates for each tree. The trees need to have at least 3 censuses each.
    
    """
    df_tree = pd.DataFrame()
    ct = 0
    for name, subframe in df.groupby('tmt.tree.id'):
        if len(subframe) < 3:
            print("invalid group...")
            continue
        group = subframe.sort_values(by='census.n', ascending=False)
        
        tmp1 = group[['census.date', bmass_col]].values
        tmp2 = np.diff(tmp1, axis=0)
        tmp3 = tmp2[:, 1] / tmp2[:, 0]
        tmp4 = tmp3 / tmp1[2, 1]
        #group = subframe.sort_values(by=['census.date'], ascending=True)
        # Make list of group indices
        idx = group.index.values

        if should_be_dead and (group['tree.status'].iloc[0] != 1):
            print("Found invalid tree!")
            continue
            
        if not should_be_dead and (group['tree.status'].iloc[0] != 0):
            print("Found invalid tree!")
            continue
        
        df_tree.at[ct, 'tmt.tree.id'] = name
        
        # Plot data
        df_tree.at[ct, 'tmt.plot.id'] = group.at[idx[0], 'tmt.plot.id']
        df_tree.at[ct, 'tmt.census.id'] = group.at[idx[0], 'tmt.census.id']
        df_tree.at[ct, 'n.plot'] = group.at[idx[0], 'n.plot']
        df_tree.at[ct, 'n.ha'] = group.at[idx[0], 'n.ha']
        df_tree.at[ct, 'dt'] = -tmp2[1, 0]
        df_tree.at[ct, 'ba1'] = group.at[idx[2], 'ba']
        df_tree.at[ct, 'ba2'] = group.at[idx[1], 'ba']
        df_tree.at[ct, 'ba3'] = group.at[idx[0], 'ba']
        # Tree size data
        df_tree.at[ct, 'gr_a'] = tmp3[1]
        df_tree.at[ct, 'gr_r'] = tmp4[1]
        df_tree.at[ct, f'{bmass_col}_before_death'] = group.at[idx[2], bmass_col]
        df_tree.at[ct, 'height1'] = group.at[idx[2], 'height'] # This might not exist for dead trees
        df_tree.at[ct, 'height2'] = group.at[idx[1], 'height']     
        df_tree.at[ct, 'D1'] = group.at[idx[2], 'd']
        df_tree.at[ct, 'D2'] = group.at[idx[1], 'd']
        df_tree.at[ct, 'pom'] = group.at[idx[0], 'pom']
        
        
        # Other data
        df_tree.at[ct, 'mode.death'] = group.at[idx[0], 'mode.death']
        df_tree.at[ct, 'mode.death.other'] = group.at[idx[0], 'mode.death.other']
        df_tree.at[ct, 'species.cor'] = group.at[idx[0], 'species.cor']
        df_tree.at[ct, 'genus.cor'] = group.at[idx[0], 'genus.cor']
        df_tree.at[ct, 'family.cor'] = group.at[idx[0], 'family.cor']
        
        ct += 1

    return df_tree

def run(config):
    sites = config.get('SITES', [])
    if len(sites) == 0:
        report("No sites provided in settings. Please provide what sites to process.")

    if isinstance(sites, str):
        sites = [sites]

    for site in sites:
        report(f"Starting preparation of traing data {site}")
        ipath = Path(config['INPUT_PATH'].format(site=site))
        opath = Path(config['OUTPUT_PATH'].format(site=site))
        ifname = Path(config['INPUT_FNAME'].format(site=site))
        ofname = Path(config['OUTPUT_FNAME'].format(site=site))
        df = pd.read_csv(ipath.joinpath(ifname))

        # Extract sites with exactly 3 censuses.
        # TODO: A few sites have four sensuses. These could be included with another filtering
        df_3census = df.groupby('tmt.tree.id').filter(lambda subframe: len(subframe) == 3)
        # Make sure censuses are ordered
        #df_3census = df_3census.groupby('tmt.tree.id').apply(lambda subframe: subframe.sort_values('census.n'))
        names_dead = df_3census[(df_3census['tree.status'] == 1)]['tmt.tree.id'].drop_duplicates().tolist()
        df_dead = df_3census[df_3census['tmt.tree.id'].isin(names_dead)]
        df_alive = df_3census[(df_3census['tree.status'] == 0) & (~df_3census['tmt.tree.id'].isin(names_dead))]

        df_dead_tree = calc_growth_rates(df_dead, 'biomass', True)
        df_alive_tree = calc_growth_rates(df_alive, 'biomass', False)

        df_dead_tree['alive'] = 0
        df_alive_tree['alive'] = 1

        df_appended = pd.concat([df_alive_tree, df_dead_tree], ignore_index=True)

        df_appended_bound_rgr = bound_variable(df_appended, 'gr_r', 0, 0.35).drop('gr_a', axis=1)
        df_appended_bound_agr = bound_variable(df_appended, 'gr_a', 0, 0.05).drop('gr_r', axis=1)

        if not opath.exists():
            opath.mkdir(parents=True)

        #df_appended_bound_agr.to_csv(f'{opath}/tree_biomass_agr_{site}_bounded_noharvest.csv', index=False)
        df_appended_bound_rgr.to_csv(opath.joinpath(ofname), index=False)

    report("DNN data preparation finished!")