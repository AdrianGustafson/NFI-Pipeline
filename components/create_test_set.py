import datetime
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split

SPECIES_COL = 'species.cor'
SPECIES_CLASS_COL = 'species.class'

def report(message):
    print(f"[{datetime.datetime.now().strftime('%Y-%m-%d: %H:%M:%S')}::{__name__}] {message}")
    
class NFIPipelineError(ValueError):
    pass

def run(config):
    sites = config.get('SITES', [])
    if len(sites) == 0:
        report("No sites provided in settings. Please provide what sites to process.")

    if isinstance(sites, str):
        sites = [sites]

    perform_stratification = config.get('STRATIFY', False)
    strat_cols_config = config.get('STRAT_COL', None)
    for site in sites:
        report(f"Starting splitting of train/test datasets for {site}")
        ipath = Path(config['INPUT_PATH'].format(site=site))
        opath = Path(config['OUTPUT_PATH'].format(site=site))
        ifname = Path(config['INPUT_FNAME'].format(site=site))
        ofname = config['OUTPUT_FNAME']

        df = pd.read_csv(ipath.joinpath(ifname))

        # Split the dataset for training and testing. 
        strat_data = None
        
        if perform_stratification:
            strat_cols = strat_cols_config.copy()
            if strat_cols is None:
                raise NFIPipelineError("Invalid settings. STRATIFY is True with STRAT_COLS not specified")
            
            # If stratification by species should be done, group species with few observations
            if ((isinstance(strat_cols, list) and SPECIES_COL in strat_cols) or
                (isinstance(strat_cols, str) and strat_cols == SPECIES_COL)):

                if isinstance(strat_cols, list):
                    colidx = strat_cols.index(SPECIES_COL)
                    col = strat_cols.pop(colidx)
                else:
                    col = SPECIES_COL

                counts = df[col].value_counts()
                df[SPECIES_CLASS_COL] = 'other'
                for name, count in counts.items():
                    if count > 500:
                        df.loc[df[col] == name, SPECIES_CLASS_COL] = name

                # Put back in the same place to keep ordering
                if isinstance(strat_cols, list):
                    strat_cols.insert(colidx, SPECIES_CLASS_COL)

            strat_data = df[strat_cols]
        
        train, test = train_test_split(df, test_size=config.get('TEST_RATIO', 0.2), random_state=42, stratify=strat_data)

        if perform_stratification:
            train.drop(SPECIES_CLASS_COL, axis=1, inplace=True)
            test.drop(SPECIES_CLASS_COL, axis=1, inplace=True)

        if not opath.exists():
            opath.mkdir(parents=True)

        train.to_csv(opath.joinpath(Path(ofname.format(site=site, traintest='train'))), index=False)
        test.to_csv(opath.joinpath(Path(ofname.format(site=site, traintest='test'))), index=False)

    report("Finished splitting train/test datasets")
        


