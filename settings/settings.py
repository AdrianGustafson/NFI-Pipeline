# Settings file for the NFI data extraction
import os

# Input data path
BASE_DATA_PATH = ''

# Output directory path
STORE_DATA_PATH = os.path.join(BASE_DATA_PATH, 'store_base')

# What data to use
# 'Full' = all the data including managed plots
# 'Noharvest' = Only reserve data without management
USE_DATA = 'Noharvest'

ALL_SITES = ['UKR', 'UKF', 'RSF', 'SLO', 'GEM', 'FRM', 'NFG', 'NNL', 'NPO', 'NSW']
RESERVE_SITES = ['UKR', 'UKF', 'RSF', 'SLO', 'GEM', 'FRM', 'NSW']

PIPELINE = [
    #'components.extract_noharvest',
    #'components.split_dead_alive',
    'components.create_test_set',
    'components.append_sites',
    'components.train_dnn'
]


APPEND_SITES = {
    'INPUT_PATH': os.path.join(STORE_DATA_PATH, '{site}'),
    'OUTPUT_PATH': os.path.join(STORE_DATA_PATH, 'appended'),
    'SITES': RESERVE_SITES,
    'INPUT_FNAME': 'tree_biomass_rgr_{site}_bounded_noharvest_{traintest}.csv',
    'OUTPUT_FNAME': 'tree_biomass_rgr_bounded_noharvest_{traintest}.csv',
    'TRAIN_TEST': ('train', )
}

EXTRACT_NOHARVEST = {
    'INPUT_PATH': os.path.join(BASE_DATA_PATH, '{site}'),
    'OUTPUT_PATH': os.path.join(STORE_DATA_PATH, '{site}'),
    'OFNAME_BIOMASS': '01_treedata-biomass_TMt_{site}_noharvest.csv',
    'OFNAME_STAND': '02_stand-level-dynamics_TMt_{site}_noharvest.csv',
    'SITES': ALL_SITES
}

CREATE_TEST_SET = {
    'INPUT_PATH': os.path.join(STORE_DATA_PATH, '{site}'),
    'INPUT_FNAME': 'tree_biomass_rgr_{site}_bounded_noharvest.csv',
    'OUTPUT_PATH': os.path.join(STORE_DATA_PATH, '{site}'),
    'OUTPUT_FNAME': 'tree_biomass_rgr_{site}_bounded_noharvest_{traintest}.csv',
    'SITES': ALL_SITES,
    'TEST_RATIO': 0.2,
    'STRATIFY': True,
    'STRAT_COL': ['alive', 'species.cor']
}

CONNECT_TRAITS = {
    'INPUT_PATH': os.path.join(STORE_DATA_PATH, '{site}'),
    'INPUT_PATH_TRAIT': os.path.join(STORE_DATA_PATH, '{site}'),
    'OUTPUT_PATH': os.path.join(STORE_DATA_PATH, '{site}'),
    'SITES': RESERVE_SITES,
}

SPLIT_DEAD_ALIVE = {
    'INPUT_PATH': os.path.join(STORE_DATA_PATH,'{site}'),
    'OUTPUT_PATH': os.path.join(STORE_DATA_PATH, '{site}'),
    'INPUT_FNAME': '01_treedata-biomass_TMt_{site}_noharvest.csv',
    'OUTPUT_FNAME': 'tree_biomass_rgr_{site}_bounded_noharvest.csv',
    'SITES': ALL_SITES,
}

TRAIN_DNN = {
    'INPUT_PATH': os.path.join(STORE_DATA_PATH, 'appended'),
    'OUTPUT_PATH': os.path.join(STORE_DATA_PATH, 'artifacts'),
    'TRAIN_INPUT_FNAME': 'tree_biomass_rgr_bounded_noharvest_train.csv',
    'ARTIFACT_NAME': 'DNN_4_LPJG_input_norm_sklearn.pt',
    'EPOCHS': 3000,
    'LEARN_RATE': 0.00003,
    'BATCH_SIZE': 512,
    'FEATURES': ['gr_r', 'biomass_before_death', 'dt']
}
